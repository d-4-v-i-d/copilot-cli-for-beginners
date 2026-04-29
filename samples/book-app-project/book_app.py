import sys
from datetime import datetime
from typing import Callable, List
from books import BookCollection, Book


# Global collection instance
collection = BookCollection()


def show_books(books: List[Book]) -> None:
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print()


def handle_list() -> None:
    books = collection.list_books()
    show_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year (leave blank for 0): ").strip()

    if not title or not author:
        print("Error: Title and author cannot be empty.\n")
        return

    try:
        year = int(year_str) if year_str else 0
        if year < 0:
            print("Error: Year cannot be negative.\n")
            return
        if year > datetime.now().year + 1:
            print(f"Error: Year cannot be in the future (max {datetime.now().year + 1}).\n")
            return
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError:
        print("Error: Year must be a valid number.\n")


def handle_remove() -> None:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    if collection.remove_book(title):
        print(f"\nBook '{title}' removed successfully.\n")
    else:
        print(f"\nBook '{title}' not found.\n")


def handle_find() -> None:
    print("\nFind Books by Title or Author\n")

    query = input("Search (title or author): ").strip()
    if not query:
        print("Error: Search query cannot be empty.\n")
        return
    books = collection.search_books(query)

    show_books(books)


def handle_mark_read() -> None:
    print("\nMark Book as Read\n")

    title = input("Enter the title of the book: ").strip()
    if not title:
        print("Error: Title cannot be empty.\n")
        return
    if collection.mark_as_read(title):
        print(f"\nBook '{title}' marked as read.\n")
    else:
        print(f"\nBook '{title}' not found.\n")


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by title or author
  read     - Mark a book as read
  help     - Show this help message
""")


COMMANDS: dict[str, Callable[[], None]] = {
    "list": handle_list,
    "add": handle_add,
    "remove": handle_remove,
    "find": handle_find,
    "read": handle_mark_read,
    "help": show_help,
}


def main() -> None:
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()
    handler = COMMANDS.get(command)

    if handler:
        handler()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
