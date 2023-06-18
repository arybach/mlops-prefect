from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

def lr_fit_check(df, categorical, numerical, target='duration'):
    # fit linear regression model and output mean squared error
    train_dicts = df[categorical + numerical].to_dict(orient='records')

    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)

    dimensionality = X_train.shape[1]
    print("Dimensionality:", dimensionality)
    
    y_train = df[target].values

    lr = LinearRegression()
    lr.fit(X_train, y_train)

    y_pred = lr.predict(X_train)

    return y_pred, y_train, mean_squared_error(y_train, y_pred, squared=False), dv, lr