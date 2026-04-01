"""Handler for searching films by keyword (title). Supports pagination by 10 results.
Обработчик поиска фильмов по ключевому слову. Поддерживает пагинацию по 10.
"""

from db.mysql_connector import search_by_keyword, count_by_keyword
from utils.formatter import print_films
from logger.log_writer import log_search


def handle_keyword_search():
    """Ask user for a keyword, show total count, display results page by page.
    Спрашивает слово, показывает сколько найдено, выводит по 10 штук.
    """
    keyword = input("Enter a keyword to search (0 - back): ")
    if keyword == "0" or not keyword.strip():
        return
    total = count_by_keyword(keyword)
    print(f"\nFound {total} films for \"{keyword}\"")
    log_search("keyword", {"keyword": keyword}, total, keyword)
    offset = 0
    while True:
        results = search_by_keyword(keyword, offset)
        if not results:
            print("No results found")
            break
        # If we got 11 results - there are more pages, show only 10
        # Если получили 11 - есть ещё страницы, показываем только 10
        has_more = len(results) == 11
        results = results[:10]
        print_films(results, start_num=offset + 1)
        if not has_more:
            print("No more results")
            break
        while True:
            choice = input("Show more? (y/n, 0 - menu): ").lower()
            if choice == "y":
                offset += 10
                break
            elif choice in ("n", "0"):
                return
            else:
                print("Please enter y or n")
