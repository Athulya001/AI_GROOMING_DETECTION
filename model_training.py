# ==============================
# AI Grooming & Threat Detection
# ==============================

# STEP 1: Import Libraries
import pickle
import pandas as pd
import numpy as np
import nltk
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Download stopwords (only first time)
nltk.download('stopwords')
from nltk.corpus import stopwords

# Load stopwords once (efficient way)
stop_words = set(stopwords.words('english'))

# STEP 2: Text Preprocessing Function
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)


# STEP 3: Load Dataset
data = pd.read_csv("dataset.csv")

print("Dataset Loaded Successfully!")
print(data.head())


# Apply preprocessing
data['text'] = data['text'].apply(preprocess)


# STEP 4: Convert Text to Numerical Features (TF-IDF with bigrams)
vectorizer = TfidfVectorizer(ngram_range=(1,2))
X = vectorizer.fit_transform(data['text'])
y = data['label']


# STEP 5: Split Data into Train & Test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# STEP 6: Train Model
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train, y_train)

# Save model and vectorizer
import pickle

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model and Vectorizer Saved Successfully!")

# STEP 7: Make Predictions
y_pred = model.predict(X_test)


# STEP 8: Evaluate Model
print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# STEP 9: Test Custom Message with Confidence Score
while True:
    user_input = input("\nEnter a message to test (or type 'exit'): ")

    if user_input.lower() == "exit":
        break

    cleaned = preprocess(user_input)
    vectorized = vectorizer.transform([cleaned])

    prediction = model.predict(vectorized)
    probabilities = model.predict_proba(vectorized)

    confidence = max(probabilities[0]) * 100

    print("Prediction:", prediction[0])
    print("Confidence Score:", round(confidence, 2), "%")

    # Risk Level Logic
    if prediction[0] == "safe":
        print("Risk Level: LOW")
    elif prediction[0] == "harassment":
        print("Risk Level: MEDIUM")
    elif prediction[0] == "threat":
        print("Risk Level: HIGH")
    elif prediction[0] == "grooming":
        print("Risk Level: CRITICAL")