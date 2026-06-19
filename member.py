
from datetime import date


def is_valid_email(email: str) -> bool:
    """
    Perform a lightweight structural check on an email address.

    This is not a full RFC validator, but it catches the most common
    mistakes: missing '@', missing domain, missing '.', or stray
    whitespace inside the address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email passes the structural check,
              False otherwise.
    """
    email = email.strip()
    if email.count("@") != 1:
        return False
    if " " in email:
        return False
    local_part, domain_part = email.split("@")
    if not local_part or not domain_part:
        return False
    if "." not in domain_part:
        return False
    return True


class Member:
    """
    Represents a library member.

    Attributes:
        member_id (str): Unique identifier for the member.
        name (str): Full name of the member.
        email (str): Email address of the member.
        phone (str): Contact phone number.
        join_date (str): Date the member joined the library.
        borrowed_books (list): List of book IDs currently borrowed.
    """

    MAX_BORROW_LIMIT = 3  # Maximum books a member can borrow at once

    def __init__(self, member_id: str, name: str,
                 email: str, phone: str) -> None:
        """
        Initialise a Member instance.

        Args:
            member_id (str): Unique ID for the member.
            name (str): Full name of the member.
            email (str): Email address.
            phone (str): Contact phone number.
        """
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.join_date = str(date.today())  # Automatically set join date
        self.borrowed_books = []  # List of book IDs currently borrowed

    def borrow_book(self, book_id: str) -> bool:
        """
        Add a book ID to the member's borrowed list.

        Args:
            book_id (str): The ID of the book being borrowed.

        Returns:
            bool: True if successful, False if borrow limit reached.
        """
        if len(self.borrowed_books) >= self.MAX_BORROW_LIMIT:
            return False  # Borrow limit reached
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)
            return True
        return False

    def return_book(self, book_id: str) -> bool:
        """
        Remove a book ID from the member's borrowed list.

        Args:
            book_id (str): The ID of the book being returned.

        Returns:
            bool: True if successful, False if book was not borrowed.
        """
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False

    def get_borrowed_books(self) -> list:
        """
        Return the list of book IDs currently borrowed.

        Returns:
            list: List of borrowed book IDs.
        """
        return self.borrowed_books.copy()

    def update_contact(self, email: str = None, phone: str = None) -> None:
        """
        Update the member's contact information.

        Args:
            email (str, optional): New email address.
            phone (str, optional): New phone number.
        """
        if email:
            self.email = email
        if phone:
            self.phone = phone

    def get_details(self) -> dict:
        """
        Return all details of the member as a dictionary.

        Returns:
            dict: Dictionary containing all member attributes.
        """
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "join_date": self.join_date,
            "borrowed_books": ";".join(self.borrowed_books),
        }

    def display(self) -> None:
        """Print a formatted summary of the member's details."""
        print(f"  [{self.member_id}] {self.name} | Email: {self.email} "
              f"| Phone: {self.phone} | Joined: {self.join_date} "
              f"| Books Borrowed: {len(self.borrowed_books)}/{self.MAX_BORROW_LIMIT}")

    def __str__(self) -> str:
        """Return string representation of the Member."""
        return (f"Member({self.member_id}, '{self.name}', "
                f"Email: {self.email}, Borrowed: {self.borrowed_books})")

    def __repr__(self) -> str:
        """Return official string representation."""
        return self.__str__()
