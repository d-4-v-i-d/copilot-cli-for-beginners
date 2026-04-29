import sys
from datetime import datetime
from typing import Callable, List
from books import BookCollection, Book


# Global collection instance
collection = BookCollection()


def show_books(books: List[Book], label: str = "Results") -> None:
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print(f"\n{label}:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print(f"\n{len(books)} book(s) displayed.\n")


def handle_list() -> None:
    books = collection.list_books()
    show_books(books, label="Your Book Collection")


def handle_add() -> None:
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year (leave blank for 0): ").strip()

    if not title or not author:
        print("Error: Title and author cannot be empty.\n", file=sys.stderr)
        return

    try:
        year = int(year_str) if year_str else 0
        if year < 0:
            print("Error: Year cannot be negative.\n", file=sys.stderr)
            return
        if year > datetime.now().year + 1:
            print(f"Error: Year cannot be in the future (max {datetime.now().year + 1}).\n", file=sys.stderr)
            return
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError:
        print("Error: Year must be a valid number.\n", file=sys.stderr)


def handle_unread() -> None:
    books = [b for b in collection.list_books() if not b.read]
    show_books(books, label="Unread Books")


def handle_remove() -> None:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    if not title:
        print("Error: Title cannot be empty.\n", file=sys.stderr)
        return

    book = collection.find_book_by_title(title)
    if not book:
        print(f"\nBook '{title}' not found.\n")
        return

    status = "read" if book.read else "unread"
    print(f"\nFound: '{book.title}' by {book.author} ({book.year}) — {status}")
    confirm = input("Are you sure you want to remove it? (y/N): ").strip().lower()
    if confirm == "y":
        collection.remove_book(title)
        print(f"\nBook '{title}' removed successfully.\n")
    else:
        print("\nRemoval cancelled.\n")


def handle_find() -> None:
    print("\nFind Books by Title or Author\n")

    query = input("Search (title or author): ").strip()
    if not query:
        print("Error: Search query cannot be empty.\n", file=sys.stderr)
        return
    books = collection.search_books(query)

    show_books(books, label=f"Results for '{query}'")


def handle_author() -> None:
    print("\nFind Books by Author (exact name match)\n")

    author = input("Author name: ").strip()
    if not author:
        print("Error: Author name cannot be empty.\n", file=sys.stderr)
        return
    books = collection.find_by_author(author)
    show_books(books, label=f"Books by '{author}'")


def handle_mark_read() -> None:
    print("\nMark Book as Read\n")

    title = input("Enter the title of the book: ").strip()
    if not title:
        print("Error: Title cannot be empty.\n", file=sys.stderr)
        return
    if collection.mark_as_read(title):
        print(f"\nBook '{title}' marked as read.\n")
    else:
        print(f"\nBook '{title}' not found.\n")


def handle_stats() -> None:
    books = collection.list_books()
    total = len(books)
    read_count = sum(1 for b in books if b.read)
    unread_count = total - read_count
    pct = f"{read_count / total * 100:.0f}%" if total > 0 else "N/A"
    print(f"\nCollection Stats:\n")
    print(f"  Total:    {total}")
    print(f"  Read:     {read_count}")
    print(f"  Unread:   {unread_count}")
    print(f"  Progress: {pct}\n")


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title (with confirmation)
  find     - Find books by title or author (substring)
  author   - Find books by exact author name
  read     - Mark a book as read
  unread   - Show only unread books
  stats    - Show collection statistics
  help     - Show this help message
  quit     - Exit interactive mode
""")


COMMANDS: dict[str, Callable[[], None]] = {
    "list": handle_list,
    "add": handle_add,
    "remove": handle_remove,
    "find": handle_find,
    "author": handle_author,
    "read": handle_mark_read,
    "unread": handle_unread,
    "stats": handle_stats,
    "help": show_help,
}


def run_command(command: str) -> bool:
    """Dispatch a command. Returns False if the user wants to quit."""
    if command in ("quit", "exit"):
        return False
    handler = COMMANDS.get(command)
    if handler:
        handler()
    else:
        print(f"Unknown command: '{command}'\n", file=sys.stderr)
        show_help()
    return True


def run_repl() -> None:
    """Interactive loop — only entered when stdin is a TTY."""
    print("Book Collection Helper — interactive mode. Type 'help' for commands, 'quit' to exit.\n")
    while True:
        try:
            command = input("book-app> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!\n")
            break
        if not command:
            continue
        if not run_command(command):
            print("Goodbye!\n")
            break


def main() -> None:
    if len(sys.argv) < 2:
        if sys.stdin.isatty():
            run_repl()
        else:
            show_help()
        return

    command = sys.argv[1].lower()
    if not run_command(command):
        return
    if COMMANDS.get(command) is None and command not in ("quit", "exit"):
        sys.exit(1)


if __name__ == "__main__":
    main()
