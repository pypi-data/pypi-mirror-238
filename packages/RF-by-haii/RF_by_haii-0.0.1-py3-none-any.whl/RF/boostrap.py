from decision_tree import Decision_Tree
import numpy as np
from collections import Counter 

class RandomForest:
    def __init__(self, n_estimators=10, max_depth=10, min_samples=2, max_features=None):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.max_features = max_features
        self.trees = []
    
    def fit(self, X, y):
        for _ in range(self.n_estimators):
            tree = Decision_Tree(min_samples=self.min_samples, max_depth=self.max_depth, n_features=self.max_features)
            
            X_sample, y_sample = self._bootstrap_samples(X, y)
            
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)
            
    def _bootstrap_samples(self, X, y):
        n_samples = X.shape[0]
        idxs = np.random.choice(n_samples, n_samples, replace=True)
        return X[idxs], y[idxs]
    
    def _most_common_label(self, y):
        counter = Counter(y)
        leaf_value = counter.most_common(1)[0][0]
        return leaf_value
    
    def predict(self, X):
        predictions = [tree.predict(X) for tree in self.trees]
        return predictions
    
    def score(self, X, y):
        tree_preds = np.array(self.predict(X))
        tree_preds = np.swapaxes(tree_preds, 0, 1)
        final_predictions = [self._most_common_label(pred) for pred in tree_preds]
        accuracy = np.mean(final_predictions == y)
        return accuracy
