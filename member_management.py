
import csv
import re
from datetime import date




# Validate non-empty text
def validate_text(prompt):

    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty!")


# Validate 10-digit phone number
def validate_phone(prompt):

    while True:
        phone = input(prompt).strip()

        if phone.isdigit() and len(phone) == 10:
            return phone

        print("Phone number must contain exactly 10 digits!")


# Validate email format
def validate_email(prompt):

    while True:
        email = input(prompt).strip()

        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return email

        print("Please enter a valid email address!")


# Validate 13-digit book ID
def validate_book_id(prompt):

    while True:
        book_id = input(prompt).strip()

        if book_id.isdigit() and len(book_id) == 13:
            return book_id

        print("Book ID must contain exactly 13 digits!")


# Validate menu choice
def validate_menu_choice():

    while True:
        choice = input("Enter your choice: ").strip()

        if choice in ["1", "2", "3", "4", "5"]:
            return choice

        print("Invalid choice! Please select between 1 and 5.")


BOOKS_FILE = "books.csv"
USERS_FILE = "users.csv"
RECORDS_FILE = "records.csv"


BOOK_FIELDS = ["id/isbn", "title", "author", "category", "count"]

USER_FIELDS = [
    "id", "name", "contact", "date_of_joining", "email"
]

RECORD_FIELDS = [
    "member_id", "book_id", "date_of_issue",
    "date_of_return", "Is_Overdue", "fine"
]

FINE_PER_DAY = 5
ALLOWED_DAYS = 14


def initialize_files():

    files = [
        (BOOKS_FILE, BOOK_FIELDS),
        (USERS_FILE, USER_FIELDS),
        (RECORDS_FILE, RECORD_FIELDS)
    ]

    for filename, fields in files:
        try:
            with open(filename, "x", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()

        except FileExistsError:
            pass


def read_data(filename):

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_data(filename, fields, data):

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def add_member():

    members = read_data(USERS_FILE)

    member_id = validate_text("Enter Member ID: ")

    for member in members:
        if member["id"] == member_id:
            print("Member ID already exists!")
            return

    name = validate_text("Enter Member Name: ")
    contact = validate_phone("Enter Contact Number: ")
    email = validate_email("Enter Email: ")

    if not all([member_id, name, contact, email]):
        print("All fields are required!")
        return

    new_member = {
        "id": member_id,
        "name": name,
        "contact": contact,
        "date_of_joining": date.today().isoformat(),
        "email": email
    }

    members.append(new_member)

    write_data(USERS_FILE, USER_FIELDS, members)

    print("Member added successfully!")


def search_member():

    members = read_data(USERS_FILE)

    member_id = validate_text("Enter Member ID to search: ")

    for member in members:

        if member["id"] == member_id:

            print("\nMember Found!")
            print("Member ID:", member["id"])
            print("Name:", member["name"])
            print("Contact:", member["contact"])
            print("Date of Joining:", member["date_of_joining"])
            print("Email:", member["email"])

            return member

    print("Member not found!")
    return None


def issue_book():

    members = read_data(USERS_FILE)
    books = read_data(BOOKS_FILE)
    records = read_data(RECORDS_FILE)

    member_id = validate_text("Enter Member ID: ")
    book_id = validate_book_id("Enter Book ID/ISBN: ")

    # Check whether member exists
    member_exists = False

    for member in members:
        if member["id"] == member_id:
            member_exists = True
            break

    if not member_exists:
        print("Member does not exist!")
        return

    # Find the selected book
    selected_book = None

    for book in books:
        if book["id/isbn"] == book_id:
            selected_book = book
            break

    if selected_book is None:
        print("Book not found!")
        return

    # Check book availability
    if int(selected_book["count"]) <= 0:
        print("Book is currently unavailable!")
        return

    # Check whether member already has this book
    for record in records:

        if (record["member_id"] == member_id
                and record["book_id"] == book_id
                and record["date_of_return"] == ""):

            print("This member already has this book!")
            return

    # Decrease available book count
    selected_book["count"] = str(
        int(selected_book["count"]) - 1
    )

    # Create new issue record
    new_record = {
        "member_id": member_id,
        "book_id": book_id,
        "date_of_issue": date.today().isoformat(),
        "date_of_return": "",
        "Is_Overdue": "",
        "fine": ""
    }

    records.append(new_record)

    # Save updated data
    write_data(BOOKS_FILE, BOOK_FIELDS, books)
    write_data(RECORDS_FILE, RECORD_FIELDS, records)

    print("Book issued successfully!")
    print("Issue Date:", date.today())


def return_book():

    books = read_data(BOOKS_FILE)
    records = read_data(RECORDS_FILE)

    member_id = validate_text("Enter Member ID: ")
    book_id = validate_book_id("Enter Book ID/ISBN: ")

    active_record = None

    # Find active issue record
    for record in records:

        if (record["member_id"] == member_id
                and record["book_id"] == book_id
                and record["date_of_return"] == ""):

            active_record = record
            break

    if active_record is None:
        print("No active issue record found!")
        return

    # Calculate borrowing and overdue days
    issue_date = date.fromisoformat(
        active_record["date_of_issue"]
    )

    return_date = date.today()

    days_borrowed = (return_date - issue_date).days

    overdue_days = days_borrowed - ALLOWED_DAYS

    # Calculate fine
    if overdue_days > 0:

        fine_amount = overdue_days * FINE_PER_DAY
        active_record["Is_Overdue"] = "Yes"
        active_record["fine"] = str(fine_amount)

    else:

        fine_amount = 0
        active_record["Is_Overdue"] = "No"
        active_record["fine"] = "0"

    # Update return date
    active_record["date_of_return"] = return_date.isoformat()

    # Increase available book count
    for book in books:

        if book["id/isbn"] == book_id:

            book["count"] = str(
                int(book["count"]) + 1
            )
            break

    # Save updated records and books
    write_data(RECORDS_FILE, RECORD_FIELDS, records)
    write_data(BOOKS_FILE, BOOK_FIELDS, books)

    # Display return and fine details
    print("\nBook returned successfully!")
    print("Issue Date:", issue_date)
    print("Return Date:", return_date)
    print("Days Borrowed:", days_borrowed)

    if overdue_days > 0:
        print("Overdue Days:", overdue_days)
        print("Fine Per Day: Rs.", FINE_PER_DAY)
        print("Total Fine: Rs.", fine_amount)

    else:
        print("Book returned within the allowed period.")
        print("Fine: Rs. 0")


def member_menu():

    initialize_files()

    while True:

        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add Member")
        print("2. Search Member")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Exit")

        choice = validate_menu_choice()

        if choice == "1":
            add_member()

        elif choice == "2":
            search_member()

        elif choice == "3":
            issue_book()

        elif choice == "4":
            return_book()

        elif choice == "5":
            print("Exiting Member Management Module.")
            break


if __name__ == "__main__":
    member_menu()
