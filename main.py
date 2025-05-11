from zenml import pipeline
from steps.data_loader import load_data
from steps.pretraining_tests import run_data_quality_tests
from steps.model_trainer import train_model
from steps.model_validator import validate_model

@pipeline
def hotel_cancellation_pipeline():
    train_df = load_data()
    passed = run_data_quality_tests(train_df)

    if not passed:
        print("Data quality tests failed. Halting pipeline.")
        return

    model_path = train_model(df=train_df)
    validate_model(df=train_df, model_path=model_path)

hotel_cancellation_pipeline()