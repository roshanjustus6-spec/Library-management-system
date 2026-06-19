"""
transaction.py
--------------
Module containing the Transaction class for the Library Management System.
Tracks all borrow and return events in the library.

Institution: Gisma University of Applied Sciences
"""

from datetime import datetime


class Transaction:
    """
    Represents a single borrow or return transaction in the library.

    Attributes:
        transaction_id (str): Unique identifier for the transaction.
        book_id (str): ID of the book involved.
        member_id (str): ID of the member involved.
        staff_id (str): ID of the librarian who processed the transaction.
        transaction_type (str): Either 'BORROW' or 'RETURN'.
        timestamp (str): Date and time the transaction occurred.
    """

    def __init__(self, transaction_id: str, book_id: str,
                 member_id: str, staff_id: str,
                 transaction_type: str) -> None:
        """
        Initialise a Transaction instance.

        Args:
            transaction_id (str): Unique ID for the transaction.
            book_id (str): ID of the book involved.
            member_id (str): ID of the member involved.
            staff_id (str): ID of the librarian who processed it.
            transaction_type (str): 'BORROW' or 'RETURN'.

        Raises:
            ValueError: If transaction_type is not 'BORROW' or 'RETURN'.
        """
        if transaction_type not in ("BORROW", "RETURN"):
            raise ValueError(
                f"Invalid transaction type '{transaction_type}'. "
                "Must be 'BORROW' or 'RETURN'."
            )
        self.transaction_id = transaction_id
        self.book_id = book_id
        self.member_id = member_id
        self.staff_id = staff_id
        self.transaction_type = transaction_type
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_details(self) -> dict:
        """
        Return all transaction details as a dictionary.

        Returns:
            dict: Dictionary of all transaction attributes.
        """
        return {
            "transaction_id": self.transaction_id,
            "book_id": self.book_id,
            "member_id": self.member_id,
            "staff_id": self.staff_id,
            "transaction_type": self.transaction_type,
            "timestamp": self.timestamp,
        }

    def is_borrow(self) -> bool:
        """
        Check if this transaction is a borrow event.

        Returns:
            bool: True if BORROW, False otherwise.
        """
        return self.transaction_type == "BORROW"

    def is_return(self) -> bool:
        """
        Check if this transaction is a return event.

        Returns:
            bool: True if RETURN, False otherwise.
        """
        return self.transaction_type == "RETURN"

    def get_summary(self) -> str:
        """
        Return a human-readable one-line summary of the transaction.

        Returns:
            str: Summary string.
        """
        action = "borrowed" if self.is_borrow() else "returned"
        return (f"[{self.transaction_id}] Member {self.member_id} {action} "
                f"Book {self.book_id} at {self.timestamp} "
                f"(Processed by Staff {self.staff_id})")

    def display(self) -> None:
        """Print the transaction summary to the console."""
        print(f"  {self.get_summary()}")

    def __str__(self) -> str:
        """Return string representation of the Transaction."""
        return (f"Transaction({self.transaction_id}, "
                f"Type: {self.transaction_type}, "
                f"Book: {self.book_id}, Member: {self.member_id})")

    def __repr__(self) -> str:
        """Return official string representation."""
        return self.__str__()
