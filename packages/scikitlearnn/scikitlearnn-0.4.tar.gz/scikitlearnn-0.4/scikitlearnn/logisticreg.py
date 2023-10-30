import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def sigmoid(x):
    return 1/(1 + np.exp(-x)) 

class LogisticRegression(): 

    def __init__(self, learning_rate = 0.0001, iterations = 1000): 
        self.learning_rate = learning_rate
        self.iterations = iterations 
        self.weights = None
        self.bias = None

    
    def fit(self, X, Y):
        samples , features = X.shape
        # initialize weights 
        self.weights = np.zeros(features)
        self.bias = 0 

        for _ in range(self.iterations):
            # calculate a1 * x1 + a2 * x2 + .... an * xn + b 
            linear_predictions = np.dot(X, self.weights) + self.bias 
            predictions = sigmoid(linear_predictions)

            # Calculate gradiance 
            dw = (1 / samples) * np.dot(X.T, (predictions - Y)) 
            db = (1 / samples) * np.sum(predictions - Y)

            # Updates  
            self.weights = self.weights - self.learning_rate * dw
            self.bias = self.bias - self.learning_rate * db

    
    def predict(self, X):
        linear_predictions = np.dot(X, self.weights) + self.bias
        y_pred = sigmoid(linear_predictions)
        class_pred = [0 if y <= 0.5 else 1 for y in y_pred]
        return class_pred
        

X = np.array([[2.5,1.5],[3.0,1.0],[4.0,3.0],[1.0,4.0],[2.0,2.0]])
y = np.array([1,1,0,0,1])

model = LogisticRegression(learning_rate=0.01,iterations=1000)
model.fit(X,y)

y_pred = model.predict(X)
print(y_pred)





# **************************************** secind option *********************************************
# Example usage
X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
y_train = np.array([0, 0, 1, 1])

model = LogisticRegression(learning_rate=0.001, iterations=1000)
model.fit(X_train, y_train)

X_test = np.array([[1, 1], [2, 2]])
predictions = model.predict(X_test)
print(predictions)

data = pd.read_csv('./breast_cancer.data', header=None)
y = (data.iloc[:, 1] == 'M').astype(int).values  # Convert 'M' (malignant) to 1 and 'B' (benign) to 0
data.drop(data.iloc[:, 1:2 ], inplace=True, axis=1)  # Remove 2nd column 
X = data


# Split data 
def split_data(X, y, test_size=0.2):
    num_samples = len(X)
    num_test = int(test_size * num_samples)
    X_train, X_test = X[:-num_test], X[-num_test:]
    y_train, y_test = y[:-num_test], y[-num_test:]
    return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test = split_data(X, y)

print('X-train - ')
print(X_train)

print('Y-train - ')
print(y_train)

print('X-test - ')
print(X_test)

print('Y-test - ')
print(y_test)


# Train the logistic regression model
model = LogisticRegression(learning_rate=0.00001, iterations=1000)
model.fit(X_train, y_train)

# Predict on the test set
predictions = model.predict(X_test)

# Calculate accuracy
accuracy = np.sum(predictions == y_test) / len(y_test) * 100
print("Accuracy:", accuracy, "%")


