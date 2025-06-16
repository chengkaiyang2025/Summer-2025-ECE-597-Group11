import logging
import os
import joblib
import pandas as pd

from models.util.data_util import get_feature_from_body, predict, PredictResult
from settings_v2 import get_pkl_path,VERSION


class PredictLogisticRegression:

    def __init__(self):
        model_pkl = os.path.join(get_pkl_path(), f'spam_classifier_model_{VERSION}.pkl')
        scalar_pkl = os.path.join(get_pkl_path(), f'spam_scaler_{VERSION}.pkl')
        feature_txt = os.path.join(get_pkl_path(), f'spam_feature_{VERSION}.txt')

        model_test = joblib.load(model_pkl)
        scaler_test = joblib.load(scalar_pkl)
        with open(feature_txt, 'r') as f:
            feature_loaded = [line.strip() for line in f]

        self.model = model_test
        self.scaler = scaler_test
        self.features = feature_loaded

    def predict_with_logistic_regression(self, spam_content,subject) -> PredictResult:
        input_pd = pd.DataFrame([
            {
                'body': spam_content,
                'subject': subject,
            }
        ])


        predict_result =  predict(input_pd, self.model, self.scaler, self.features)
        logging.info(f"predict_result: {predict_result}")
        return predict_result


