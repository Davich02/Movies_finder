from db.mysql_connector import get_all_genres, search_by_genre_and_years, get_genre_year_ranges, count_by_genre_and_years
from utils.formatter import print_films
from logger.log_writer import log_search


# Search films by genre and year range with pagination
def handle_genre_search():
    genres = get_all_genres()
    genre_years = get_genre_year_ranges()
    print("\nAvailable genres:")
    for genre in genres:
        yr = genre_years.get(genre[0], ("?", "?"))
        print(f"  {genre[0]:>2}. {genre[1]:<15} | {yr[0]} - {yr[1]}")
    print("\n0 - Back to main menu")
    genre_name = input("Enter genre name: ")
    if genre_name == "0":
        return
    genre_id = None
    for genre in genres:
        if genre[1].lower() == genre_name.lower():
            genre_id = genre[0]
            break
    if genre_id is None:
        print("Genre not found")
        return
    min_year, max_year = genre_years.get(genre_id, (1900, 2100))
    try:
        year_range = input("Year or range (e.g. 2000-2010): ")
        if "-" in year_range:
            year_from, year_to = year_range.split("-")
        else:
            year_from = year_to = year_range
        year_from, year_to = int(year_from), int(year_to)
    except ValueError:
        print("Please enter a valid year!")
        return
    if year_from < min_year or year_to > max_year or year_from > year_to:
        print(f"Invalid range! Available years: {min_year} - {max_year}")
        return
    query_label = f"{genre_name} {year_from}-{year_to}"
    total = count_by_genre_and_years(genre_id, year_from, year_to)
    print(f"\nFound {total} films for \"{genre_name}\" ({year_from}-{year_to})")
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
    input("\nEnter -> Main menu")
