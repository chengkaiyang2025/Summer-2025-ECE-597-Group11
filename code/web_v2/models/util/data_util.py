import ast
import pandas as pd
import glob
import os



def string_to_multiline(text):
    try:
        lst = ast.literal_eval(text)  # Convert to list
        return '\n'.join([s for s in lst if s.strip()])  # Join non-empty lines
    except Exception as e:
        return ''  # Or handle/log the error as needed


# s = ham_df['text'].head(5)
# ham_df['text_str'] = ham_df['text'].apply(string_to_multiline)
def step_100_get_enron_pd():
    # Set the path where the CSV files are located
    csv_folder = "D:\GITHUB\SpamEmailClassifier\data\cleaned_enron_dataset"  # adjust this if running from a different working dir
    csv_files = glob.glob(os.path.join(csv_folder, "*_5.csv"))

    # Read and concatenate all CSVs into one DataFrame
    enron_pd = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

    # Optional: Preview the result
    print(enron_pd.head())
    enron_pd['body'] = enron_pd['text'].apply(string_to_multiline)
    enron_pd['label'] = 0
    print("Total rows:", len(enron_pd))
    return enron_pd


def step_150_get_spam_dataset():
    df = pd.read_csv('D:\GITHUB\SpamEmailClassifier\data\CaptstoneProjectData_2025.csv')
    # df = df.applymap(lambda x: x.replace('\r', '').replace('\n', '') if isinstance(x, str) else x)
    df.fillna("", inplace=True)
    df['row_id'] = range(len(df))
    df.rename(columns={'Body': 'body', 'Subject': 'subject'}, inplace=True)
    df['label'] = 1

    print(len(df))

    return df


def run_get_dataset():
    spam_df = step_150_get_spam_dataset()
    ham_df = step_100_get_enron_pd()
    ham_df_sample = ham_df.sample(n=len(spam_df), random_state=42)

    df = pd.concat([spam_df[['subject', 'body', 'label']], ham_df_sample[['subject', 'body', 'label']]],
                   ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


import re
import unicodedata

COMMON_PUNCTUATION = set([
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'
])


def detect_suspicious_non_latin(text):
    suspicious_chars = []

    for char in text:
        if char.isascii():
            if char in COMMON_PUNCTUATION or char.isalnum() or char.isspace():
                continue
            else:
                suspicious_chars.append((char, 'Unusual ASCII'))
                continue

        try:
            name = unicodedata.name(char)
            if 'LATIN' not in name:
                suspicious_chars.append((char, name))
        except ValueError:
            suspicious_chars.append((char, 'No Unicode Name'))
    return len(suspicious_chars), len(set(suspicious_chars))


SPAM_WORDS = {
    "account", "rbc", "helpdesk", "password", "urgent"
                                              "free", "win", "winner", "won", "cash", "prize", "award", "bonus",
    "billion",
    "urgent", "act now", "apply now", "buy now", "click", "click here", "exclusive deal",
    "limited time", "order now", "money", "rich", "income", "investment", "profit",
    "cheap", "discount", "save big", "save up to", "clearance", "guarantee",
    "no cost", "no fees", "no obligation", "pre-approved", "risk-free",
    "trial", "free trial", "free gift", "gift", "deal", "access now",
    "credit", "credit card", "debt", "loan", "mortgage", "refinance",
    "insurance", "life insurance", "home insurance", "viagra", "cialis",
    "prescription", "pharmacy", "weight loss", "diet", "miracle", "solution",
    "unsubscribe", "opt out", "spam", "remove", "this is not spam",
    "congratulations", "you have been selected", "claim now", "get paid",
    "extra income", "work from home", "be your own boss", "fast cash",
    "earn", "make money", "million", "guaranteed", "increase sales",
    "limited offer", "once in a lifetime", "act immediately", "call now",
    "apply now", "exclusive", "important information", "hidden charges",
    "luxury", "online biz opportunity", "winner!", "!!!", "$$$", "100% free"
}
# Combine features
import emoji


def extract_features(email_text, spam_words=SPAM_WORDS):
    words = email_text.lower().split()

    total_words = len(words)
    spam_count = sum(1 for word in words if word in spam_words)
    (non_latin_count, non_latin_distinct_count) = detect_suspicious_non_latin(email_text)
    return {
        "non_latin_count": non_latin_count,
        "non_latin_distinct_count": non_latin_distinct_count,
        "emoji_count": emoji.emoji_count(email_text) if len(email_text) > 0 else 0,
        "emoji_distinct_count": len(emoji.distinct_emoji_list(email_text)) if len(email_text) > 0 else 0,
        "spam_word_count": spam_count,
        "spam_word_ratio": spam_count / total_words if total_words > 0 else 0.0,
        "has_spam_word": int(spam_count > 0),
        'has_link': int(bool(re.search(r'https?://', email_text))),
        'has_email': int(bool(re.search(r'\S+@\S+', email_text))),
        'has_number': int(bool(re.search(r'\d+', email_text))),
        'has_dollar': int('$' in email_text),
        'has_emoji': int(bool(re.search(r'[^\w\s,]', email_text))),  # crude emoji/symbol detection
        'text_length': len(email_text),
        'word_count': len(email_text.split()),
    }

import pandas as pd
class PredictResult:

    def __init__(self, predicted_label:int, confidence:float, explain_info:list):
        self.predicted_label = 'SPAM' if predicted_label == 1 else 'HAM'
        self.confidence = confidence
        self.explain_info = explain_info
        self.conclusion = [f"""
        The email is {self.predicted_label} with a confidence of {self.confidence:.9%}.👈
        """]
    def __str__(self):
        return f"Predicted Label: {self.predicted_label}, Confidence: {self.confidence}, Explain Info: {self.explain_info}"
    pass

def explain(new_data)->list:
    re = extract_features(new_data['body'][0])
    explain_info = [f"""
    - This email contains {re['non_latin_count']} non-Latin characters from {re['non_latin_distinct_count']} different scripts, includes {re['emoji_count']} emojis, and uses {re['spam_word_count']} common spam words ({re['spam_word_ratio']:.2%} of total words).  \n
    """,

    f"""
    - It contains both a link and an email address, along with numerical and monetary content.  \n
    """,
        f"""
    - These features, combined with a total text length of {re['text_length']} characters and {re['word_count']} words, suggest a high likelihood of promotional or malicious intent.  \n

    """,]
    return explain_info
# TODO Use a class to predict and explain.
def predict(input_pd: pd.DataFrame, model, scaler, feature_cols) -> PredictResult:
    new_data = get_feature_from_body(input_pd)
    assert len(new_data) == 1, "Only one row is allowed for prediction"

    X_scaled = scaler.transform(new_data[feature_cols])

    pred = model.predict(X_scaled).item()
    prob = model.predict_proba(X_scaled)[0, 1]
    explain_info = explain(new_data)
    # TODO
    return PredictResult(predicted_label=pred, confidence=prob,explain_info = explain_info)


    # Add predictions and probabilities to the original data
    # result = new_data.copy()
    # result['prediction'] = preds
    # result['probability'] = probs
def get_feature_from_body(df):
    features_df = df['body'].apply(extract_features).apply(pd.Series)

    df_features = pd.concat([df, features_df], axis=1)
    return df_features


def run_1():
    df = run_get_dataset()
    df_features = get_feature_from_body(df)
    return df_features
