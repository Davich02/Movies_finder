# Database connection module for Sakila MySQL database
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

config = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
    }


def get_connection():
    try:
        return pymysql.connect(**config)
    except pymysql.err.OperationalError:
        print("Error: Could not connect to MySQL database. Check your .env settings.")
        exit(1)


def execute_query(sql, params=(), fetchone=False):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            if fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()


def get_all_genres():
    return execute_query('SELECT category_id, name FROM category')


def get_year_range():
    return execute_query(
        'SELECT MIN(release_year), MAX(release_year) FROM film', fetchone=True)


def get_genre_year_ranges():
    rows = execute_query(
        'SELECT fc.category_id, MIN(f.release_year), MAX(f.release_year) '
        'FROM film f JOIN film_category fc ON f.film_id = fc.film_id '
        'GROUP BY fc.category_id'
    )
    return {row[0]: (row[1], row[2]) for row in rows}


def count_by_keyword(keyword):
    pattern = f"%{keyword}%"
    result = execute_query('SELECT COUNT(*) FROM film WHERE title LIKE %s', (pattern,), fetchone=True)
    return result[0]


def count_by_genre_and_years(genre_id, year_from, year_to):
    result = execute_query(
        'SELECT COUNT(*) FROM film f JOIN film_category fc ON f.film_id = fc.film_id '
        'WHERE fc.category_id = %s AND f.release_year BETWEEN %s AND %s',
        (genre_id, year_from, year_to), fetchone=True)
    return result[0]


def search_by_keyword(keyword, offset):
    pattern = f"%{keyword}%"
    return execute_query(
        'SELECT film_id, title, release_year, rating, length FROM film WHERE title LIKE %s LIMIT 11 OFFSET %s',
        (pattern, offset,))


def search_by_genre_and_years(genre_id, year_from, year_to, offset):
        return execute_query(
            'Select f.film_id, f.title,f.release_year,f.rating,f.length from film f JOIN film_category fc ON f.film_id = fc.film_id WHERE fc.category_id = %s AND f.release_year BETWEEN %s AND %s LIMIT 11 OFFSET %s ',
            (genre_id, year_from, year_to, offset,))
