"""Entry point of the application. Displays menu and routes user input to handlers.
Главный файл - запуск приложения и маршрутизация по меню.
"""

from handlers.keyword_search import handle_keyword_search
from handlers.genre_search import handle_genre_search
from handlers.stats import handle_top_searches, handle_recent_searches


def show_menu():
    """Print the main menu with available options. / Выводит главное меню."""
    print("""
=============================
      MOVIES FINDER
=============================
1. Search by keyword
2. Search by genre and year
3. Top searches
4. Recent searches
5. Exit
=============================
    """)


def main():
    """Main loop - show menu, read user choice, call the handler. / Цикл меню пока не выберет выход."""
    while True:
        show_menu()
        try:
            button = int(input("Choose an option: "))
        except ValueError:
            print("Please enter a number to choose the option !")
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
            print("Goodbye!")
            break
        else:
            print("Invalid option!")


if __name__ == '__main__':
    main()
