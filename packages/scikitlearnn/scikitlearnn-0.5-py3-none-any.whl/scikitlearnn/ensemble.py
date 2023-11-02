import pandas as pd

df = pd.read_csv('boston.csv')
df

print("shape of the dataset: ", df.shape)

print("Column names: " ,df.columns)

print("Summary of the dataset")
print(df.info())
print()
print(df.describe())

df.fillna(df.mean(), inplace=True)


from sklearn.model_selection import train_test_split
X = df.drop(columns=['medv'])
y = df['medv']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import Lasso,Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

#Stacking

base_models = [('lasso', Lasso()),('ridge',Ridge()),('knn',KNeighborsRegressor()),('svr',SVR()),
               ('dt',DecisionTreeRegressor())]
meta_model = Ridge()
stacking_regressor = StackingRegressor(estimators=base_models,final_estimator=meta_model)
stacking_regressor.fit(X_train,y_train)

y_train_pred = stacking_regressor.predict(X_train)
y_test_pred = stacking_regressor.predict(X_test)


from sklearn.ensemble import RandomForestRegressor

#bagging

random_forest_regressor = RandomForestRegressor(n_estimators=10,random_state=42)
random_forest_regressor.fit(X_train,y_train)

y_train_pred_rf = random_forest_regressor.predict(X_train)
y_test_pred_rf = random_forest_regressor.predict(X_test)


import xgboost as xgb

#boosting
xgb_regressor = xgb.XGBRegressor(n_estimators=10,random_state=42)
xgb_regressor.fit(X_train,y_train)

y_train_pred_xgb = xgb_regressor.predict(X_train)
y_test_pred_xgb= xgb_regressor.predict(X_test)


from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

def mape(y_true,y_pred):
    return np.mean(np.abs((y_true-y_pred)/y_true)) * 100

rmse_stacking_train = np.sqrt(mean_squared_error(y_train,y_train_pred))
mape_stacking_train = mape(y_train,y_train_pred)
rmse_stacking_test = np.sqrt(mean_squared_error(y_test,y_test_pred))
mape_stacking_test = mape(y_test,y_test_pred)

rmse_rf_train = np.sqrt(mean_squared_error(y_train,y_train_pred_rf))
mape_rf_train = mape(y_train,y_train_pred_rf)
rmse_rf_test = np.sqrt(mean_squared_error(y_test,y_test_pred_rf))
mape_rf_test = mape(y_test,y_test_pred_rf)

rmse_boosting_train = np.sqrt(mean_squared_error(y_train,y_train_pred_xgb))
mape_boosting_train = mape(y_train,y_train_pred_xgb)
rmse_boosting_test = np.sqrt(mean_squared_error(y_test,y_test_pred_xgb))
mape_boosting_test = mape(y_test,y_test_pred_xgb)