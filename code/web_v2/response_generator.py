import logging
from enum import Enum

from models.spam_models import PredictLogisticRegression, PredictNaiveBayes, PredictLogisticRegression_Version2, \
    PredictRandomForrest
from models.util.data_util import PredictResult

#
MODEL_LR = '📈Logistic Regression'
MODEL_NB = '🎲Naive Bayes'
MODEL_SVM = '🛰️SVM'
MODEL_RF = '🌳Random Forest'

#
MODEL_CHOICES = [MODEL_LR, MODEL_NB,

                 # MODEL_SVM,
                 MODEL_RF]
AUTHOR_INFO = {

    MODEL_LR: [
        f"""
        For more details about **[{MODEL_LR}](https://github.com/chengkaiyang2025/Summer-2025-ECE-597-Group11/issues/22)**,  
        please click [here](https://github.com/chengkaiyang2025/Summer-2025-ECE-597-Group11/issues/10).
        """,
    ],
    MODEL_NB: [
        f"""
        For more details about **{MODEL_NB}** please click [here](https://github.com/chengkaiyang2025/Summer-2025-ECE-597-Group11/issues/18).
        """
    ]


}

class ResponseMessage:
    def __init__(self,md_content_list:list,image_path:str = None):
        self.md_content_list = md_content_list
        self.image_path = image_path
class ResponseService:

    def __init__(self):
        self.p_rl_v2 = PredictLogisticRegression_Version2()
        self.p_nb = PredictNaiveBayes()
        self.p_rr = PredictRandomForrest()
        logging.info("Init ResponseService successfully")
    def response(self,model_selected:str, email_subject:str, email_body:str) -> ResponseMessage:
        if model_selected == MODEL_LR:
            assistant_response: PredictResult = self.p_rl_v2.predict_email(email_body, email_subject)
        elif model_selected == MODEL_NB:
            assistant_response: PredictResult = self.p_nb.predict_email(email_body, email_subject)
        elif model_selected == MODEL_RF:
            assistant_response: PredictResult = self.p_rr.predict_email(email_body, email_subject)
        else:
            return ResponseMessage(["Sorry the mad group 11 is still working on this model"])

        # md_content_list = assistant_response.conclusion + assistant_response.explain_info + AUTHOR_INFO[model_selected]
        md_content_list = assistant_response.conclusion + assistant_response.explain_info
        return ResponseMessage(md_content_list,assistant_response.get_image_path())

