from settings import HUGGING_FACE_MODEL_1_PATH


class Jinji2Response:
    type = "BASIC"
class HuggingFaceModelResult(Jinji2Response):
    type = "HuggingFaceModelResult"

class HuggingFaceModelResult1(HuggingFaceModelResult):
    """
    The process result of a spam model on Hugging face:
https://huggingface.co/dima806/email-spam-detection-roberta

    """
    type = "dima806/email-spam-detection-roberta"


    def __init__(self,predicted_label,confidence):
        self.predicted_label = predicted_label
        self.confidence = f"{confidence:.2%}"

    def __str__(self):
        return f"predicted_label: {self.predicted_label}, confidence: {self.confidence}"


class DumbCheckResult(Jinji2Response):
    type = "DumbCheckResult"
    suspicious_words_set = {"verify", "prize", "urgent", "discount", "account", "bank"}
    sentiment_terms_set = {"danger", "hurry", "guarantee", "risk"}

    def     __init__(self):
        self.subject_length = 0
        self.body_length = 0
        self.number_of_url = 0
        self.suspicious_words = []
        self.sentiment_terms = []
        self.punctuation_marks = []
        self.spam_type = ""
        self.emoji_count = 0

    def __str__(self):
        return (
            f"subject_length: {self.subject_length}, "
            f"body_length: {self.body_length}, "
            f"number_of_url: {self.number_of_url}, "
            f"suspicious_words: {self.suspicious_words}, "
            f"sentiment_terms: {self.sentiment_terms}, "
            f"punctuation_marks: {self.punctuation_marks}"
        )
