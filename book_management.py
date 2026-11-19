
import csv
import os

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


# Validate 13-digit Book ID / ISBN
def validate_book_id(prompt):

    while True:
        book_id = input(prompt).strip()

        if book_id.isdigit() and len(book_id) == 13:
            return book_id

        print("Book ID must contain exactly 13 digits!")


# Validate positive number of copies
def validate_positive_count(prompt):

    while True:
        value = input(prompt).strip()

        if value.isdigit() and int(value) > 0:
            return int(value)

        print("Enter a positive whole number!")


# Validate optional non-negative count
def validate_optional_count(prompt):

    while True:
        value = input(prompt).strip()

        if value == "":
            return None

        if value.isdigit():
            return int(value)

        print("Enter zero or a positive whole number!")


# Validate menu choice
def validate_menu_choice():

    while True:
        choice = input("Enter your choice: ").strip()

        if choice in ["1", "2", "3", "4", "5", "6"]:
            return choice

        print("Invalid choice! Please select between 1 and 6.")


# Create books.csv if it does not exist
def create_file():

    if not os.path.exists(BOOKS_FILE):

        with open(BOOKS_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=BOOK_FIELDS)
            writer.writeheader()


# Read book records
def read_books():

    with open(BOOKS_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


# Write book records
def write_books(books):

    with open(BOOKS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=BOOK_FIELDS)
        writer.writeheader()
        writer.writerows(books)


# 1. Add Book
def add_book():

    books = read_books()

    book_id = validate_book_id("Enter Book ID/ISBN: ")

    for book in books:

        if book["id/isbn"] == book_id:
            print("Book ID already exists!")
            return

    title = validate_text("Enter Book Title: ")
    author = validate_text("Enter Author Name: ")
    category = validate_text("Enter Category: ")

    count = validate_positive_count("Enter Number of Copies: ")

    new_book = {
        "id/isbn": book_id,
        "title": title,
        "author": author,
        "category": category,
        "count": str(count)
    }

    books.append(new_book)

    write_books(books)

    print("Book added successfully!")


# 2. Display Books
def display_books():

    books = read_books()

    if not books:
        print("No books found!")
        return

    print("\n========== BOOK RECORDS ==========")

    for book in books:

        print("\nBook ID:", book["id/isbn"])
        print("Title:", book["title"])
        print("Author:", book["author"])
        print("Category:", book["category"])
        print("Available Copies:", book["count"])

    print("==================================")


# 3. Search Book
def search_book():

    books = read_books()

    search = validate_text("Enter Book ID or Title: ").lower()

    found = False

    for book in books:

        if (book["id/isbn"].lower() == search or
                book["title"].lower() == search):

            print("\nBook Found!")

            print("Book ID:", book["id/isbn"])
            print("Title:", book["title"])
            print("Author:", book["author"])
            print("Category:", book["category"])
            print("Available Copies:", book["count"])

            found = True

    if not found:
        print("Book not found!")


# 4. Update Book
def update_book():

    books = read_books()

    book_id = validate_book_id("Enter Book ID to update: ")

    found = False

    for book in books:

        if book["id/isbn"] == book_id:

            found = True

            print("\nLeave a field blank to keep its old value.")

            title = input("Enter New Title: ").strip()
            author = input("Enter New Author: ").strip()
            category = input("Enter New Category: ").strip()

            if title:
                book["title"] = title

            if author:
                book["author"] = author

            if category:
                book["category"] = category

            new_count = validate_optional_count("Enter New Available Count: ")

            if new_count is not None:

                # Check currently issued copies
                records = read_records()

                issued = sum(
                    1 for record in records
                    if record["book_id"] == book_id
                    and record["date_of_return"].strip() == ""
                )

                if new_count < issued:
                    print("Count cannot be less than currently issued copies!")
                    return

                book["count"] = str(new_count)

            break

    if found:

        write_books(books)
        print("Book updated successfully!")

    else:
        print("Book not found!")


# Helper function to read transaction records
def read_records():

    if not os.path.exists(RECORDS_FILE):
        return []

    with open(RECORDS_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


# 5. Delete Book
def delete_book():

    books = read_books()

    book_id = validate_book_id("Enter Book ID to delete: ")

    found = False

    for book in books:

        if book["id/isbn"] == book_id:
            found = True
            break

    if not found:
        print("Book not found!")
        return

    # Check transaction history
    records = read_records()

    for record in records:

        if record["book_id"] == book_id:

            if record["date_of_return"].strip() == "":
                print("Cannot delete! This book is currently issued.")
                return

    books = [
        book for book in books
        if book["id/isbn"] != book_id
    ]

    write_books(books)

    print("Book deleted successfully!")


# Main Book Management Menu
def book_menu():

    create_file()

    while True:

        print("\n===== BOOK MANAGEMENT SYSTEM =====")
        print("1. Add Book")
        print("2. Display Books")
        print("3. Search Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("6. Exit")

        choice = validate_menu_choice()

        if choice == "1":
            add_book()

        elif choice == "2":
            display_books()

        elif choice == "3":
            search_book()

        elif choice == "4":
            update_book()

        elif choice == "5":
            delete_book()

        elif choice == "6":
            print("Exiting Book Management Module.")
            break


if __name__ == "__main__":
    book_menu()
