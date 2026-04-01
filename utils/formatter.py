"""Output formatting module. Displays film search results as a table.
Модуль форматирования. Выводит результаты поиска фильмов таблицей.
"""

from tabulate import tabulate


def print_films(films, start_num=1):
    """Format and print a list of films as a grid table.
    Форматирует и выводит список фильмов в виде таблицы.

    Args:
        films: list of tuples (id, title, year, rating, length)
        start_num: starting number for row numbering (continues across pages)
    """
    headers = ["#", "Title", "Year", "Rating", "Duration"]
    films_with_min = [
        (i, f[1], f[2], f[3], f"{f[4]} min") for i, f in enumerate(films, start_num)
    ]
    print(tabulate(films_with_min, headers=headers, tablefmt="grid"))
