# saves search queries to mongodb / сохраняет поисковые запросы в mongodb

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# trying to connect to mongo, if it doesnt work - app still runs but without logging
# пробуем подключиться к монго, если не получится - приложение работает но без логов
try:
    client = MongoClient(os.getenv("MONGO_URL"), serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client["ich_edit"]
    collection = db["final_project_101025_david_narkevych"]
except Exception:
    print("Warning: Could not connect to MongoDB. Search logging is disabled.")
    collection = None


# saves one search to mongo with timestamp and what user searched for
# сохраняет один поиск в монго с временем и тем что искал пользователь
def log_search(search_type, params, results_count, query_label):
    if collection is None:
        return
    doc = {
        "timestamp": datetime.now().isoformat(),
        "search_type": search_type,        # "keyword" or "genre"
        "params": params,                   # search details like keyword or genre+years
        "results_count": results_count,
        "query_label": query_label,         # readable label for top searches stats
    }
    collection.insert_one(doc)
