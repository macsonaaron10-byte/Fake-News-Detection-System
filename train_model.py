# train_model.py

import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

fake = pd.read_csv("dataset/Fake.csv")
true = pd.read_csv("dataset/True.csv")


fake["label"] = 0
true["label"] = 1

data = pd.concat([fake, true])

X = data["text"]
y = data["label"]

vectorizer = TfidfVectorizer(stop_words='english',
                             max_df=0.7)

X = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression()

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

print("Accuracy:", accuracy)

joblib.dump(model, "model/fake_news_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("Model Saved")