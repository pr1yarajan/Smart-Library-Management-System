
import csv


BOOKS_FILE = "books.csv"
RECORDS_FILE = "records.csv"


BOOK_FIELDS = ["id/isbn", "title", "author", "category", "count"]

RECORD_FIELDS = [
    "member_id", "book_id", "date_of_issue",
    "date_of_return", "Is_Overdue", "fine"
]




# Validate non-empty text
def validate_text(prompt):

    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty!")


# Validate menu choice
def validate_menu_choice():

    while True:
        choice = input("Enter your choice: ").strip()

        if choice in ["1", "2", "3", "4"]:
            return choice

        print("Invalid choice! Please select between 1 and 4.")


def read_data(filename):

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def recommend_books():

    books = read_data(BOOKS_FILE)

    if not books:
        print("No books available!")
        return

    selected_category = validate_text(
        "Enter category to recommend books: "
    ).lower()

    recommended_books = []

    for book in books:

        if book["category"].strip().lower() == selected_category:
            recommended_books.append(book)

    if not recommended_books:
        print("No books found in this category!")
        return

    print("\n===== RECOMMENDED BOOKS =====")

    for book in recommended_books:

        print("Book ID/ISBN:", book["id/isbn"])
        print("Title:", book["title"])
        print("Author:", book["author"])
        print("Category:", book["category"])
        print("Available Copies:", book["count"])
        print("-" * 30)


def rank_books():

    books = read_data(BOOKS_FILE)
    records = read_data(RECORDS_FILE)

    if not books:
        print("No books available!")
        return

    borrowing_count = {}

    for book in books:
        borrowing_count[book["id/isbn"]] = 0

    for record in records:
        book_id = record["book_id"]

        if book_id in borrowing_count:
            borrowing_count[book_id] += 1

    ranked_books = []

    for book in books:

        book_id = book["id/isbn"]

        ranked_book = {
            "id/isbn": book_id,
            "title": book["title"],
            "author": book["author"],
            "category": book["category"],
            "borrow_count": borrowing_count[book_id]
        }

        ranked_books.append(ranked_book)

    ranked_books.sort(
        key=lambda book: book["borrow_count"],
        reverse=True
    )

    print("\n===== BOOKS RANKED BY BORROWING FREQUENCY =====")

    rank = 1

    for book in ranked_books:

        print("Rank:", rank)
        print("Book ID/ISBN:", book["id/isbn"])
        print("Title:", book["title"])
        print("Author:", book["author"])
        print("Category:", book["category"])
        print("Times Borrowed:", book["borrow_count"])
        print("-" * 30)

        rank += 1


def identify_popular_books():

    books = read_data(BOOKS_FILE)
    records = read_data(RECORDS_FILE)

    if not books:
        print("No books available!")
        return

    borrowing_count = {}

    for book in books:
        borrowing_count[book["id/isbn"]] = 0

    for record in records:
        book_id = record["book_id"]

        if book_id in borrowing_count:
            borrowing_count[book_id] += 1

    maximum_borrow_count = 0

    for book_id in borrowing_count:

        if borrowing_count[book_id] > maximum_borrow_count:
            maximum_borrow_count = borrowing_count[book_id]

    if maximum_borrow_count == 0:
        print("No books have been borrowed yet!")
        return

    print("\n===== POPULAR BOOKS =====")

    for book in books:

        book_id = book["id/isbn"]

        if borrowing_count[book_id] == maximum_borrow_count:

            print("Book ID/ISBN:", book_id)
            print("Title:", book["title"])
            print("Author:", book["author"])
            print("Category:", book["category"])
            print("Times Borrowed:", maximum_borrow_count)
            print("-" * 30)


def recommendation_menu():

    while True:

        print("\n===== BOOK RECOMMENDATION MODULE =====")
        print("1. Recommend Books by Category")
        print("2. Rank Books by Borrowing Frequency")
        print("3. Identify Popular Books")
        print("4. Exit")

        choice = validate_menu_choice()

        if choice == "1":
            recommend_books()

        elif choice == "2":
            rank_books()

        elif choice == "3":
            identify_popular_books()

        elif choice == "4":
            print("Exiting Recommendation Module.")
            break


if __name__ == "__main__":
    recommendation_menu()
