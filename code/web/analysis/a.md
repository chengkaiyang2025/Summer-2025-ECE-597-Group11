You're exactly right — before training a spam classifier (e.g., with logistic regression), you should **combine the datasets, extract meaningful features**, and perform **exploratory data analysis (EDA)**. Here's a clear, step-by-step plan tailored to your case:

---

## 🧠 Goal

Build a **binary spam classifier** using:

* ✅ Your labeled **2K spam** dataset (`label = 1`)
* ✅ Clean **Enron ham emails** (`label = 0`)
* ✅ Logistic Regression as your model

---

## ✅ Step-by-Step Workflow (Before Training)

### 📂 Step 1: **Combine the Two Datasets**

```python
import pandas as pd

# Load spam and ham datasets
spam_df = pd.read_csv('your_spam.csv')     # must contain 'text' column
ham_df = pd.read_csv('enron_clean.csv')    # must contain 'text' column

# Add labels
spam_df['label'] = 1
ham_df['label'] = 0

# Combine them
df = pd.concat([spam_df, ham_df], ignore_index=True)

# Shuffle rows
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(df.head())
```

---

### 🔍 Step 2: **Basic EDA (Exploratory Data Analysis)**

```python
# Check label balance
df['label'].value_counts().plot(kind='bar', title='Spam vs Ham Distribution')

# Look at basic stats
df['text_length'] = df['text'].apply(len)
df['word_count'] = df['text'].apply(lambda x: len(x.split()))

# Compare distributions
import seaborn as sns
sns.histplot(data=df, x='text_length', hue='label', bins=100, kde=True)
```

---

### 🛠 Step 3: **Feature Engineering**

Create new **binary or numerical features** from the text:

```python
import re

def extract_features(text):
    return {
        'has_link': int(bool(re.search(r'https?://', text))),
        'has_email': int(bool(re.search(r'\S+@\S+', text))),
        'has_number': int(bool(re.search(r'\d+', text))),
        'has_dollar': int('$' in text),
        'has_emoji': int(bool(re.search(r'[^\w\s,]', text))),  # crude emoji/symbol detection
        'text_length': len(text),
        'word_count': len(text.split()),
    }

features_df = df['text'].apply(extract_features).apply(pd.Series)

# Combine features
df_features = pd.concat([df, features_df], axis=1)
```

---

### 🔢 Step 4: **Optional — TF-IDF Text Vectorization**

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=10000, stop_words='english')
X_tfidf = vectorizer.fit_transform(df_features['text'])
```

---

### 🧩 Step 5: **Combine Features**

```python
from scipy.sparse import hstack

# Choose which features to use:
numeric_features = df_features[['has_link', 'has_email', 'has_number', 'has_dollar', 'has_emoji', 'text_length', 'word_count']]
X = hstack([X_tfidf, numeric_features])
y = df_features['label']
```

---

### ✅ Next Step: Train/Test Split and Modeling

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
```

---

## 🔁 Summary of Steps

| Step | Description                                           |
| ---- | ----------------------------------------------------- |
| 1    | Combine datasets and assign labels                    |
| 2    | Explore label distribution, text length, word counts  |
| 3    | Extract custom features (has\_link, has\_emoji, etc.) |
| 4    | Vectorize text using TF-IDF                           |
| 5    | Merge TF-IDF and custom features                      |
| 6    | Split, train, and evaluate model                      |

---

Let me know if you want:

* A complete runnable Jupyter Notebook template
* More advanced NLP features (e.g. spam keywords, word embeddings)
* How to deploy the model or build an API around it
