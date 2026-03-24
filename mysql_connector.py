# Database connection module for Sakila MySQL database / Модуль подключения к базе данных Sakila
import os
# Module for connecting to MySQL database / импорт модуля для подключения к бд
import pymysql
# Module for loading environment variables from .env file / импорт модуля для использования данных с файла .env
from dotenv import load_dotenv

# Load environment variables from .env file / загружает переменные из файла .env
load_dotenv()

# Database connection settings loaded from environment variables / словарь с данными о бд
config = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
    }

# Creates and returns a MySQL database connection / подключение к бд
def get_connection():
    return pymysql.connect(**config)

# Fetches all genre names and IDs from the category table / извлекаем все названия категорий
def get_all_genres():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT category_id, name FROM category')
            return cursor.fetchall()

# Fetches the minimum and maximum release years from the film table / извлекаем минимальный и максимальный года
def get_year_range():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT MIN(release_year), MAX(release_year) FROM film')
            return cursor.fetchone()