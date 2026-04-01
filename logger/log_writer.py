"""MongoDB logging module. Saves every search query as a document for analytics.
Модуль логирования. Сохраняет каждый поисковый запрос в MongoDB.
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# Try to connect to MongoDB. If it fails, set collection to None so the app still works.
# Пробуем подключиться к MongoDB. Если не получится - приложение работает, но без логов.
try:
    client = MongoClient(os.getenv("MONGO_URL"), serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client["ich_edit"]
    collection = db["final_project_101025_david_narkevych"]
except Exception:
    print("Warning: Could not connect to MongoDB. Search logging is disabled.")
    collection = None


def log_search(search_type, params, results_count, query_label):
    """Save a search query to MongoDB.
    Сохраняет один поисковый запрос в MongoDB.

    Args:
        search_type: 'keyword' or 'genre'
        params: dict with search parameters (keyword, genre, years)
        results_count: how many films were found
        query_label: readable label for analytics (e.g. 'love' or 'Action 2006-2006')
    """
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
