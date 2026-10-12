from pymongo import MongoClient

client = MongoClient("mongodb+srv://macsonaaron10_db_user:FakeNews12345@cluster0.tsk4jbb.mongodb.net/?appName=Cluster0")

db = client["fake_news_db"]

collection = db["articles"]

collection.insert_one({
    "title": "Test News",
    "prediction": "REAL",
    "confidence": 95
})

print("Inserted Successfully")