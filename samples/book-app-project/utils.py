def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        print("❌ Invalid choice. Please enter a number between 1 and 5.")



def get_book_details() -> tuple[str, str, int]:
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print("❌ Title cannot be empty.")
    
    while True:
        author = input("Enter author: ").strip()
        if author:
            break
        print("❌ Author cannot be empty.")

    while True:
        year_input = input("Enter publication year (or press Enter for 0): ").strip()
        if not year_input:
            year = 0
            break
        try:
            year = int(year_input)
            if year < 0:
                print("❌ Year must be a positive number.")
                continue
            break
        except ValueError:
            print("❌ Invalid year. Please enter a valid number.")

    return title, author, year


def print_books(books: list) -> None:
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
