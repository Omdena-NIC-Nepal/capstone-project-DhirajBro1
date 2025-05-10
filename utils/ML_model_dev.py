# ML_model_dev.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, mean_absolute_error, classification_report, r2_score

# ---------------------- Classification Models ----------------------

def random_forest_classification(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Random Forest Classification Report:")
    print(classification_report(y_test, y_pred))
    return model

def svm_classification(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = SVC(kernel='rbf', random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Support Vector Machine Classification Report:")
    print(classification_report(y_test, y_pred))
    return model

def gradient_boosting_classification(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GradientBoostingClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Gradient Boosting Classification Report:")
    print(classification_report(y_test, y_pred))
    return model

# ---------------------- Regression Models ----------------------

def multiple_linear_regression(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    evaluate_regression(y_test, y_pred, "Multiple Linear Regression")
    return model

def ridge_regression(X, y, alpha=1.0):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    evaluate_regression(y_test, y_pred, "Ridge Regression")
    return model

def lasso_regression(X, y, alpha=0.1):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = Lasso(alpha=alpha)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    evaluate_regression(y_test, y_pred, "Lasso Regression")
    return model

def gradient_boosting_regression(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GradientBoostingRegressor(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    evaluate_regression(y_test, y_pred, "Gradient Boosting Regression")
    return model

# ---------------------- Model Evaluation Helpers ----------------------

def evaluate_regression(y_true, y_pred, model_name="Model"):
    print(f"\n{model_name} Evaluation:")
    print("RMSE:", np.sqrt(mean_squared_error(y_true, y_pred)))
    print("MAE:", mean_absolute_error(y_true, y_pred))
    print("R2 Score:", r2_score(y_true, y_pred))

def cross_validate_model(model, X, y, cv=5):
    scores = cross_val_score(model, X, y, cv=cv)
    print(f"Cross-validation scores ({cv}-fold):", scores)
    print("Average cross-validation score:", np.mean(scores))
