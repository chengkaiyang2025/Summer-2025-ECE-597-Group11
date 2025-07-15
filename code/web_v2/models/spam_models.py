import logging
import os
import uuid

import joblib
import pandas as pd
import shap
import numpy as np
from matplotlib import pyplot as plt

from models.util.data_util import get_feature_from_body, predict, PredictResult
from settings_v2 import get_pkl_path, VERSION, BAYES_VERSION, get_image_path


class PredictModel:
    def predict_email(self, spam_content,subject) -> PredictResult:
        raise NotImplementedError()
class PredictLogisticRegression_Version2(PredictModel):
    def __init__(self):
        self.model = joblib.load(os.path.join(get_pkl_path(), f'model_tfidf_lr.pkl'))
        self.vectorizer = joblib.load(os.path.join(get_pkl_path(), f'tfidf_vectorizer_lr.pkl'))
    def __explain_result(self,X_input,image_path) -> list:
        explain_sentences = list()
        # SHAP explanation
        explainer = shap.LinearExplainer(self.model,
                                         self.vectorizer.transform(self.vectorizer.get_feature_names_out()),
                                         feature_perturbation="interventional")
        shap_values = explainer.shap_values(X_input)

        # Get feature names and shap values
        feature_names = self.vectorizer.get_feature_names_out()
        dense_input = X_input.toarray()[0]
        indices = np.where(dense_input != 0)[0]
        tokens = feature_names[indices]
        shap_vals = shap_values[0][indices]

        # explain_sentences.append top contributing tokens
        explain_sentences.append("📝 SHAP Explanation Summary:")
        positive_words = []
        negative_words = []

        for word, val in sorted(zip(tokens, shap_vals), key=lambda x: -abs(x[1])):
            if val > 0:
                positive_words.append(f'"{word}"')
            elif val < 0:
                negative_words.append(f'"{word}"')
        if positive_words:
            explain_sentences.append(" - The following words contributed to predicting this email as **phishing**:")
            explain_sentences.append("`"  + ", ".join(positive_words[:10])+"... `" )

        if negative_words:
            explain_sentences.append(" - The following words pushed the model toward predicting **legitimate**:")
            explain_sentences.append("`" + ", ".join(negative_words[:10])+"... `" )

        explain_sentences.append("- 📊 The chart below shows the top contributing words ranked by their SHAP values,"
                                 "with red bars indicating words pushing the prediction toward **phishing**,"
                                 "and blue bars indicating words supporting **legitimate**.")
        plt.figure()  # 显式创建新图，否则可能出错
        shap.plots.bar(shap.Explanation(values=shap_vals, feature_names=tokens), max_display=10,
                       show=False)  # 关键：show=False 不自动弹出图
        plt.savefig(image_path,                    bbox_inches="tight")  # 保存到磁盘
        plt.close()  # 关闭图，防止 Streamlit 或 Jupyter 出现重叠图

        return explain_sentences
        pass
    def predict_email(self, spam_content,subject) -> PredictResult:
        email_text = subject + " " + spam_content

        X_input = self.vectorizer.transform([email_text])
        prediction = self.model.predict(X_input)
        confidence = self.model.predict_proba(X_input)
        logging.info(f"The label is {prediction[0]}, the confidence is  {confidence[0][1]}")

        image_path = os.path.join(get_image_path(),f"shap_bar_plot_{str(uuid.uuid4())}.png")
        explain_info = self.__explain_result(X_input,image_path)
        predict_result =  PredictResult(
            predicted_label=prediction[0],
            confidence=confidence[0][1],
            explain_info=explain_info,
        )
        predict_result.set_image_path(image_path)
        return predict_result
class PredictNaiveBayes(PredictModel):
    def __init__(self):

        # Load model and vectorizer
        self.nb = joblib.load(os.path.join(get_pkl_path(), f'naive_bayes_model_final_bow.pkl'))
        self.vectorizer = joblib.load(os.path.join(get_pkl_path(), f'bow_vectorizer_final.pkl'))
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


