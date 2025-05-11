import pandas as pd
import joblib
import os
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from zenml import step

@step
def train_model(df: pd.DataFrame) -> str:
    if len(df) < 1000:
        raise ValueError("Training dataset too small (< 1000 rows). Aborting model training.")

    X = df[['LeadTime', 'ADR']]
    y = df['IsCanceled']
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)

    with mlflow.start_run():
        model.fit(X_train, y_train)
        model_path = "model.joblib"
        joblib.dump(model, model_path)
        mlflow.log_artifact(model_path)
        mlflow.sklearn.log_model(model, "sk_model")

    return os.path.abspath(model_path)
