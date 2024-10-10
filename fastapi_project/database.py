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

exploration_production_collection = db.get_collection("ExplorationProduction")
financial_performance_collection = db.get_collection("FinancialPerformance")
health_safety_environment_collection = db.get_collection("HealthSafetyEnvironment")

exploration_kpi_collection = db.get_collection("ExplorationKPI")
financial_kpi_collection = db.get_collection("FinancialKPI")
health_kpi_collection = db.get_collection("HealthKPI")