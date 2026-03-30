# mysql connection and queries / подключение к mysql и запросы к базе

import os
import pymysql
from dotenv import load_dotenv

# loading db credentials from .env / загружаем данные для подключения из .env
load_dotenv()

config = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
    }


# connects to db, if cant connect - stops the app / подключение к бд, если не получилось - останавливает приложение
def get_connection():
    try:
        return pymysql.connect(**config)
    except pymysql.err.OperationalError:
        print("Error: Could not connect to MySQL database. Check your .env settings.")
        exit(1)


# helper so i dont repeat connection code in every function / чтобы не повторять код подключения в каждой функции
def execute_query(sql, params=(), fetchone=False):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            if fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()


# gets all genres from category table / получаем все жанры
def get_all_genres():
    return execute_query('SELECT category_id, name FROM category')


# gets min and max year from all films / мин и макс год из всех фильмов
def get_year_range():
    return execute_query(
        'SELECT MIN(release_year), MAX(release_year) FROM film', fetchone=True)


# gets min and max year for each genre separately / мин и макс год для каждого жанра отдельно
def get_genre_year_ranges():
    rows = execute_query(
        'SELECT fc.category_id, MIN(f.release_year), MAX(f.release_year) '
        'FROM film f JOIN film_category fc ON f.film_id = fc.film_id '
        'GROUP BY fc.category_id'
    )
    return {row[0]: (row[1], row[2]) for row in rows}


# counts how many films match the keyword / считает сколько фильмов по ключевому слову
def count_by_keyword(keyword):
    pattern = f"%{keyword}%"
    result = execute_query('SELECT COUNT(*) FROM film WHERE title LIKE %s', (pattern,), fetchone=True)
    return result[0]


# counts films by genre and year range / считает фильмы по жанру и годам
def count_by_genre_and_years(genre_id, year_from, year_to):
    result = execute_query(
        'SELECT COUNT(*) FROM film f JOIN film_category fc ON f.film_id = fc.film_id '
        'WHERE fc.category_id = %s AND f.release_year BETWEEN %s AND %s',
        (genre_id, year_from, year_to), fetchone=True)
    return result[0]


# search by keyword with limit 11 - we show 10, the 11th just tells us if theres more
# поиск по слову с лимитом 11 - показываем 10, а 11й нужен чтобы понять есть ли ещё
def search_by_keyword(keyword, offset):
    pattern = f"%{keyword}%"
    return execute_query(
        'SELECT film_id, title, release_year, rating, length FROM film WHERE title LIKE %s LIMIT 11 OFFSET %s',
        (pattern, offset,))


# search by genre + years, join connects film with film_category to know which film is in which genre
# поиск по жанру + годам, join связывает film с film_category чтобы знать какой фильм в каком жанре
def search_by_genre_and_years(genre_id, year_from, year_to, offset):
        return execute_query(
            'Select f.film_id, f.title,f.release_year,f.rating,f.length from film f JOIN film_category fc ON f.film_id = fc.film_id WHERE fc.category_id = %s AND f.release_year BETWEEN %s AND %s LIMIT 11 OFFSET %s ',
            (genre_id, year_from, year_to, offset,))
