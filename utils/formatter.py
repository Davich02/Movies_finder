#Module with tables to make beauty output
from tabulate import tabulate


def print_films(films):
    headers = ["ID", "Title", "Year", "Rating", "Duration"]
    films_with_min = [
        (f[0], f[1], f[2], f[3], f"{f[4]} min") for f in films
    ]
    print(tabulate(films_with_min, headers=headers, tablefmt="grid"))
