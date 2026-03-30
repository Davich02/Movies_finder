# handles search by genre and year range / обработка поиска по жанру и годам

from db.mysql_connector import get_all_genres, search_by_genre_and_years, get_genre_year_ranges, count_by_genre_and_years, get_year_range
from utils.formatter import print_films
from logger.log_writer import log_search


# shows all genres with year ranges, asks user to pick one, then shows results 10 at a time
# показывает жанры с диапазоном лет, пользователь выбирает, потом результаты по 10
def handle_genre_search():
    genres = get_all_genres()
    genre_years = get_genre_year_ranges()

    # show all genres with their year range / выводим жанры с их диапазоном лет
    print("\nAvailable genres:")
    for genre in genres:
        yr = genre_years.get(genre[0], ("?", "?"))
        print(f"  {genre[0]:>2}. {genre[1]:<15} | {yr[0]} - {yr[1]}")
    print("\n0 - Back to main menu")

    # user can pick genre by number or name / можно выбрать жанр по номеру или названию
    user_input = input("Enter genre number or name: ")
    if user_input == "0":
        return

    genre_id = None
    genre_name = None
    # check if user entered a number / проверяем ввёл ли пользователь номер
    if user_input.isdigit():
        num = int(user_input)
        for genre in genres:
            if genre[0] == num:
                genre_id = num
                genre_name = genre[1]
                break
    else:
        for genre in genres:
            if genre[1].lower() == user_input.lower():
                genre_id = genre[0]
                genre_name = genre[1]
                break
    if genre_id is None:
        print("Genre not found")
        return

    # user can enter one year (2006) or range (2000-2010), 3 attempts / можно ввести год или диапазон, 3 попытки
    min_year, max_year = genre_years.get(genre_id, get_year_range())
    year_from, year_to = None, None
    for attempt in range(3):
        try:
            year_range = input(f"Year or range (e.g. {min_year}-{max_year}, 0 - back): ")
            if year_range == "0":
                return
            if "-" in year_range:
                year_from, year_to = year_range.split("-")
            else:
                year_from = year_to = year_range
            year_from, year_to = int(year_from), int(year_to)
        except ValueError:
            print(f"Please enter a valid year! Attempts left: {2 - attempt}")
            year_from, year_to = None, None
            continue
        # check that years make sense / проверяем что года в допустимом диапазоне
        if year_from < min_year or year_to > max_year or year_from > year_to:
            print(f"Invalid range! Available years: {min_year} - {max_year}. Attempts left: {2 - attempt}")
            year_from, year_to = None, None
            continue
        break
    if year_from is None:
        print("Too many wrong attempts, back to menu")
        return

    query_label = f"{genre_name} {year_from}-{year_to}"
    total = count_by_genre_and_years(genre_id, year_from, year_to)
    print(f"\nFound {total} films for \"{genre_name}\" ({year_from}-{year_to})")

    # pagination - same as keyword search / пагинация - так же как в поиске по слову
    offset = 0
    while True:
        results = search_by_genre_and_years(genre_id, year_from, year_to, offset)
        if not results:
            print("No results found")
            break
        has_more = len(results) == 11
        results = results[:10]
        log_search("genre", {"genre": genre_name, "year_from": year_from, "year_to": year_to}, len(results), query_label)
        print_films(results)
        if not has_more:
            print("No more results")
            break
        if input("Show more? (y/n): ") == "y":
            offset += 10
        else:
            break
