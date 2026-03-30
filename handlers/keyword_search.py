from db.mysql_connector import search_by_keyword, count_by_keyword
from utils.formatter import print_films
from logger.log_writer import log_search


# Search films by keyword with pagination
def handle_keyword_search():
    keyword = input("Enter a keyword to search (0 - back): ")
    if keyword == "0" or not keyword.strip():
        return
    total = count_by_keyword(keyword)
    print(f"\nFound {total} films for \"{keyword}\"")
    offset = 0
    while True:
        results = search_by_keyword(keyword, offset)
        if not results:
            print("No results found")
            break
        has_more = len(results) == 11
        results = results[:10]
        log_search("keyword", {"keyword": keyword}, len(results), keyword)
        print_films(results)
        if not has_more:
            print("No more results")
            break
        if input("Show more? (y/n): ") == "y":
            offset += 10
        else:
            break
    input("\nEnter -> Main menu")
