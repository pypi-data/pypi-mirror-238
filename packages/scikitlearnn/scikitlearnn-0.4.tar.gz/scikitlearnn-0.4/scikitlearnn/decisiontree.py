import numpy as np 
import pandas as pd

import numpy as np

class TreeNode:
    def __init__(self, gini, num_samples, num_samples_per_class, predicted_class):
        self.gini = gini
        self.num_samples = num_samples
        self.num_samples_per_class = num_samples_per_class
        self.predicted_class = predicted_class
        self.feature_index = 0
        self.threshold = 0
        self.left = None
        self.right = None

class DecisionTreeClassifier:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth

    def fit(self, X, y):
        self.num_classes = len(np.unique(y))
        self.num_features = X.shape[1]
        self.tree = self._grow_tree(X, y)

    def _gini(self, y):
        m = len(y)
        return 1.0 - sum((np.sum(y == c) / m) ** 2 for c in range(self.num_classes))

    def _best_split(self, X, y):
        m, n = X.shape
        if m <= 1:
            return None, None

        num_parent = [np.sum(y == c) for c in range(self.num_classes)]
        best_gini = 1.0 - sum((num / m) ** 2 for num in num_parent)
        best_idx, best_thr = None, None

        for idx in range(self.num_features):
            thresholds, classes = zip(*sorted(zip(X[:, idx], y)))
            num_left = [0] * self.num_classes
            num_right = num_parent.copy()

            for i in range(1, m):
                c = classes[i - 1]
                num_left[c] += 1
                num_right[c] -= 1
                gini_left = 1.0 - sum((num_left[x] / i) ** 2 for x in range(self.num_classes))
                gini_right = 1.0 - sum((num_right[x] / (m - i)) ** 2 for x in range(self.num_classes))
                gini = (i * gini_left + (m - i) * gini_right) / m

                if thresholds[i] == thresholds[i - 1]:
                    continue

                if gini < best_gini:
                    best_gini = gini
                    best_idx = idx
                    best_thr = (thresholds[i] + thresholds[i - 1]) / 2

        return best_idx, best_thr

    def _grow_tree(self, X, y, depth=0):
        num_samples_per_class = [np.sum(y == i) for i in range(self.num_classes)]
        predicted_class = np.argmax(num_samples_per_class)
        node = TreeNode(
            gini=self._gini(y),
            num_samples=len(y),
            num_samples_per_class=num_samples_per_class,
            predicted_class=predicted_class,
        )

        if depth < self.max_depth:
            idx, thr = self._best_split(X, y)
            if idx is not None:
                indices_left = X[:, idx] < thr
                X_left, y_left = X[indices_left], y[indices_left]
                X_right, y_right = X[~indices_left], y[~indices_left]
                node.feature_index = idx
                node.threshold = thr
                node.left = self._grow_tree(X_left, y_left, depth + 1)
                node.right = self._grow_tree(X_right, y_right, depth + 1)
        return node

    def predict(self, X):
        return [self._predict_tree(x, self.tree) for x in X]

    def _predict_tree(self, x, tree):
        if tree.left is None and tree.right is None:
            return tree.predicted_class
        if x[tree.feature_index] < tree.threshold:
            return self._predict_tree(x, tree.left)
        else:
            return self._predict_tree(x, tree.right)



# Load the dataset
data = pd.read_csv('./salaries.csv')  # Replace with the actual dataset filename

# Define custom mapping dictionaries for each categorical column
company_mapping = {'google': 0, 'facebook': 1, 'abc pharma': 2}
job_mapping = {'sales executive': 0, 'business manager': 1, 'computer programmer': 2}
degree_mapping = {'bachelors': 0, 'masters': 1}

# Apply custom mapping to each categorical column
data['company'] = data['company'].map(company_mapping)
data['job'] = data['job'].map(job_mapping)
data['degree'] = data['degree'].map(degree_mapping)

print(data)
# Separate features (X) and target (y)
X = data.drop('salary_more_then_100k', axis=1)
y = data['salary_more_then_100k']


X.head()

y.head()

# Create and train the DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth=3)
clf.fit(X.values, y)

new_data = pd.DataFrame({
    'company': ['google', 'facebook','abc pharma'],
    'job': ['sales executive', 'computer programmer','computer programmer'],
    'degree': ['bachelors', 'masters','bachelors']
})

new_data_encoded = new_data.copy()
new_data_encoded['company'] = new_data['company'].map(company_mapping)
new_data_encoded['job'] = new_data['job'].map(job_mapping)
new_data_encoded['degree'] = new_data['degree'].map(degree_mapping)

print(new_data_encoded)
# Predict for the new data
if 'new_data_encoded' in locals():
    predictions = clf.predict(new_data_encoded.values)
    for i, pred in enumerate(predictions):
        company = new_data['company'][i]
        job = new_data['job'][i]
        degree = new_data['degree'][i]
        salary_prediction = "Yes" if pred == 1 else "No"
        print(f"For {degree} degree holder in {job} role at {company}, predicted salary more than $100k: {salary_prediction}")

