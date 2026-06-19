"""
library.py
----------
Module containing the Library class — the central controller of the
Library Management System. Coordinates Books, Members, Librarians,
and Transactions.

Institution: Gisma University of Applied Sciences
"""

import file_handler
import os
from datetime import date
from book import Book
from member import Member, is_valid_email
from librarian import Librarian
from transaction import Transaction


class Library:
    """
    Central controller class for the Library Management System.

    Manages all books, members, librarians, and transactions.
    Loads data from CSV files on startup and saves after every change.

    Attributes:
        name (str): Name of the library.
        books (dict): All books stored as {book_id: Book}.
        members (dict): All members stored as {member_id: Member}.
        librarians (dict): All librarians stored as {staff_id: Librarian}.
        transactions (list): All transaction records.
        _book_counter (int): Auto-increment counter for book IDs.
        _member_counter (int): Auto-increment counter for member IDs.
        _txn_counter (int): Auto-increment counter for transaction IDs.
    """

    def __init__(self, name: str) -> None:
        """
        Initialise the Library and load all existing data from CSV files.

        Args:
            name (str): The name of the library.
        """
        self.name = name
        # Load persisted data from CSV files
        self.books = file_handler.load_books()
        self.members = file_handler.load_members()
        self.librarians = file_handler.load_librarians()
        self.transactions = file_handler.load_transactions()
        # Set counters based on existing data to avoid ID collisions
        self._book_counter = self._get_max_id(self.books, "B") + 1
        self._member_counter = self._get_max_id(self.members, "M") + 1
        self._txn_counter = len(self.transactions) + 1

        # Seed a default librarian if none exist
        if not self.librarians:
            self._seed_default_librarian()

    # ── Private Helpers ───────────────────────────────────────────────────

    def _get_max_id(self, data: dict, prefix: str) -> int:
        """
        Extract the highest numeric suffix from existing IDs.

        Args:
            data (dict): The dictionary to inspect (books or members).
            prefix (str): The ID prefix character ('B' or 'M').

        Returns:
            int: The highest numeric suffix found, or 0 if none.
        """
        max_num = 0
        for key in data:
            try:
                num = int(key.replace(prefix, ""))
                if num > max_num:
                    max_num = num
            except ValueError:
                continue
        return max_num

    def _generate_book_id(self) -> str:
        """Generate a unique book ID in the format B001, B002, etc."""
        book_id = f"B{self._book_counter:03d}"
        self._book_counter += 1
        return book_id

    def _generate_member_id(self) -> str:
        """Generate a unique member ID in the format M001, M002, etc."""
        member_id = f"M{self._member_counter:03d}"
        self._member_counter += 1
        return member_id

    def _generate_txn_id(self) -> str:
        """Generate a unique transaction ID in the format T0001, T0002, etc."""
        txn_id = f"T{self._txn_counter:04d}"
        self._txn_counter += 1
        return txn_id

    def _get_active_librarian(self) -> Librarian:
        """
        Return the first available librarian for logging purposes.

        Returns:
            Librarian: The first librarian in the dictionary.
        """
        return next(iter(self.librarians.values()))

    def _seed_default_librarian(self) -> None:
        """Create a default librarian when the system starts for the first time."""
        default = Librarian("S001", "Admin Librarian", "admin@library.com")
        self.librarians[default.staff_id] = default
        file_handler.save_librarians(self.librarians)

    # ── Book Management ─────────────────────────────────────────────────

    def add_book(self, title: str, author: str,
                 genre: str, year: int) -> Book:
        """
        Add a new book to the library catalogue.

        Args:
            title (str): Title of the book.
            author (str): Author of the book.
            genre (str): Genre/category.
            year (int): Publication year.

        Returns:
            Book: The newly created Book object.

        Raises:
            ValueError: If title/author is empty, or year is outside
                a realistic range (1000 to the current year).
        """
        if not title.strip() or not author.strip():
            raise ValueError("Book title and author cannot be empty.")

        current_year = date.today().year
        if year < 1000 or year > current_year:
            raise ValueError(
                f"Publication year must be between 1000 and {current_year}."
            )

        book_id = self._generate_book_id()
        new_book = Book(book_id, title.strip(), author.strip(),
                        genre.strip(), year)
        self.books[book_id] = new_book
        file_handler.save_books(self.books)

        librarian = self._get_active_librarian()
        librarian.log_action(f"Added book '{title}' (ID: {book_id}).")
        return new_book

    def remove_book(self, book_id: str) -> bool:
        """
        Remove a book from the library catalogue by its ID.

        Args:
            book_id (str): The ID of the book to remove.

        Returns:
            bool: True if removed successfully.

        Raises:
            KeyError: If the book_id does not exist.
            ValueError: If the book is currently borrowed.
        """
        if book_id not in self.books:
            raise KeyError(f"Book ID '{book_id}' not found.")

        book = self.books[book_id]
        if not book.is_available:
            raise ValueError(
                f"Cannot remove '{book.title}' — it is currently borrowed."
            )

        del self.books[book_id]
        file_handler.save_books(self.books)

        librarian = self._get_active_librarian()
        librarian.log_action(f"Removed book ID '{book_id}'.")
        return True

    def search_books(self, keyword: str) -> list:
        """
        Search books by title, author, or genre (case-insensitive).

        Args:
            keyword (str): Search term.

        Returns:
            list: List of matching Book objects.
        """
        keyword_lower = keyword.lower()
        results = []
        for book in self.books.values():
            if (keyword_lower in book.title.lower()
                    or keyword_lower in book.author.lower()
                    or keyword_lower in book.genre.lower()):
                results.append(book)
        return results

    def get_all_books(self) -> list:
        """
        Return all books in the catalogue.

        Returns:
            list: List of all Book objects.
        """
        return list(self.books.values())

    # ── Member Management ───────────────────────────────────────────────

    def register_member(self, name: str, email: str, phone: str) -> Member:
        """
        Register a new library member.

        Args:
            name (str): Full name of the member.
            email (str): Email address.
            phone (str): Contact phone number.

        Returns:
            Member: The newly created Member object.

        Raises:
            ValueError: If name/email is empty, or email fails the
                structural validity check (e.g. missing '@' or '.').
        """
        if not name.strip() or not email.strip():
            raise ValueError("Member name and email cannot be empty.")

        if not is_valid_email(email):
            raise ValueError(
                f"'{email}' is not a valid email address. "
                "Expected format: name@example.com"
            )

        member_id = self._generate_member_id()
        new_member = Member(member_id, name.strip(),
                            email.strip(), phone.strip())
        self.members[member_id] = new_member
        file_handler.save_members(self.members)

        librarian = self._get_active_librarian()
        librarian.log_action(
            f"Registered new member '{name}' (ID: {member_id})."
        )
        return new_member

    def remove_member(self, member_id: str) -> bool:
        """
        Remove a member from the library system.

        Args:
            member_id (str): The ID of the member to remove.

        Returns:
            bool: True if removed successfully.

        Raises:
            KeyError: If member_id does not exist.
            ValueError: If the member currently has borrowed books.
        """
        if member_id not in self.members:
            raise KeyError(f"Member ID '{member_id}' not found.")

        member = self.members[member_id]
        if member.borrowed_books:
            raise ValueError(
                f"Cannot remove '{member.name}' — they have "
                f"{len(member.borrowed_books)} book(s) still borrowed."
            )

        del self.members[member_id]
        file_handler.save_members(self.members)
        return True

    def search_members(self, keyword: str) -> list:
        """
        Search members by name or email (case-insensitive).

        Args:
            keyword (str): Search term.

        Returns:
            list: List of matching Member objects.
        """
        keyword_lower = keyword.lower()
        return [
            m for m in self.members.values()
            if keyword_lower in m.name.lower()
            or keyword_lower in m.email.lower()
        ]

    def get_all_members(self) -> list:
        """
        Return all registered members.

        Returns:
            list: List of all Member objects.
        """
        return list(self.members.values())

    # ── Borrow & Return ─────────────────────────────────────────────────

    def borrow_book(self, book_id: str, member_id: str) -> Transaction:
        """
        Process a book borrowing transaction.

        Args:
            book_id (str): The ID of the book to borrow.
            member_id (str): The ID of the member borrowing.

        Returns:
            Transaction: The completed borrow Transaction object.

        Raises:
            KeyError: If book or member ID does not exist.
            ValueError: If book is unavailable or member hit borrow limit.
        """
        if book_id not in self.books:
            raise KeyError(f"Book ID '{book_id}' not found.")
        if member_id not in self.members:
            raise KeyError(f"Member ID '{member_id}' not found.")

        book = self.books[book_id]
        member = self.members[member_id]

        if not book.is_available:
            raise ValueError(
                f"'{book.title}' is currently not available for borrowing."
            )
        if len(member.borrowed_books) >= member.MAX_BORROW_LIMIT:
            raise ValueError(
                f"'{member.name}' has reached the borrow limit "
                f"({member.MAX_BORROW_LIMIT} books)."
            )

        # Update book and member state
        book.mark_as_borrowed()
        member.borrow_book(book_id)

        # Record the transaction
        librarian = self._get_active_librarian()
        txn = Transaction(
            self._generate_txn_id(), book_id, member_id,
            librarian.staff_id, "BORROW"
        )
        self.transactions.append(txn)

        # Persist all changes
        file_handler.save_books(self.books)
        file_handler.save_members(self.members)
        file_handler.save_transactions(self.transactions)

        librarian.log_action(
            f"Member '{member.name}' borrowed '{book.title}'."
        )
        return txn

    def return_book(self, book_id: str, member_id: str) -> Transaction:
        """
        Process a book return transaction.

        Args:
            book_id (str): The ID of the book being returned.
            member_id (str): The ID of the member returning it.

        Returns:
            Transaction: The completed return Transaction object.

        Raises:
            KeyError: If book or member ID does not exist.
            ValueError: If the member did not borrow this book.
        """
        if book_id not in self.books:
            raise KeyError(f"Book ID '{book_id}' not found.")
        if member_id not in self.members:
            raise KeyError(f"Member ID '{member_id}' not found.")

        book = self.books[book_id]
        member = self.members[member_id]

        if book_id not in member.borrowed_books:
            raise ValueError(
                f"'{member.name}' did not borrow '{book.title}'."
            )

        # Update book and member state
        book.mark_as_returned()
        member.return_book(book_id)

        # Record the transaction
        librarian = self._get_active_librarian()
        txn = Transaction(
            self._generate_txn_id(), book_id, member_id,
            librarian.staff_id, "RETURN"
        )
        self.transactions.append(txn)

        # Persist all changes
        file_handler.save_books(self.books)
        file_handler.save_members(self.members)
        file_handler.save_transactions(self.transactions)

        librarian.log_action(
            f"Member '{member.name}' returned '{book.title}'."
        )
        return txn

    # ── Reports ─────────────────────────────────────────────────────────

    def get_transaction_history(self) -> list:
        """
        Return the full list of all transactions.

        Returns:
            list: List of all Transaction objects.
        """
        return self.transactions.copy()

    def get_statistics(self) -> dict:
        """
        Return basic summary statistics for the library.

        Returns:
            dict: Dictionary containing total/available/borrowed book
                counts, total members, and total transactions.
        """
        total_books = len(self.books)
        available = sum(1 for b in self.books.values() if b.is_available)
        borrowed = total_books - available
        total_members = len(self.members)
        total_transactions = len(self.transactions)

        return {
            "total_books": total_books,
            "available_books": available,
            "borrowed_books": borrowed,
            "total_members": total_members,
            "total_transactions": total_transactions,
        }

    def reset_all_data(self) -> None:
        """
        Permanently wipe every book, member, librarian, and
        transaction record, both in memory and on disk, then
        re-seed a default librarian so the system is immediately
        usable again without needing a restart.

        This is destructive and cannot be undone. If a CSV file is
        locked by another program (a common issue on Windows when
        the file is open in Excel), that one file is skipped with a
        warning instead of crashing the whole reset.
        """
        self.books = {}
        self.members = {}
        self.librarians = {}
        self.transactions = []
        self._book_counter = 1
        self._member_counter = 1
        self._txn_counter = 1

        data_files = [
            file_handler.BOOKS_FILE,
            file_handler.MEMBERS_FILE,
            file_handler.LIBRARIANS_FILE,
            file_handler.TRANSACTIONS_FILE,
        ]
        for data_file in data_files:
            try:
                if os.path.exists(data_file):
                    os.remove(data_file)
            except OSError as error:
                print(f"  [WARNING] Could not delete '{data_file}': {error}")
                print("  Close any program using this file and try again.")

    
        self._seed_default_librarian()
