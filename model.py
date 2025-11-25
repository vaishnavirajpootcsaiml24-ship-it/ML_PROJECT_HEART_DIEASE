import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from sklearn.metrics import accuracy_score, f1_score
import pickle

def train_model():
    print("Loading Dataset...")

   
    data = pd.read_csv("C:\\Users\\vaish\\OneDrive\\Desktop\\mlproject2\\archive (5)\\framingham.csv")

   
    data = data.fillna(data.median())

  
    y = data["TenYearCHD"]

    
    X = data.select_dtypes(include=[np.number]).drop(columns=["TenYearCHD"])

    print("\nFeatures used for training:")
    print(list(X.columns))

    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )


    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    
    model = xgb.XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss"
    )

    model.fit(X_train_scaled, y_train)


    y_pred = model.predict(X_test_scaled)

    
    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("F1 Score:", f1_score(y_test, y_pred))

   
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)


    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print("\nTraining complete! model.pkl and scaler.pkl saved successfully.")

if __name__ == "__main__":
    train_model()
