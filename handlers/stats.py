"""Handlers for displaying search analytics from MongoDB.
Обработчики для вывода статистики поиска из MongoDB.
"""

from tabulate import tabulate
from logger.log_stats import get_top_searches, get_recent_searches


def handle_top_searches():
    """Display top 5 most frequent search queries as a table.
    Выводит топ 5 самых частых запросов таблицей.
    """
    print("\n--- Top searches ---")
    rows = []
    for i, item in enumerate(get_top_searches(), 1):
        search_type = item.get("search_type", "")
        icon = "keyword" if search_type == "keyword" else "genre"
        rows.append((i, icon, item['_id'], item['count']))
    if rows:
        print(tabulate(rows, headers=["#", "Type", "Query", "Count"], tablefmt="grid"))
    else:
        print("No searches yet")
    print()


def handle_recent_searches():
    """Display 5 most recent unique searches with count and time as a table.
    Выводит 5 последних уникальных запросов со счётчиком и временем.
    """
    print("\n--- Recent searches ---")
    rows = []
    for i, item in enumerate(get_recent_searches(), 1):
        search_type = item.get("search_type", "")
        icon = "keyword" if search_type == "keyword" else "genre"
        time = item['last_time'][:16].replace('T', ' ')
        rows.append((i, icon, item['_id'], item['count'], time))
    if rows:
        print(tabulate(rows, headers=["#", "Type", "Query", "Count", "Last search"], tablefmt="grid"))
    else:
        print("No searches yet")
    print()
