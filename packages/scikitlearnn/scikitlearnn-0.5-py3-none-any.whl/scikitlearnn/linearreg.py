import matplotlib.pyplot as plt
import numpy as np
import math


x = [151, 174, 138, 186, 128, 136, 179, 163, 152, 131, 100, 69, 21]
y = [63, 81, 56, 91, 47, 57, 76, 72, 62, 48, 49, 37, 11]

plt.scatter(x, y)
plt.show()


mean_x = np.mean(x)
mean_y = np.mean(y)
print(f"mean_x = {mean_x} , mean_y = {mean_y}")

l=len(x)
numerator=0
denominator=0
for i in range(l):
  numerator += (x[i] - mean_x) * (y[i] - mean_y)
  denominator += (x[i] - mean_x) **2
m = numerator / denominator
c = mean_y - (m * mean_x)
print(f"m = {m} , c = {c}")

max_x = np.max(x) + 100
min_x = np.min(y) - 100
X = np.linspace(min_x,max_x,100)
Y = c + m*X

plt.plot(X, Y, color='green', label = 'Regression Line')
plt.scatter(x, y, c = 'red', label = 'data')
plt.xlabel('Height')
plt.ylabel('Weight')
plt.legend()
plt.show()