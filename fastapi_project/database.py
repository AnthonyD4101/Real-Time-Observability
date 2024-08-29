import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

database_url = os.getenv("DATABASE_URL")

client = MongoClient(database_url)

try:
    client.admin.command('ping')
    print("Successful connection to MongoDB")
except Exception as e:
    print(e)

db = client.get_database("FastAPI")

collection = db.get_collection("Users")