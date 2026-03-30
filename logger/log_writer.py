from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

try:
    client = MongoClient(os.getenv("MONGO_URL"), serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client["ich_edit"]
    collection = db["final_project_101025_david_narkevych"]
except Exception:
    print("Warning: Could not connect to MongoDB. Search logging is disabled.")
    collection = None


def log_search(search_type, params, results_count, query_label):
    if collection is None:
        return
    doc = {
        "timestamp": datetime.now().isoformat(),
        "search_type": search_type,
        "params": params,
        "results_count": results_count,
        "query_label": query_label,
    }
    collection.insert_one(doc)
