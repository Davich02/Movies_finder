"""MySQL connection and queries to the Sakila database.
Подключение к MySQL и запросы к базе данных Sakila.
"""

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
    """Create and return a MySQL connection. Exit app if DB is unreachable.
    Подключение к БД, если не получилось - останавливает приложение.
    """
    try:
        return pymysql.connect(**config)
    except pymysql.err.OperationalError:
        print("Error: Could not connect to MySQL database. Check your .env settings.")
        exit(1)


def execute_query(sql, params=(), fetchone=False):
    """Execute a SQL query and return results. Reusable helper to avoid repeating connection logic.
    Выполняет SQL запрос и возвращает результат. Чтобы не повторять код подключения.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            if fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()


def get_all_genres():
    """Return all genres (id, name) from the category table.
    Получает все жанры из таблицы category.
    """
    return execute_query('SELECT category_id, name FROM category')


def get_year_range():
    """Return the overall min and max release year across all films.
    Мин и макс год из всех фильмов.
    """
    return execute_query(
        'SELECT MIN(release_year), MAX(release_year) FROM film', fetchone=True)


def get_genre_year_ranges():
    """Return min and max release year per genre as dict {genre_id: (min_year, max_year)}.
    Uses JOIN to connect films with their categories.
    Мин и макс год для каждого жанра отдельно через JOIN.
    """
    rows = execute_query(
        'SELECT fc.category_id, MIN(f.release_year), MAX(f.release_year) '
        'FROM film f JOIN film_category fc ON f.film_id = fc.film_id '
        'GROUP BY fc.category_id'
    )
    return {row[0]: (row[1], row[2]) for row in rows}


def count_by_keyword(keyword):
    """Return total number of films matching the keyword in title.
    Считает сколько фильмов найдено по ключевому слову.
    """
    pattern = f"%{keyword}%"
    result = execute_query(
        'SELECT COUNT(*) FROM film WHERE title LIKE %s',
        (pattern,), fetchone=True)
    return result[0]


def count_by_genre_and_years(genre_id, year_from, year_to):
    """Return total number of films for a given genre and year range.
    Считает фильмы по жанру и диапазону годов.
    """
    result = execute_query(
        'SELECT COUNT(*) FROM film f JOIN film_category fc ON f.film_id = fc.film_id '
        'WHERE fc.category_id = %s AND f.release_year BETWEEN %s AND %s',
        (genre_id, year_from, year_to), fetchone=True)
    return result[0]


def search_by_keyword(keyword, offset):
    """Search films by title keyword with pagination.
    LIMIT 11 instead of 10: the 11th row tells us if more results exist
    without running a separate COUNT query.
    Поиск по слову с лимитом 11 - показываем 10, а 11й нужен чтобы понять есть ли ещё.
    """
    pattern = f"%{keyword}%"
    return execute_query(
        'SELECT film_id, title, release_year, rating, length '
        'FROM film WHERE title LIKE %s LIMIT 11 OFFSET %s',
        (pattern, offset,))


def search_by_genre_and_years(genre_id, year_from, year_to, offset):
    """Search films by genre and year range with pagination.
    JOIN connects film with film_category to filter by genre. LIMIT 11 for pagination check.
    Поиск по жанру и годам, JOIN связывает film с film_category.
    """
    return execute_query(
        'SELECT f.film_id, f.title, f.release_year, f.rating, f.length '
        'FROM film f JOIN film_category fc ON f.film_id = fc.film_id '
        'WHERE fc.category_id = %s AND f.release_year BETWEEN %s AND %s '
        'LIMIT 11 OFFSET %s',
        (genre_id, year_from, year_to, offset,))
