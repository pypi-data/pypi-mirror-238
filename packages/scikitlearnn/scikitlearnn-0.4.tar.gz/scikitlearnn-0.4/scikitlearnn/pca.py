import numpy as np
from sklearn.decomposition import PCA
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler

# Load the Breast Cancer dataset
data = load_breast_cancer().data

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)
print(scaled_data)

# Create a PCA instance with 2 components
n_components = 2
pca = PCA(n_components=n_components)

# Fit PCA to the scaled data
pca.fit(scaled_data)

# Transform the data to its principal components
transformed_data = pca.transform(scaled_data)


# Explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_
print("Explained Variance Ratio:", explained_variance_ratio)

# Principal components
principal_components = pca.components_
print("Principal Components:", principal_components)