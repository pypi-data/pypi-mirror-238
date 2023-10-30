import numpy as np
import math
from collections import Counter

class Node:
    def __init__(self, feature=None, thresh=None, leaf=None, right=None, value=None):
        self.feature = feature
        self.thresh = thresh
        self.leaf = leaf
        self.right = right
        self.value = value

    def is_leaf(self):
        return self.value is not None

class Decision_Tree:
    def __init__(self, min_samples=2, max_depth=10, n_features=None):
        self.min_samples = min_samples
        self.max_depth = max_depth
        self.n_features = n_features
        self.root = None

    def fit(self, X, y):
        self.n_features = X.shape[1] if self.n_features is None else min(X.shape[1], self.n_features)
        self.root = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_feats = X.shape
        n_labels = len(np.unique(y))

        if n_samples == 0:
            return Node(value=100)

        if n_labels == 1 or n_samples <= self.min_samples or depth >= self.max_depth:
            label_value = self._most_common_label(y)
            return Node(value=label_value)

        feat_idxs = np.random.choice(n_feats, self.n_features, replace=False)
        best_feature, best_thresh, left_idxs, right_idxs = self._best_split(X, y, feat_idxs)
        left = self._grow_tree(X[left_idxs, :], y[left_idxs], depth + 1)
        right = self._grow_tree(X[right_idxs, :], y[right_idxs], depth + 1)
        return Node(best_feature, best_thresh, left, right)

    def _best_split(self, X, y, feat_idxs):
        best_gini = 1
        best_feature, best_thresh = None, None
        size = 10
        for feat_idx in feat_idxs:
            X_column = X[:, feat_idx]
            idx_sorted = np.argsort(X_column)

            X_column_sorted = X_column[idx_sorted]
            y_sorted = y[idx_sorted]

            X_bin = self._chunk(X_column_sorted, size)
            X_mean = self._calculate_mean(X_bin)
            y_bin = self._chunk(y_sorted, size)
            y_gini = self._gini(y_bin)

            index_bin = self._chunk(idx_sorted, size)
            gini = np.min(y_gini)

            if gini < best_gini:
                best_gini = gini
                best_thresh = X_mean[np.argmin(y_gini)]
                best_feature = feat_idx
                left_index_bin = np.where(np.array(y_gini) <= best_gini)[0].tolist()
                right_index_bin = np.where(np.array(y_gini) > best_gini)[0].tolist()

                left_indexs, right_indexs = self._index(left_index_bin, right_index_bin, index_bin)
        return best_feature, best_thresh, left_indexs, right_indexs

    def _index(self, left_index_bin, right_index_bin, index_bin):
        left_indexs = [item for i in left_index_bin for item in index_bin[i]]
        right_indexs = [item for i in right_index_bin for item in index_bin[i]]
        return left_indexs, right_indexs

    def _gini(self, arrs):
        gini_bin = []

        for arr in arrs:
            hist = np.bincount(arr)
            total_samples = len(arr)
            gini = 1.0
            for count in hist:
                if count > 0:
                    prob = count / total_samples
                    gini -= math.pow(prob, 2)
            gini_bin.append(gini)
        return gini_bin

    def _calculate_mean(self, arrs):
        avg = [np.mean(arr) for arr in arrs]
        return avg

    def _chunk(self, arr, size):
        bin = [arr[i:i + size] for i in range(0, len(arr), size)]
        return bin

    def _most_common_label(self, y):
        counts = Counter(y)
        max_count = max(counts, key=counts.get)
        return max_count

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])

    def _traverse_tree(self, x, node):
        if node.is_leaf():
            return node.value

        if x[node.feature] <= node.thresh:
            return self._traverse_tree(x, node.leaf)
        return self._traverse_tree(x, node.right)


