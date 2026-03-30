# formats film results into a nice table / форматирует результаты в красивую таблицу

from tabulate import tabulate


# takes list of films and prints them as a grid table / берёт список фильмов и выводит таблицей
def print_films(films):
    headers = ["#", "Title", "Year", "Rating", "Duration"]
    # enumerate instead of db id / нумерация вместо id из базы
    films_with_min = [
        (i, f[1], f[2], f[3], f"{f[4]} min") for i, f in enumerate(films, 1)
    ]
    print(tabulate(films_with_min, headers=headers, tablefmt="grid"))
