import ast
import pandas as pd
import glob
import os

from dataset_settings import CLEANED_ENRON_DATASET_PATH, CAPSTONE_DATASET


def string_to_multiline(text):
    try:
        lst = ast.literal_eval(text)  # Convert to list
        return '\n'.join([s for s in lst if s.strip()])  # Join non-empty lines
    except Exception as e:
        return ''  # Or handle/log the error as needed


# s = ham_df['text'].head(5)
# ham_df['text_str'] = ham_df['text'].apply(string_to_multiline)
def step_100_get_enron_pd():
    csv_folder = CLEANED_ENRON_DATASET_PATH

    target_files = [
        "emaildata_100000_4.csv",
        "emaildata_100000_5.csv",
    ]

    #
    full_paths = [os.path.join(csv_folder, fname) for fname in target_files]

    enron_pd = pd.concat([pd.read_csv(f) for f in full_paths], ignore_index=True)

    enron_pd['body'] = enron_pd['text'].apply(string_to_multiline)
    enron_pd['label'] = 0
    print("Total rows:", len(enron_pd))

    return enron_pd

def step_150_get_spam_dataset():
    df = pd.read_csv(CAPSTONE_DATASET)
    # df = df.applymap(lambda x: x.replace('\r', '').replace('\n', '') if isinstance(x, str) else x)
    df.fillna("", inplace=True)
    df['row_id'] = range(len(df))
    df.rename(columns={'Body': 'body', 'Subject': 'subject'}, inplace=True)
    df['label'] = 1

    print(len(df))

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

def predict(new_data: pd.DataFrame, model, scaler, feature_cols):

    # Select feature columns
    X_new = new_data[feature_cols]

    # Apply standardization using the trained scaler
    X_new_scaled = scaler.transform(X_new)

    # Predict class labels (0 or 1)
    preds = model.predict(X_new_scaled)

    # Predict probabilities for class 1
    probs = model.predict_proba(X_new_scaled)[:, 1]

    # Add predictions and probabilities to the original data
    result = new_data.copy()
    result['prediction'] = preds
    result['probability'] = probs

    return result

def get_feature_from_body(df):
    features_df = df['body'].apply(extract_features).apply(pd.Series)

    df_features = pd.concat([df, features_df], axis=1)
    return df_features



def combine_dataset_and_save_to_disk():
    spam_df = step_150_get_spam_dataset()
    ham_df = step_100_get_enron_pd()
    # ham_df_sample = ham_df.sample(n=len(spam_df), random_state=42)

    df = pd.concat([spam_df[['subject', 'body', 'label']], ham_df[['subject', 'body', 'label']]],
                   ignore_index=True)
    # df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_json("D:\GITHUB\Summer-2025-ECE-597-Group11\data\output\dataset_v20250618.json")
    return df

df = combine_dataset_and_save_to_disk()
# df_features = get_feature_from_body(df)


