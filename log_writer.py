# Module for connecting to MongoDB database / импорт модуля для подключения к бд
from pymongo import MongoClient
# Module for loading environment variables from .env file / импорт модуля для использования данных с файла .env
from dotenv import load_dotenv
# Database connection module for Sakila MySQL database / Модуль подключения к базе данных Sakila
import os
# Module for working with time
from datetime import datetime


# Load environment variables from .env file / загружает переменные из файла .env
load_dotenv()

# Connection to db with db datas
client = MongoClient(os.getenv("MONGO_URI"))
db = client["ich_edit"]
collection = db["final_project_101025_david_narkevych"]


def log_search(search_type,params,results_count):
    doc = {
        # Getting time and switching it to str
        "timestamp": datetime.now().isoformat(),
        "search_type": search_type,
        "params": params,
        "results_count": results_count,
    }
    collection.insert_one(doc)


