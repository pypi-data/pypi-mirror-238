# importing libraries 
import numpy as np 
import pandas as pd
import matplotlib as plt 

# dataset read 
data = pd.read_csv('data.csv')
df = pd.DataFrame(data)
df

# 1. Imputation :- This code will replace missing 'Salary' values with the mean of the available 'Salary' values.
# Perform mean imputation for the 'Salary' column
mean_salary = df['Salary'].mean()
mean_age = df['Age'].mean()
df['Salary'].fillna(mean_salary, inplace=True)
df['Age'].fillna(mean_age, inplace=True)
df

# set decimal precision to 2
df['Salary'] = df['Salary'].round(2)
df['Age'] = (df['Age']).astype(int)
df

# 2. Anomaly Detection - 
# We calculate the z-scores for the 'Age' and 'Salary' columns using the formula: (x - mean) / standard_deviation, where x is the value of the data point, mean is the mean of the column, and standard_deviation is the standard deviation of the column.
# We add two new columns, 'Age_ZScore' and 'Salary_ZScore', to the DataFrame to store the calculated z-scores.
# Now, the DataFrame df contains the original data along with the z-scores for the 'Age' and 'Salary' columns, which indicate how many standard deviations each data point is away from the mean in their respective columns.
new_data = {
    'Country': 'pakistan',
    'Age': 140,
    'Salary': 1000000,
    'Purchased': 'No',
}
df = df.append(new_data, ignore_index=True)
df1 =df.copy()

# # Calculate the z-scores for the 'Age' and 'Salary' columns
df1['Age_ZScore'] = (df['Age'] - df['Age'].mean()) / df['Age'].std(ddof=0)
df1['Salary_ZScore'] = (df['Salary'] - df['Salary'].mean()) / df['Salary'].std(ddof=0)
df1

# Find the tuples with the maximum absolute z-score values
max_abs_age_zscore = df1['Age_ZScore'].abs().max()
max_abs_salary_zscore = df1['Salary_ZScore'].abs().max()

# Filter the DataFrame to include only the tuples with maximum absolute z-score values
max_abs_age_tuples = df1[df1['Age_ZScore'].abs() == max_abs_age_zscore]
max_abs_salary_tuples = df1[df1['Salary_ZScore'].abs() == max_abs_salary_zscore]

max_abs_age_tuples


# 3. Standardization 
# Standardization, also known as z-score normalization or feature scaling, is a data preprocessing technique used to transform the data in a way that it has a mean of 0 and a standard deviation of 1. This process is applied to numerical features in a dataset and is particularly useful when you have features with different units or scales.

# The formula for standardization (z-score) of a data point x is:
# z = (x - μ) / σ
# # Calculate the z-scores for the 'Age' and 'Salary' columns
df2 = df.copy()
df2['Age'] = (df['Age'] - df['Age'].mean()) / df['Age'].std(ddof=0)
df2['Salary'] = (df['Salary'] - df['Salary'].mean()) / df['Salary'].std(ddof=0)
df2


# 4. Normalization
# Normalize 'Age' and 'Salary' columns using Min-Max scaling
df3 = df.copy()
df3['Age'] = (df['Age'] - df['Age'].min()) / (df['Age'].max() - df['Age'].min())
df3['Salary'] = (df['Salary'] - df['Salary'].min()) / (df['Salary'].max() - df['Salary'].min())
df3


# Encoding
df_encoded = pd.get_dummies(df, columns=['Country', 'Purchased'], drop_first=True)
df_encoded