from tabulate import tabulate

def print_films(films):
    headers = ["ID", "Название", "Год", "Рейтинг", "Длина"]
    print(tabulate(films, headers=headers, tablefmt="grid"))