from analysis.prepare_data_and_feature import predict

from analysis.prepare_data_and_feature import get_feature_from_body
import os
import joblib
import pandas as pd

from models.check_result import LogisticRegressionResult
from settings import PATH_PKL

VERSION = "v1"


class PredictLogisticRegression:

    def __init__(self):
        model_pkl = os.path.join(PATH_PKL, f'spam_classifier_model_{VERSION}.pkl')
        scalar_pkl = os.path.join(PATH_PKL, f'spam_scaler_{VERSION}.pkl')
        feature_txt = os.path.join(PATH_PKL, f'spam_feature_{VERSION}.txt')

        model_test = joblib.load(model_pkl)
        scaler_test = joblib.load(scalar_pkl)
        with open(feature_txt, 'r') as f:
            feature_loaded = [line.strip() for line in f]

        self.model = model_test
        self.scaler = scaler_test
        self.features = feature_loaded

    def predict_with_logistic_regression(self, spam_content,subject):
        input_pd = pd.DataFrame([
            {
                'body': spam_content,
                'subject': subject,
            }
        ])


        feature_vector = get_feature_from_body(input_pd)
        result = predict(feature_vector, self.model, self.scaler, self.features)
        return result[['body','subject','prediction','probability']]

#
# def test_1():
#     spam_head_1 = 'UPDATE'
#     spam_content_1 = 'Notice: This message was sent from outside the University of Victoria email system. Please be cautious with links and sensitive information.\r\n\r\n\r\nHello\r\n\r\nYour Email account will be Deactivated shortly.\r\nTo stop De-activation CLICK HERE<https://edu-it-helpdesk-sys.weebly.com/> and log in\r\n\r\nThanks\r\n\r\n\r\nIT Help Desk\r\n'
#     p = PredictLogisticRegression()
#     result = (p.predict_with_logistic_regression(spam_content_1,spam_head_1))
#     predicted_label = result['prediction'].values[0]
#     confidence = result['probability'].values[0]
#     response = LogisticRegressionResult(predicted_label, confidence)
#     print(response)
# test_1()