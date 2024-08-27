from pymongo import MongoClient

DATABASE_URL = "mongodb+srv://fastAdmin:password123!@personalprojects.uuknh.mongodb.net/?retryWrites=true&w=majority&appName=PersonalProjects"

client = MongoClient(DATABASE_URL)

try:
    client.admin.command('ping')
    print("Successful connection to MongoDB")
except Exception as e:
    print(e)

db = client.get_database("FastAPI")

collection = db.get_collection("Users")