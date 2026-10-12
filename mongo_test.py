# mongo_test.py

from pymongo import MongoClient

uri = "mongodb+srv://macsonaaron10_db_user:FakeNews12345@cluster0.tsk4jbb.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

db = client["fake_news_db"]

print("Connected Successfully")