"""
book.py
-------
Module containing the Book class for the Library Management System.
Institution: Gisma University of Applied Sciences
"""


class Book:
    """
    Represents a book in the library.

    Attributes:
        book_id (str): Unique identifier for the book.
        title (str): Title of the book.
        author (str): Author of the book.
        genre (str): Genre/category of the book.
        year (int): Publication year.
        is_available (bool): Availability status of the book.
    """

    def __init__(self, book_id: str, title: str, author: str,
                 genre: str, year: int) -> None:
        """
        Initialise a Book instance.

        Args:
            book_id (str): Unique ID for the book.
            title (str): Title of the book.
            author (str): Author of the book.
            genre (str): Genre of the book.
            year (int): Publication year.
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.is_available = True  # All books available on creation

    def get_details(self) -> dict:
        """
        Return all details of the book as a dictionary.

        Returns:
            dict: A dictionary containing all book attributes.
        """
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "year": self.year,
            "is_available": self.is_available,
        }

    def mark_as_borrowed(self) -> bool:
        """
        Mark the book as borrowed (unavailable).

        Returns:
            bool: True if successfully marked borrowed, False if already borrowed.
        """
        if self.is_available:
            self.is_available = False
            return True
        return False

    def mark_as_returned(self) -> bool:
        """
        Mark the book as returned (available).

        Returns:
            bool: True if successfully returned, False if already available.
        """
        if not self.is_available:
            self.is_available = True
            return True
        return False

    def update_details(self, title: str = None, author: str = None,
                       genre: str = None, year: int = None) -> None:
        """
        Update one or more details of the book.

        Args:
            title (str, optional): New title.
            author (str, optional): New author.
            genre (str, optional): New genre.
            year (int, optional): New publication year.
        """
        if title:
            self.title = title
        if author:
            self.author = author
        if genre:
            self.genre = genre
        if year:
            self.year = year

    def display(self) -> None:
        """Print a formatted summary of the book's details."""
        status = "Available" if self.is_available else "Borrowed"
        print(f"  [{self.book_id}] '{self.title}' by {self.author} "
              f"| Genre: {self.genre} | Year: {self.year} | Status: {status}")

    def __str__(self) -> str:
        """Return string representation of the Book."""
        return (f"Book({self.book_id}, '{self.title}', "
                f"Author: {self.author}, Available: {self.is_available})")

    def __repr__(self) -> str:
        """Return official string representation."""
        return self.__str__()
