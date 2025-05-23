import logging

import emoji
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

from models.check_result import DumbCheckResult, Jinji2Response, HuggingFaceModelResult1, LogisticRegressionResult
from models.spam_logistic_regression import PredictLogisticRegression
from settings import HUGGING_FACE_MODEL_1_PATH

logger = logging.getLogger(__name__)


class EmailProcessTemplate:
    def process(self, body:str, subject:str) -> Jinji2Response:
        pass

class HuggingFaceModelProcess(EmailProcessTemplate):
    model_name = "some hugging face model"
    model = None
    def __init__(self):
        logger.info("")
        pass
    def process(self, body:str, subject:str) -> Jinji2Response:
        pass

class HuggingFaceModelProcess_1(HuggingFaceModelProcess):
    model_name = "dima806/email-spam-detection-roberta"
    model_path = HUGGING_FACE_MODEL_1_PATH

    def __init__(self):
        super().__init__()
        logger.info(f"Start to initialize {self.model_name} successfully.")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        logger.info(f"Initialize {self.model_name} successfully.")
    def process(self, body:str, subject:str) -> Jinji2Response:
        response = self.__process_content(content=subject+""+body)
        return response

    def __process_content(self,content):
        inputs = self.tokenizer(content, return_tensors="pt", truncation=True, max_length=512, padding=True)

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = F.softmax(logits, dim=-1)

        labels = ["ham", "spam"]
        predicted_label = labels[probs.argmax()]
        confidence = probs.max().item()
        response = HuggingFaceModelResult1(predicted_label,confidence)
        return response

class DumbEmailProcessTemplate(EmailProcessTemplate):

    def __dumb_process__(self,body:str, subject:str):
        """
        Process the email and return the result.
        """
        c = DumbCheckResult()

        c.subject_length = len(subject)
        c.body_length = len(body)
        c.number_of_url = body.count("http://") + body.count("https://")

        b = body.split(" ")
        for word in b:
            if word in c.suspicious_words_set:
                c.suspicious_words.append(word)
            if word in c.sentiment_terms_set:
                c.sentiment_terms.append(word)
            if len(word) > 1 and  word.isupper():
                c.punctuation_marks.append(word)
        c.emoji_count = emoji.emoji_count(body) + emoji.emoji_count(subject)
        return c

    def process(self, body:str, subject:str) -> Jinji2Response:
        return self.__dumb_process__(body,subject)

class LogisticRegressionProcess(EmailProcessTemplate):
    model_name = "logistic-regression"
    def __init__(self):
        super().__init__()
        self.p = PredictLogisticRegression()
    pass

    def process(self, body:str, subject:str) -> Jinji2Response:
        result = self.p.predict_with_logistic_regression(body,subject)
        predicted_label = result['prediction'].values[0]
        confidence = result['probability'].values[0]
        response = LogisticRegressionResult(predicted_label,confidence)

        return response

