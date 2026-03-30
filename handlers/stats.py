# shows search statistics from mongodb / выводит статистику запросов из mongodb

from logger.log_stats import get_top_searches, get_recent_searches


# shows top 5 most searched queries / показывает топ 5 самых частых запросов
def handle_top_searches():
    print("\n--- Top searches ---")
    for i, item in enumerate(get_top_searches(), 1):
        search_type = item.get("search_type", "")
        icon = "keyword" if search_type == "keyword" else "genre"
        print(f"{i}. [{icon}] {item['_id']} - {item['count']} times")
    print()


# shows 5 last searches with time / показывает 5 последних запросов со временем
def handle_recent_searches():
    print("\n--- Recent searches ---")
    for i, item in enumerate(get_recent_searches(), 1):
        params = item['params']
        time = item['timestamp'][:16].replace('T', ' ')
        if item['search_type'] == 'keyword':
            print(f"{i}. [keyword] {params.get('keyword')} | {time}")
        else:
            print(f"{i}. [genre] {params.get('genre')} | {params.get('year_from')}-{params.get('year_to')} | {time}")
    print()
