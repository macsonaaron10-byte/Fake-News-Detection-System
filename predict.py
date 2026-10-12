import os
import joblib
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "model", "fake_news_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "model", "vectorizer.pkl"))


def clean_text(text):
    text = text.lower()

    # remove URLs (VERY IMPORTANT for BBC articles)
    text = re.sub(r"http\S+|www\S+", "", text)

    # remove special characters but keep spaces
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def predict_news(text):
    cleaned_text = clean_text(text)

    transformed = vectorizer.transform([cleaned_text])

    prediction = model.predict(transformed)[0]

    # safer probability handling
    probs = model.predict_proba(transformed)[0]
    confidence = max(probs)

    label = "REAL" if prediction == 1 else "FAKE"

    return {
        "prediction": label,
        "confidence": round(confidence * 100, 2)
    }