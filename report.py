
import csv


# Validate menu choice
def validate_menu_choice():

    while True:
        choice = input("Enter your choice: ").strip()

        if choice in ["1", "2", "3"]:
            return choice

        print("Invalid choice! Please select between 1 and 3.")


def generate_statistics():

    # Calculate total books
    with open("books.csv", "r") as file:
        reader = csv.DictReader(file)

        total_books = 0

        for row in reader:
            total_books += int(row["count"])

    # Calculate currently issued books
    with open("records.csv", "r") as file:
        reader = csv.DictReader(file)

        issued_books = 0

        for row in reader:
            if row["date_of_return"].strip() == "":
                issued_books += 1

    # Calculate available books
    available_books = total_books - issued_books

    print("\n===== LIBRARY STATISTICS =====")
    print("Total books:", total_books)
    print("Issued books:", issued_books)
    print("Available books:", available_books)


def generate_report():

    # Read books
    with open("books.csv", "r") as file:
        books = list(csv.DictReader(file))

    total_titles = len(books)
    total_books = sum(int(book["count"]) for book in books)

    # Create book ID mappings
    book_category = {}
    book_title = {}

    for book in books:
        book_id = book["id/isbn"]
        book_category[book_id] = book["category"]
        book_title[book_id] = book["title"]

    # Read records
    with open("records.csv", "r") as file:
        records = list(csv.DictReader(file))

    issued_books = 0
    overdue_books = 0
    total_fine = 0

    borrow_count = {}
    category_count = {}

    for row in records:

        book_id = row["book_id"]

        # Currently issued books
        if row["date_of_return"].strip() == "":
            issued_books += 1

        # Overdue transactions
        if row["Is_Overdue"].strip().lower() == "true":
            overdue_books += 1

        # Total fines
        total_fine += float(row["fine"] or 0)

        # Count book borrowing frequency
        borrow_count[book_id] = borrow_count.get(book_id, 0) + 1

        # Count category borrowing frequency
        category = book_category.get(book_id)

        if category is not None:
            category_count[category] = category_count.get(category, 0) + 1

    available_books = total_books - issued_books

    # Read users
    with open("users.csv", "r") as file:
        users = list(csv.DictReader(file))

    total_members = len(users)

    # Display report
    print("\n========== LIBRARY SUMMARY REPORT ==========")

    print("Total book titles:", total_titles)
    print("Total physical books:", total_books)
    print("Available books:", available_books)
    print("Issued books:", issued_books)

    print("\nTotal registered members:", total_members)
    print("Overdue transactions:", overdue_books)
    print("Total fines recorded: Rs.", total_fine)

    # Most borrowed books
    print("\n------ MOST BORROWED BOOKS ------")

    if borrow_count:
        max_borrow = max(borrow_count.values())

        for book_id, count in borrow_count.items():
            if count == max_borrow:
                print(book_title.get(book_id, book_id),
                      "-", count, "borrowings")
    else:
        print("No borrowing records found.")

    # Most popular categories
    print("\n------ POPULAR CATEGORIES ------")

    if category_count:
        max_category = max(category_count.values())

        for category, count in category_count.items():
            if count == max_category:
                print(category, "-", count, "borrowings")
    else:
        print("No category borrowing records found.")

    print("\n============================================")


def library_stats_menu():

    while True:

        print("\n===== LIBRARY STATISTICS & REPORT MODULE =====")
        print("1. View Library Statistics")
        print("2. Generate Library Summary Report")
        print("3. Exit")

        choice = validate_menu_choice()

        if choice == "1":
            generate_statistics()

        elif choice == "2":
            generate_report()

        elif choice == "3":
            print("Exiting Library Statistics & Report Module.")
            break


if __name__ == "__main__":
    library_stats_menu()
