"""
file_handler.py
---------------
Module for all file input/output operations in the Library Management System.
Handles reading and writing of Books, Members, Librarians, and Transactions
using CSV files for persistent data storage.
Institution: Gisma University of Applied Sciences
"""

import csv
import os

from book import Book
from member import Member
from librarian import Librarian
from transaction import Transaction

# ── File paths for all data files ────────────────────────────────────────────
BOOKS_FILE = "data/books.csv"
MEMBERS_FILE = "data/members.csv"
LIBRARIANS_FILE = "data/librarians.csv"
TRANSACTIONS_FILE = "data/transactions.csv"

# ── CSV column headers ────────────────────────────────────────────────────────
BOOKS_HEADERS = ["book_id", "title", "author", "genre", "year", "is_available"]
MEMBERS_HEADERS = ["member_id", "name", "email", "phone",
                   "join_date", "borrowed_books"]
LIBRARIANS_HEADERS = ["staff_id", "name", "email"]
TRANSACTIONS_HEADERS = ["transaction_id", "book_id", "member_id",
                        "staff_id", "transaction_type", "timestamp"]


def ensure_data_directory() -> None:
    """
    Create the data/ directory if it does not already exist.
    This prevents FileNotFoundError when writing for the first time.
    """
    os.makedirs("data", exist_ok=True)


# ── Book I/O ──────────────────────────────────────────────────────────────────

def save_books(books: dict) -> None:
    """
    Write all Book objects to the books CSV file.

    Args:
        books (dict): Dictionary mapping book_id -> Book object.
    """
    ensure_data_directory()
    try:
        with open(BOOKS_FILE, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=BOOKS_HEADERS)
            writer.writeheader()
            for book in books.values():
                writer.writerow(book.get_details())
    except IOError as error:
        print(f"  [ERROR] Could not save books to disk: {error}")
        print("  [WARNING] This change exists only in memory and will "
              "be lost when the program closes.")


def load_books() -> dict:
    """
    Read all Book records from the books CSV file.

    Returns:
        dict: Dictionary mapping book_id -> Book object.
              Returns an empty dict if the file does not exist.
    """
    books = {}
    ensure_data_directory()
    try:
        with open(BOOKS_FILE, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                book = Book(
                    book_id=row["book_id"],
                    title=row["title"],
                    author=row["author"],
                    genre=row["genre"],
                    year=int(row["year"]),
                )
                # Restore availability from file
                book.is_available = row["is_available"].strip().lower() == "true"
                books[book.book_id] = book
    except FileNotFoundError:
        # First run: no file exists yet — return empty dict
        pass
    except (IOError, KeyError, ValueError) as error:
        print(f"  [ERROR] Could not load books: {error}")
    return books


# ── Member I/O ────────────────────────────────────────────────────────────────

def save_members(members: dict) -> None:
    """
    Write all Member objects to the members CSV file.

    Args:
        members (dict): Dictionary mapping member_id -> Member object.
    """
    ensure_data_directory()
    try:
        with open(MEMBERS_FILE, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=MEMBERS_HEADERS)
            writer.writeheader()
            for member in members.values():
                writer.writerow(member.get_details())
    except IOError as error:
        print(f"  [ERROR] Could not save members to disk: {error}")
        print("  [WARNING] This change exists only in memory and will "
              "be lost when the program closes.")


def load_members() -> dict:
    """
    Read all Member records from the members CSV file.

    Returns:
        dict: Dictionary mapping member_id -> Member object.
              Returns an empty dict if the file does not exist.
    """
    members = {}
    ensure_data_directory()
    try:
        with open(MEMBERS_FILE, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                member = Member(
                    member_id=row["member_id"],
                    name=row["name"],
                    email=row["email"],
                    phone=row["phone"],
                )
                # Restore join date and borrowed books from file
                member.join_date = row["join_date"]
                raw_borrowed = row["borrowed_books"].strip()
                if raw_borrowed:
                    member.borrowed_books = raw_borrowed.split(";")
                members[member.member_id] = member
    except FileNotFoundError:
        pass
    except (IOError, KeyError) as error:
        print(f"  [ERROR] Could not load members: {error}")
    return members


# ── Librarian I/O ─────────────────────────────────────────────────────────────

def save_librarians(librarians: dict) -> None:
    """
    Write all Librarian objects to the librarians CSV file.

    Args:
        librarians (dict): Dictionary mapping staff_id -> Librarian object.
    """
    ensure_data_directory()
    try:
        with open(LIBRARIANS_FILE, "w", newline="",
                  encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=LIBRARIANS_HEADERS)
            writer.writeheader()
            for librarian in librarians.values():
                writer.writerow(librarian.get_details())
    except IOError as error:
        print(f"  [ERROR] Could not save librarians to disk: {error}")
        print("  [WARNING] This change exists only in memory and will "
              "be lost when the program closes.")


def load_librarians() -> dict:
    """
    Read all Librarian records from the librarians CSV file.

    Returns:
        dict: Dictionary mapping staff_id -> Librarian object.
              Returns an empty dict if the file does not exist.
    """
    librarians = {}
    ensure_data_directory()
    try:
        with open(LIBRARIANS_FILE, "r", newline="",
                  encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                librarian = Librarian(
                    staff_id=row["staff_id"],
                    name=row["name"],
                    email=row["email"],
                )
                librarians[librarian.staff_id] = librarian
    except FileNotFoundError:
        pass
    except (IOError, KeyError) as error:
        print(f"  [ERROR] Could not load librarians: {error}")
    return librarians


# ── Transaction I/O ───────────────────────────────────────────────────────────

def save_transactions(transactions: list) -> None:
    """
    Write all Transaction objects to the transactions CSV file.

    Args:
        transactions (list): List of Transaction objects.
    """
    ensure_data_directory()
    try:
        with open(TRANSACTIONS_FILE, "w", newline="",
                  encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=TRANSACTIONS_HEADERS)
            writer.writeheader()
            for txn in transactions:
                writer.writerow(txn.get_details())
    except IOError as error:
        print(f"  [ERROR] Could not save transactions to disk: {error}")
        print("  [WARNING] This transaction exists only in memory and "
              "will be lost when the program closes.")


def load_transactions() -> list:
    """
    Read all Transaction records from the transactions CSV file.

    Returns:
        list: List of Transaction objects.
              Returns an empty list if the file does not exist.
    """
    transactions = []
    ensure_data_directory()
    try:
        with open(TRANSACTIONS_FILE, "r", newline="",
                  encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                txn = Transaction(
                    transaction_id=row["transaction_id"],
                    book_id=row["book_id"],
                    member_id=row["member_id"],
                    staff_id=row["staff_id"],
                    transaction_type=row["transaction_type"],
                )
                # Restore original timestamp from file
                txn.timestamp = row["timestamp"]
                transactions.append(txn)
    except FileNotFoundError:
        pass
    except (IOError, KeyError, ValueError) as error:
        print(f"  [ERROR] Could not load transactions: {error}")
    return transactions
