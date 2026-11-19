
import csv
from datetime import date


BOOKS_FILE = "books.csv"
RECORDS_FILE = "records.csv"


BOOK_FIELDS = ["id/isbn", "title", "author", "category", "count"]

RECORD_FIELDS = [
    "member_id", "book_id", "date_of_issue",
    "date_of_return", "Is_Overdue", "fine"
]


FINE_PER_DAY = 5
ALLOWED_DAYS = 14


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


# Validate menu choice
def validate_menu_choice():

    while True:
        choice = input("Enter your choice: ").strip()

        if choice in ["1", "2", "3"]:
            return choice

        print("Invalid choice! Please select between 1 and 3.")


def read_data(filename):

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_data(filename, fields, data):

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def calculate_fine():

    records = read_data(RECORDS_FILE)

    member_id = validate_text("Enter Member ID: ")
    book_id = validate_book_id("Enter Book ID/ISBN: ")

    selected_record = None

    for record in records:

        if (record["member_id"] == member_id
                and record["book_id"] == book_id
                and record["date_of_return"] == ""):

            selected_record = record
            break

    if selected_record is None:
        print("No active issue record found!")
        return

    issue_date = date.fromisoformat(
        selected_record["date_of_issue"]
    )

    today = date.today()

    days_borrowed = (today - issue_date).days

    overdue_days = days_borrowed - ALLOWED_DAYS

    if overdue_days <= 0:

        selected_record["Is_Overdue"] = "No"
        selected_record["fine"] = "0"

        write_data(RECORDS_FILE, RECORD_FIELDS, records)

        print("No fine is applicable.")
        print("Days borrowed:", days_borrowed)
        print("Fine: Rs. 0")
        return

    fine_amount = overdue_days * FINE_PER_DAY

    selected_record["Is_Overdue"] = "Yes"
    selected_record["fine"] = str(fine_amount)

    write_data(RECORDS_FILE, RECORD_FIELDS, records)

    print("Fine calculated successfully!")
    print("Issue Date:", selected_record["date_of_issue"])
    print("Days Borrowed:", days_borrowed)
    print("Overdue Days:", overdue_days)
    print("Fine Per Day: Rs.", FINE_PER_DAY)
    print("Total Fine: Rs.", fine_amount)


def view_overdue_books():

    records = read_data(RECORDS_FILE)

    overdue_found = False

    print("\n===== OVERDUE BOOKS =====")

    for record in records:

        if record["date_of_return"] == "":

            issue_date = date.fromisoformat(
                record["date_of_issue"]
            )

            today = date.today()

            days_borrowed = (today - issue_date).days

            overdue_days = days_borrowed - ALLOWED_DAYS

            if overdue_days > 0:

                overdue_found = True

                print("Member ID:", record["member_id"])
                print("Book ID/ISBN:", record["book_id"])
                print("Issue Date:", record["date_of_issue"])
                print("Overdue Days:", overdue_days)
                print("Fine: Rs.", overdue_days * FINE_PER_DAY)
                print("-" * 30)

    if not overdue_found:
        print("No overdue books found!")


def fine_menu():

    while True:

        print("\n===== FINE CALCULATION MODULE =====")
        print("1. Calculate Fine")
        print("2. View Overdue Books")
        print("3. Exit")

        choice = validate_menu_choice()

        if choice == "1":
            calculate_fine()

        elif choice == "2":
            view_overdue_books()

        elif choice == "3":
            print("Exiting Fine Calculation Module.")
            break


if __name__ == "__main__":
    fine_menu()
