from pymongo import MongoClient

MONGO_URI = "mongodb+srv://macsonaaron10_db_user:FakeNews12345@cluster0.tsk4jbb.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["fake_news_db"]

collection = db["articles"]

print("MongoDB Connected")