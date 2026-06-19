"""
librarian.py
------------
Module containing the Librarian class for the Library Management System.

Institution: Gisma University of Applied Sciences
"""

from datetime import datetime


class Librarian:
    """
    Represents a librarian (staff member) of the library.

    Attributes:
        staff_id (str): Unique identifier for the librarian.
        name (str): Full name of the librarian.
        email (str): Work email address.
        actions_log (list): Log of all actions performed by this librarian.
    """

    def __init__(self, staff_id: str, name: str, email: str) -> None:
        """
        Initialise a Librarian instance.

        Args:
            staff_id (str): Unique staff ID.
            name (str): Full name.
            email (str): Work email.
        """
        self.staff_id = staff_id
        self.name = name
        self.email = email
        self.actions_log = []  # Simple in-memory record of actions taken

    def log_action(self, action: str) -> None:
        """
        Record an action performed by this librarian with a timestamp.
        This stays in memory only — it is a lightweight internal audit
        trail, not persisted to disk.

        Args:
            action (str): Description of the action performed.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {self.name} (ID: {self.staff_id}): {action}"
        self.actions_log.append(entry)

    def get_action_log(self) -> list:
        """
        Return a copy of all logged actions.

        Returns:
            list: List of action log strings.
        """
        return self.actions_log.copy()

    def display_log(self) -> None:
        """Print all logged actions to the console."""
        if not self.actions_log:
            print("  No actions logged yet.")
            return
        for entry in self.actions_log:
            print(f"  {entry}")

    def update_email(self, new_email: str) -> None:
        """
        Update the librarian's email address.

        Args:
            new_email (str): The new email address.
        """
        old_email = self.email
        self.email = new_email
        self.log_action(f"Email updated from '{old_email}' to '{new_email}'.")

    def get_details(self) -> dict:
        """
        Return all details of the librarian as a dictionary.

        Returns:
            dict: Dictionary containing all librarian attributes.
        """
        return {
            "staff_id": self.staff_id,
            "name": self.name,
            "email": self.email,
        }

    def display(self) -> None:
        """Print a formatted summary of the librarian's details."""
        print(f"  [{self.staff_id}] {self.name} | Email: {self.email} "
              f"| Actions Logged: {len(self.actions_log)}")

    def __str__(self) -> str:
        """Return string representation of the Librarian."""
        return (f"Librarian({self.staff_id}, '{self.name}', "
                f"Email: {self.email})")

    def __repr__(self) -> str:
        """Return official string representation."""
        return self.__str__()
