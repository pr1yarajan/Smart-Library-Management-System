import csv
import os

from book_management import book_menu
from member_management import member_menu
from fine import fine_menu
from recommendation import recommendation_menu
from report import library_stats_menu


def initialize_csv_files():

    # Create books.csv if it does not exist
    if not os.path.exists("books.csv"):
        with open("books.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id/isbn", "title", "author", "category", "count"])

    # Create users.csv if it does not exist
    if not os.path.exists("users.csv"):
        with open("users.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "contact", "date_of_joining", "email"])

    # Create records.csv if it does not exist
    if not os.path.exists("records.csv"):
        with open("records.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "member_id", "book_id", "date_of_issue",
                "date_of_return", "Is_Overdue", "fine"
            ])

# Validate main menu choice
def validate_menu_choice():

    while True:
        choice = input("\nEnter your choice: ").strip()

        if choice in ["1", "2", "3", "4", "5", "6"]:
            return choice

        print("\nInvalid choice! Please enter a number from 1 to 6.")


def main():

    while True:

        print("\n====================================")
        print("     LIBRARY MANAGEMENT SYSTEM")
        print("====================================")

        print("1. Book Management and Issue / Return")
        print("2. Member Management")
        print("3. Fine Management")
        print("4. Book Recommendations")
        print("5. Library Statistics and Reports")
        print("6. Exit")

        choice = validate_menu_choice()

        if choice == "1":
            book_menu()

        elif choice == "2":
            member_menu()

        elif choice == "3":
            fine_menu()

        elif choice == "4":
            recommendation_menu()

        elif choice == "5":
            library_stats_menu()

        elif choice == "6":
            print("\nThank you for using Library Management System!")
            break


# Program execution starts here

if __name__ == "__main__":
    main()
