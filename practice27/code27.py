class BookModel:
    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        self.books.append({"title": title, "author": author})

    def get_all_books(self):
        return self.books

    def search_books(self, query):
        query_lower = query.lower()
        return [b for b in self.books if query_lower in b["title"].lower()]

    def delete_book(self, index):
        if 0 <= index < len(self.books):
            return self.books.pop(index)
        return None


class BookView:
    @staticmethod
    def show_menu():
        print("\n    Каталог книг    ")
        print("1. Додати книгу")
        print("2. Показати каталог")
        print("3. Знайти книгу")
        print("4. Видалити книгу")
        print("5. Вихід")

    @staticmethod
    def show_books(books):
        if not books:
            print("Каталог порожній.")
            return
        print("\nСписок книг у каталозі:")
        for idx, book in enumerate(books, 1):
            print(f"{idx}. {book['title']} — {book['author']}")

    @staticmethod
    def show_search_results(query, books):
        print(f"\nПошук «{query}»: знайдено книг: {len(books)}")
        for idx, book in enumerate(books, 1):
            print(f"{idx}. {book['title']} — {book['author']}")

    @staticmethod
    def show_message(message):
        print(f"[Повідомлення]: {message}")

    @staticmethod
    def get_input(prompt):
        return input(prompt).strip()


class BookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        while True:
            self.view.show_menu()
            choice = self.view.get_input("Оберіть дію (1-5): ")

            if choice == "1":
                title = self.view.get_input("Введіть назву книги: ")
                author = self.view.get_input("Введіть автора книги: ")
                if title and author:
                    self.model.add_book(title, author)
                    self.view.show_message(f"Додано: {title} — {author}")
                else:
                    self.view.show_message("Помилка: назва та автор не можуть бути порожніми.")

            elif choice == "2":
                books = self.model.get_all_books()
                self.view.show_books(books)

            elif choice == "3":
                query = self.view.get_input("Введіть назву для пошуку: ")
                if query:
                    results = self.model.search_books(query)
                    self.view.show_search_results(query, results)
                else:
                    self.view.show_message("Помилка: пошуковий запит не може бути порожнім.")

            elif choice == "4":
                books = self.model.get_all_books()
                if not books:
                    self.view.show_message("Каталог порожній, нічого видаляти.")
                    continue
                self.view.show_books(books)
                idx_str = self.view.get_input("Введіть номер книги для видалення: ")
                try:
                    idx = int(idx_str) - 1
                    removed = self.model.delete_book(idx)
                    if removed:
                        self.view.show_message(f"Видалено: {removed['title']} — {removed['author']}")
                    else:
                        self.view.show_message("Помилка: книга з таким номером не знайдена.")
                except ValueError:
                    self.view.show_message("Помилка: введено некоректне число.")

            elif choice == "5":
                self.view.show_message("Роботу програми завершено.")
                break
            else:
                self.view.show_message("Помилка: невідома команда. Оберіть від 1 до 5.")


if __name__ == "__main__":
    model = BookModel()
    view = BookView()
    controller = BookController(model, view)
    controller.run()
