from mysql_connector import get_all_genres, get_year_range, search_by_keyword, search_by_genre_and_years, get_genre_year_ranges
from log_stats import get_top_searches, get_recent_searches
from formatter import print_films
from log_writer import log_search


def show_menu():
    print("""
=============================
    🎬 MOVIES FINDER
=============================
1. Поиск по ключевому слову
2. Поиск по жанру и годам
3. Топ популярных запросов
4. Последние запросы
5. Выйти
=============================
    """)


# Search films by keyword with pagination / Поиск фильмов по названию
def handle_keyword_search():
    keyword = input("Введите слово для поиска (0 - выход): ")
    if keyword == "0" or not keyword.strip():
        return
    offset = 0
    while True:
        results = search_by_keyword(keyword, offset)
        if not results:
            print("Больше нет результатов 😔")
            break
        has_more = len(results) == 11
        results = results[:10]
        log_search("keyword", {"keyword": keyword}, len(results), keyword)
        print_films(results)
        if not has_more:
            print("Больше нет результатов 😔")
            break
        if input("Показать ещё? (y/n): ") == "y":
            offset += 10
        else:
            break
    input("\nEnter → Главное меню")


# Search films by genre and year range with pagination / Поиск фильма с указанием жанра и годов
def handle_genre_search():
    genres = get_all_genres()
    genre_years = get_genre_year_ranges()
    print("\nДоступные жанры:")
    for genre in genres:
        yr = genre_years.get(genre[0], ("?", "?"))
        print(f"  {genre[0]:>2}. {genre[1]:<15} | {yr[0]} — {yr[1]}")
    print("\n0 - Вернуться в главное меню")
    genre_name = input("Введите название жанра: ")
    if genre_name == "0":
        return
    genre_id = None
    for genre in genres:
        if genre[1].lower() == genre_name.lower():
            genre_id = genre[0]
            break
    if genre_id is None:
        print("Жанр не найден 😔")
        return
    try:
        year_range = input("Год или диапазон (например 2000-2010): ")
        if "-" in year_range:
            year_from, year_to = year_range.split("-")
        else:
            year_from = year_to = year_range
        year_from, year_to = int(year_from), int(year_to)
    except ValueError:
        print("Введите корректный год!")
        return
    query_label = f"{genre_name} {year_from}-{year_to}"
    offset = 0
    while True:
        results = search_by_genre_and_years(genre_id, year_from, year_to, offset)
        if not results:
            print("Больше нет результатов 😔")
            break
        has_more = len(results) == 11
        results = results[:10]
        log_search("genre", {"genre": genre_name, "year_from": year_from, "year_to": year_to}, len(results), query_label)
        print_films(results)
        if not has_more:
            break
        if input("Показать ещё? (y/n): ") == "y":
            offset += 10
        else:
            break
    input("\nEnter → Главное меню")


# Show top searches from MongoDB / Вывод топ запросов
def handle_top_searches():
    print("\n--- Топ популярных запросов ---")
    for i, item in enumerate(get_top_searches(), 1):
        search_type = item.get("search_type", "")
        icon = "🔍" if search_type == "keyword" else "🎬"
        print(f"{i}. {icon} {item['_id']} — {item['count']} раз")
    input("\nEnter → Главное меню")


# Show recent searches from MongoDB / Вывод последних запросов
def handle_recent_searches():
    print("\n--- Последние запросы ---")
    for i, item in enumerate(get_recent_searches(), 1):
        params = item['params']
        time = item['timestamp'][:16].replace('T', ' ')
        if item['search_type'] == 'keyword':
            print(f"{i}. Слово: {params.get('keyword')} | {time}")
        else:
            print(f"{i}. Жанр: {params.get('genre')} | {params.get('year_from')}-{params.get('year_to')} | {time}")
    input("\nEnter → Главное меню")


# Main func / Главная функция для запуска программы
def main():
    while True:
        show_menu()
        try:
            button = int(input("Выберите действие: "))
        except ValueError:
            print("Введите число!")
            continue
        if button == 1:
            handle_keyword_search()
        elif button == 2:
            handle_genre_search()
        elif button == 3:
            handle_top_searches()
        elif button == 4:
            handle_recent_searches()
        elif button == 5:
            print("До встречи!")
            break
        else:
            print("УПС 🫢\nНекорректный выбор!")


if __name__ == '__main__':
    main()
