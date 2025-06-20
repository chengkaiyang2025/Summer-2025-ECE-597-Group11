import logging
import os
import joblib
import pandas as pd

from models.util.data_util import get_feature_from_body, predict, PredictResult
from settings_v2 import get_pkl_path, VERSION, BAYES_VERSION


class PredictModel:
    def predict_email(self, spam_content,subject) -> PredictResult:
        raise NotImplementedError()

class PredictNaiveBayes(PredictModel):
    def __init__(self):

        # Load model and vectorizer
        self.nb = joblib.load(os.path.join(get_pkl_path(), f'naive_bayes_model_{BAYES_VERSION}.pkl'))
        self.vectorizer = joblib.load(os.path.join(get_pkl_path(), f'tfidf_vectorizer_{BAYES_VERSION}.pkl'))
    def predict_email(self, spam_content,subject) -> PredictResult:
        email_text = subject + " " + spam_content

        # Transform and predict
        X_input = self.vectorizer.transform([email_text])
        prediction = self.nb.predict(X_input)
        confidence = self.nb.predict_proba(X_input)
        logging.info(f"The label is {prediction[0]}, the confidence is  {confidence[0][1]}")
        return PredictResult(
            predicted_label=prediction[0],
            confidence=confidence[0][1],
            explain_info=[
                "We are still working on explainable ai to explain the model result.",

            ]
        )
class PredictLogisticRegression(PredictModel):

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

    def predict_email(self, spam_content,subject) -> PredictResult:
        input_pd = pd.DataFrame([
            {
                'body': spam_content,
                'subject': subject,
            }
        ])


        predict_result =  predict(input_pd, self.model, self.scaler, self.features)
        logging.info(f"predict_result: {predict_result}")
        return predict_result


