from mysql_connector import get_all_genres, get_year_range, search_by_keyword, search_by_genre_and_years
from log_stats import get_top_searches, get_recent_searches
from formatter  import print_films
from log_writer import log_search



def show_menu():
    print("""
=============================
    🎬 MOVIES FINDER
=============================
1. Поиск по ключевому слову
2. Поиск по жанру и годам
3. Популярные запросы
4. Выйти
=============================
    """)


def main():
    while True:
        show_menu()
        try:
            button = int(input("Выберите действие: "))
        except ValueError:
            print("Введите число!")
            continue
        if button == 1:
            keyword = input("Введите слово для поиска: ")
            if not keyword.strip():
                print("Введите слово для поиска!")
            else:
                results = search_by_keyword(keyword, 0)
                if not results:
                    print("Ничего не найдено 😔")
                else:
                    print_films(results)
        elif button == 2:
            genres = get_all_genres()
            years = get_year_range()
            # сначала выводим ВСЕ жанры
            for genre in genres:
                print(f"{genre[0]} - {genre[1]:<15} | {years[0]} - {years[1]}")

                    # потом спрашиваем
            print("\n0 - Вернуться в главное меню")
            genre_name = input("Введите название жанра: ")

            if genre_name == "0":
                continue

            genre_id = None
            for genre in genres:
                if genre[1].lower() == genre_name.lower():
                    genre_id = genre[0]
                    break

            if genre_id is None:
                print("Жанр не найден 😔")
            else:
                try:
                    year_from = int(input("Год от: "))
                    year_to = int(input("Год до: "))
                except ValueError:
                    print("Введите корректный год!")
                else:
                    results = search_by_genre_and_years(genre_id, year_from, year_to, 0)
                    if not results:
                        print("Ничего не найдено 😔")
                    else:
                        print_films(results)
        elif button == 3:
            get_recent_searches()
        elif button == 4:
            print("До встречи !")
            break
        else:
            print("УПС 🫢\nНекорректный  выбор, введите число для поиска. ")





if __name__ == '__main__':
    main()

