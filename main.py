
from library import Library


# ── UI Helpers ────────────────────────────────────────────────────────────────

def print_banner() -> None:
    """Print the welcome banner for the application."""
    print("\n" + "=" * 60)
    print("       GISMA LIBRARY MANAGEMENT SYSTEM")
    print("=" * 60)


def print_divider() -> None:
    """Print a thin divider line."""
    print("-" * 60)


def pause() -> None:
    """Pause execution until the user presses Enter."""
    input("\n  Press Enter to continue...")


def get_input(prompt: str) -> str:
    """
    Prompt the user for input and strip surrounding whitespace.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        str: The cleaned user input string.
    """
    return input(f"  {prompt}").strip()


def get_int_input(prompt: str) -> int:
    """
    Prompt the user for an integer input, retrying on invalid input.

    Args:
        prompt (str): The message to display.

    Returns:
        int: A valid integer entered by the user.
    """
    while True:
        try:
            return int(get_input(prompt))
        except ValueError:
            print("  [ERROR] Please enter a valid number.")


# ── Sub-Menus ─────────────────────────────────────────────────────────────────

def book_menu(library: Library) -> None:
    """
    Display and handle the Book Management sub-menu.

    Args:
        library (Library): The active Library instance.
    """
    while True:
        print("\n  --- BOOK MANAGEMENT ---")
        print("  1. Add a New Book")
        print("  2. View All Books")
        print("  3. Search Books")
        print("  4. Remove a Book")
        print("  0. Back to Main Menu")
        print_divider()

        choice = get_input("Enter choice: ")

        if choice == "1":
            # ── Add Book ──────────────────────────────────────────────────
            print("\n  -- Add New Book --")
            title = get_input("Title: ")
            author = get_input("Author: ")
            genre = get_input("Genre: ")
            year = get_int_input("Publication Year: ")
            try:
                book = library.add_book(title, author, genre, year)
                print(f"\n  [SUCCESS] Book added successfully!")
                book.display()
            except ValueError as error:
                print(f"\n  [ERROR] {error}")

        elif choice == "2":
            # ── View All Books ────────────────────────────────────────────
            print("\n  -- All Books in Catalogue --")
            books = library.get_all_books()
            if not books:
                print("  No books found in the catalogue.")
            else:
                for book in books:
                    book.display()
            print(f"\n  Total: {len(books)} book(s)")

        elif choice == "3":
            # ── Search Books ──────────────────────────────────────────────
            keyword = get_input("Search (title/author/genre): ")
            results = library.search_books(keyword)
            print(f"\n  -- Search Results for '{keyword}' --")
            if not results:
                print("  No matching books found.")
            else:
                for book in results:
                    book.display()
                print(f"\n  Found: {len(results)} result(s)")

        elif choice == "4":
            # ── Remove Book ───────────────────────────────────────────────
            book_id = get_input("Enter Book ID to remove: ").upper()
            try:
                library.remove_book(book_id)
                print(f"\n  [SUCCESS] Book '{book_id}' removed successfully.")
            except (KeyError, ValueError) as error:
                print(f"\n  [ERROR] {error}")

        elif choice == "0":
            break
        else:
            print("  [ERROR] Invalid choice. Please try again.")

        pause()


def member_menu(library: Library) -> None:
    """
    Display and handle the Member Management sub-menu.

    Args:
        library (Library): The active Library instance.
    """
    while True:
        print("\n  --- MEMBER MANAGEMENT ---")
        print("  1. Register New Member")
        print("  2. View All Members")
        print("  3. Search Members")
        print("  4. Remove a Member")
        print("  0. Back to Main Menu")
        print_divider()

        choice = get_input("Enter choice: ")

        if choice == "1":
            # ── Register Member ───────────────────────────────────────────
            print("\n  -- Register New Member --")
            name = get_input("Full Name: ")
            email = get_input("Email: ")
            phone = get_input("Phone: ")
            try:
                member = library.register_member(name, email, phone)
                print(f"\n  [SUCCESS] Member registered successfully!")
                member.display()
            except ValueError as error:
                print(f"\n  [ERROR] {error}")

        elif choice == "2":
            # ── View All Members ──────────────────────────────────────────
            print("\n  -- All Registered Members --")
            members = library.get_all_members()
            if not members:
                print("  No members registered yet.")
            else:
                for member in members:
                    member.display()
            print(f"\n  Total: {len(members)} member(s)")

        elif choice == "3":
            # ── Search Members ────────────────────────────────────────────
            keyword = get_input("Search (name/email): ")
            results = library.search_members(keyword)
            print(f"\n  -- Search Results for '{keyword}' --")
            if not results:
                print("  No matching members found.")
            else:
                for member in results:
                    member.display()

        elif choice == "4":
            # ── Remove Member ─────────────────────────────────────────────
            member_id = get_input("Enter Member ID to remove: ").upper()
            try:
                library.remove_member(member_id)
                print(f"\n  [SUCCESS] Member '{member_id}' removed.")
            except (KeyError, ValueError) as error:
                print(f"\n  [ERROR] {error}")

        elif choice == "0":
            break
        else:
            print("  [ERROR] Invalid choice. Please try again.")

        pause()


def transaction_menu(library: Library) -> None:
    """
    Display and handle the Borrow/Return sub-menu.

    Args:
        library (Library): The active Library instance.
    """
    while True:
        print("\n  --- BORROW / RETURN ---")
        print("  1. Borrow a Book")
        print("  2. Return a Book")
        print("  3. View Transaction History")
        print("  0. Back to Main Menu")
        print_divider()

        choice = get_input("Enter choice: ")

        if choice == "1":
            # ── Borrow Book ───────────────────────────────────────────────
            print("\n  -- Borrow a Book --")
            book_id = get_input("Book ID: ").upper()
            member_id = get_input("Member ID: ").upper()
            try:
                txn = library.borrow_book(book_id, member_id)
                print(f"\n  [SUCCESS] Book borrowed successfully!")
                txn.display()
            except (KeyError, ValueError) as error:
                print(f"\n  [ERROR] {error}")

        elif choice == "2":
            # ── Return Book ───────────────────────────────────────────────
            print("\n  -- Return a Book --")
            book_id = get_input("Book ID: ").upper()
            member_id = get_input("Member ID: ").upper()
            try:
                txn = library.return_book(book_id, member_id)
                print(f"\n  [SUCCESS] Book returned successfully!")
                txn.display()
            except (KeyError, ValueError) as error:
                print(f"\n  [ERROR] {error}")

        elif choice == "3":
            # ── Transaction History ───────────────────────────────────────
            print("\n  -- Transaction History --")
            history = library.get_transaction_history()
            if not history:
                print("  No transactions recorded yet.")
            else:
                for txn in history:
                    txn.display()
            print(f"\n  Total: {len(history)} transaction(s)")

        elif choice == "0":
            break
        else:
            print("  [ERROR] Invalid choice. Please try again.")

        pause()


def reports_menu(library: Library) -> None:
    """
    Display basic library statistics.

    Args:
        library (Library): The active Library instance.
    """
    print("\n  --- LIBRARY STATISTICS ---")
    stats = library.get_statistics()
    print(f"  Total Books         : {stats['total_books']}")
    print(f"  Available Books     : {stats['available_books']}")
    print(f"  Currently Borrowed  : {stats['borrowed_books']}")
    print(f"  Registered Members  : {stats['total_members']}")
    print(f"  Total Transactions  : {stats['total_transactions']}")
    pause()


def reset_menu(library: Library) -> None:
    """
    Handle the Reset All Data option. Requires the user to type the
    full word 'yes' (not just 'y') before anything is deleted, since
    this permanently erases every book, member, librarian, and
    transaction record — both in memory and on disk.

    Args:
        library (Library): The active Library instance.
    """
    print("\n  --- RESET ALL DATA ---")
    print("  This will permanently delete ALL books, members,")
    print("  librarians, and transaction history. This cannot be undone.")
    confirm = get_input("Type 'yes' to confirm, or anything else to cancel: ")
    if confirm.lower() == "yes":
        library.reset_all_data()
        print("\n  [SUCCESS] All library data has been reset.")
    else:
        print("\n  Reset cancelled. No data was changed.")
    pause()


# ── Main Entry Point ──────────────────────────────────────────────────────────

def main() -> None:
    """
    Main function: initialise the library and launch the interactive
    menu. This is the program's single entry point.
    """
    print_banner()
    print("  Initialising system and loading data...\n")

    try:
        library = Library("Gisma University Library")
        print(f"  Welcome to {library.name}!")
    except Exception as error:
        # Critical startup failure — inform user and exit safely
        print(f"  [CRITICAL ERROR] Failed to initialise library: {error}")
        return

    # ── Main Menu Loop ────────────────────────────────────────────────────
    while True:
        print("\n" + "=" * 60)
        print(f"  {library.name}")
        print("=" * 60)
        print("  1. Book Management")
        print("  2. Member Management")
        print("  3. Borrow / Return Books")
        print("  4. View Statistics")
        print("  5. Reset All Data")
        print("  0. Exit")
        print_divider()

        choice = get_input("Enter your choice: ")

        if choice == "1":
            book_menu(library)
        elif choice == "2":
            member_menu(library)
        elif choice == "3":
            transaction_menu(library)
        elif choice == "4":
            reports_menu(library)
        elif choice == "5":
            reset_menu(library)
        elif choice == "0":
            print("\n  Thank you for using the Library Management System.")
            print("  All data has been saved. Goodbye!\n")
            break
        else:
            print("  [ERROR] Invalid choice. Please select from the menu.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Triggered if the user presses Ctrl+C at any input prompt.
        print("\n\n  Program interrupted. Goodbye!\n")
    except EOFError:
        # Triggered if the input stream closes unexpectedly
        # (e.g. terminal window closed while waiting for input).
        print("\n\n  Input stream closed. Exiting.\n")
