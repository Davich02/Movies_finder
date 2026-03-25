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

# Helper function to execute SQL queries and return results / вспомогательная функция для выполнения SQL запросов чтобы не повторять код
def execute_query(sql, params=(), fetchone=False):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            if fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()


# Fetches all genre names and IDs from the category table / извлекаем все названия категорий
def get_all_genres():
    return execute_query('SELECT category_id, name FROM category')


# Fetches the minimum and maximum release years from the film table / извлекаем минимальный и максимальный года
def get_year_range():
    return execute_query(
        'SELECT MIN(release_year), MAX(release_year) FROM film', fetchone=True)


#Searching movies by user_input keyword and show 10 options/ поиск фильма по слову от пользователя и выводим 10 позиций
def search_by_keyword(keyword,offset):
    pattern = f"%{keyword}%"
    return execute_query(
        'SELECT film_id, title, release_year, rating, length FROM film WHERE title LIKE %s LIMIT 10 OFFSET %s',
        (pattern,offset,))


#Searching movies by user_input genre and years limits / поиск фильма по жанру и годам от пользователя
def search_by_genre_and_years(genre_id, year_from, year_to, offset):
        return execute_query(
            'Select f.film_id, f.title,f.release_year,f.rating,f.length from film f JOIN film_category fc ON f.film_id = fc.film_id WHERE fc.category_id = %s AND f.release_year BETWEEN %s AND %s LIMIT 10 OFFSET %s ',
            (genre_id,year_from, year_to,offset,))
