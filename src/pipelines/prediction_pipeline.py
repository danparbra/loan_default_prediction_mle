import os
import sys
from dataclasses import dataclass
import pandas as pd
from src.exception import CustomException
from src.utils import load_object


class PredictPipeline:
    def __init__(self) -> None:
        model_path = os.path.join("artifacts", "models", "model.pkl")
        preprocessor_path = os.path.join("artifacts", "models", "preprocessor.pkl")
        self.model = load_object(file_path=model_path)
        self.preprocessor = load_object(file_path=preprocessor_path)

    def predict(self, features: pd.DataFrame) -> list:
        try:
            data_scaled = self.preprocessor.transform(features)
            preds = self.model.predict(data_scaled)
            return preds

        except Exception as e:
            raise CustomException(e, sys)


@dataclass
class CustomData:
    Credit_Score: float
    Loan_Duration_Years: int
    Loan_Amount: float
    Age: float
    Had_Past_Default: int
    Annual_Income: float
    Number_of_Open_Accounts: float
