import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

cancer = datasets.load_breast_cancer()
X = cancer.data
y = cancer.target
print(X)
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ek SVM classifier banayein
svm_rbf10_classifier = SVC(kernel='rbf', C=10, gamma="auto")
# Model ko training data par train karein
svm_rbf10_classifier.fit(X_train, y_train)

# Testing data par predictions banayein
y_pred = svm_rbf10_classifier.predict(X_test)

# Accuracy calculate karein
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Classification report aur confusion matrix print karein
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ********************************************************************************************************************************************
# Ek SVM classifier banayein
svm_rbf100_classifier = SVC(kernel='rbf', C=100, gamma="auto")
# Model ko training data par train karein
svm_rbf100_classifier.fit(X_train, y_train)

# Testing data par predictions banayein
y_pred = svm_rbf100_classifier.predict(X_test)

# Accuracy calculate karein
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Classification report aur confusion matrix print karein
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))












# Ek SVM classifier banayein
svm_linear10_classifier = SVC(kernel='linear', C=10)
# Model ko training data par train karein
svm_linear10_classifier.fit(X_train, y_train)

# Testing data par predictions banayein
y_pred = svm_linear10_classifier.predict(X_test)

# Accuracy calculate karein
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Classification report aur confusion matrix print karein
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ********************************************************************************************************************************************
# Ek SVM classifier banayein
svm_linear100_classifier = SVC(kernel='linear', C=100)
# Model ko training data par train karein
svm_linear100_classifier.fit(X_train, y_train)

# Testing data par predictions banayein
y_pred = svm_linear100_classifier.predict(X_test)

# Accuracy calculate karein
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Classification report aur confusion matrix print karein
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))







# Ek SVM classifier banayein
svm_poly10_classifier = SVC(kernel='poly', C=10)
# Model ko training data par train karein
svm_poly10_classifier.fit(X_train, y_train)

# Testing data par predictions banayein
y_pred = svm_poly10_classifier.predict(X_test)

# Accuracy calculate karein
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Classification report aur confusion matrix print karein
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ********************************************************************************************************************************************
# Ek SVM classifier banayein
svm_poly100_classifier = SVC(kernel='poly', C=100)
# Model ko training data par train karein
svm_poly100_classifier.fit(X_train, y_train)

# Testing data par predictions banayein
y_pred = svm_poly100_classifier.predict(X_test)

# Accuracy calculate karein
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Classification report aur confusion matrix print karein
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))