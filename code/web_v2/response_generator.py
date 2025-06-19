import logging
from enum import Enum

from models.spam_models import PredictLogisticRegression, PredictNaiveBayes
from models.util.data_util import PredictResult

#
MODEL_LR = '📈Logistic Regression'
MODEL_NB = '🎲Naive Bayes'
MODEL_SVM = '🛰️SVM'
MODEL_RF = '🌳Random Forest'

#
MODEL_CHOICES = [MODEL_LR, MODEL_NB, MODEL_SVM, MODEL_RF]
AUTHOR_INFO = {

    MODEL_LR: [
        f"""
        The **[{MODEL_LR}](https://github.com/chengkaiyang2025/Summer-2025-ECE-597-Group11/issues/22)**  is trained by [Kai](https://www.linkedin.com/in/chengkai-yang-61b1a4253/). 
        For more details please click [here](https://github.com/chengkaiyang2025/Summer-2025-ECE-597-Group11/issues/10).
        """,
    ],
    MODEL_NB: [
        f"""
        The **{MODEL_NB}** is trained by Charina. 
        For more details please click [here](https://github.com/chengkaiyang2025/Summer-2025-ECE-597-Group11/issues/18).
        """
    ]


}
class ResponseService:

    def __init__(self):
        self.p1 = PredictLogisticRegression()
        self.p_nb = PredictNaiveBayes()
        logging.info("Init ResponseService successfully")
    def predict(self,model_selected:str, email_subject:str, email_body:str) -> list:
        if model_selected == MODEL_LR:
            assistant_response: PredictResult = self.p1.predict_email(email_body, email_subject)
        elif model_selected == MODEL_NB:
            assistant_response: PredictResult = self.p_nb.predict_email(email_body, email_subject)
        else:
            return ["Sorry the mad group 11 is still working on this model"]

        md_content_list = assistant_response.conclusion + assistant_response.explain_info + AUTHOR_INFO[model_selected]

        return md_content_list
