from logger.log_stats import get_top_searches, get_recent_searches


# Show top searches from MongoDB
def handle_top_searches():
    print("\n--- Top searches ---")
    for i, item in enumerate(get_top_searches(), 1):
        search_type = item.get("search_type", "")
        icon = "keyword" if search_type == "keyword" else "genre"
        print(f"{i}. [{icon}] {item['_id']} - {item['count']} times")
    input("\nEnter -> Main menu")


# Show recent searches from MongoDB
def handle_recent_searches():
    print("\n--- Recent searches ---")
    for i, item in enumerate(get_recent_searches(), 1):
        params = item['params']
        time = item['timestamp'][:16].replace('T', ' ')
        if item['search_type'] == 'keyword':
            print(f"{i}. [keyword] {params.get('keyword')} | {time}")
        else:
            print(f"{i}. [genre] {params.get('genre')} | {params.get('year_from')}-{params.get('year_to')} | {time}")
    input("\nEnter -> Main menu")
