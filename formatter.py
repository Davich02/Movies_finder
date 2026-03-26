#Module with tables to make beuaty output
from tabulate import tabulate
# Printing with table
def print_films(films):
    headers = ["ID", "Название", "Год", "Рейтинг", "Продолжительность"]
    films_with_min = [
        (f[0], f[1], f[2], f[3], f"{f[4]} min") for f in films
    ]
    print(tabulate(films_with_min, headers=headers, tablefmt="grid"))