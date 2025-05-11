import pandas as pd
import joblib
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from zenml import step

@step
def validate_model(df: pd.DataFrame, model_path: str) -> None:
    X = df[['LeadTime', 'ADR']]
    y = df['IsCanceled']
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = joblib.load(model_path)
    preds = model.predict(X_test)
    score = f1_score(y_test, preds)

    print(f"F1 Score: {score:.2f}")
    if score < 0.6:
        print("Warning: Model performance below expected threshold (0.6).")
