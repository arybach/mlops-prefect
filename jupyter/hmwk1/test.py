from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

def apply_model(df, categorical, numerical, dv, lr, target='duration'):
    # apply 
    new_dicts = df[categorical + numerical].to_dict(orient='records')
    X_new = dv.transform(new_dicts)
    y_new = df[target].values
    y_pred = lr.predict(X_new)
    mse = mean_squared_error(y_new, y_pred, squared=False)
    return y_pred, y_new, mse