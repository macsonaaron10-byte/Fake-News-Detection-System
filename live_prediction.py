import requests
from langdetect import detect
from predict import predict_news
from pymongo import MongoClient

API_KEY = "d853da22e622496ea090b06a3bd37301"

client = MongoClient("mongodb+srv://macsonaaron10_db_user:FakeNews12345@cluster0.tsk4jbb.mongodb.net/?appName=Cluster0")

db = client["fake_news_db"]

collection = db["articles"]

url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

response = requests.get(url)

data = response.json()

for article in data["articles"]:

    title = article["title"]

    try:
        language = detect(title)
    except:
        language = "unknown"

    result = predict_news(title)

    document = {
        "title": title,
        "language": language,
        "prediction": result["prediction"],
        "confidence": result["confidence"]
    }

    collection.insert_one(document)

    print("Saved:", title)