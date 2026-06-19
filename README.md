## Library Management System

**Module:** B100 Introduction to Computer Programming with Python
**Institution:** Gisma University of Applied Sciences
**Author:** [Your Full Name]
**Student ID:** [Your Student ID]

---

## Project Overview

The **Library Management System** is a command-line Python application designed for a university library. It allows library staff to manage the complete lifecycle of books and members — from adding books to the catalogue, registering members, processing borrow and return transactions, to viewing library statistics.

All data is automatically saved to CSV files so nothing is lost between sessions. The system starts up, loads all existing records, and is immediately ready to use.

### Problem It Solves

A university library needs a reliable digital system to:
- Track which books are available and which are borrowed
- Manage registered members and their borrowing history
- Record every transaction with timestamps for audit purposes
- Prevent rule violations (e.g. borrowing more than 3 books, removing borrowed books)

This system addresses all of these needs through a clean, menu-driven interface requiring no technical knowledge to operate.

---

##  Project Structure

```
library_management_system/
│
├── main.py            ← Entry point — runs the interactive menu
├── library.py         ← Library class — central controller/coordinator
├── book.py            ← Book class — represents a single book
├── member.py          ← Member class — represents a library member
├── librarian.py       ← Librarian class — represents a staff member
├── transaction.py     ← Transaction class — records borrow/return events
├── file_handler.py    ← All CSV file read/write operations
│
└── data/              ← Auto-created on first run
    ├── books.csv          ← Persistent book records
    ├── members.csv        ← Persistent member records
    ├── librarians.csv     ← Persistent librarian records
    └── transactions.csv   ← Persistent transaction history
```

---

## Installation and Setup

### Requirements

- **Python 3.8 or higher**
- No external libraries required — uses Python standard library only (`csv`, `os`, `datetime`)

### Steps

**1. Clone or download the repository**

```bash
git clone https://github.com/roshanjustus6-spec/library-management-system.git
cd library-management-system
```

**2. Verify Python version**

```bash
python --version
# Must be Python 3.8 or above
```

**3. Run the application**

```bash
python main.py
```

> The `data/` folder and all CSV files are created **automatically** on first run. You do not need to create anything manually.

---

##  Example Usage

### Starting the Application

```
============================================================
       GISMA LIBRARY MANAGEMENT SYSTEM
============================================================
  Initialising system and loading data...

  Welcome to Gisma University Library!

============================================================
  Gisma University Library
============================================================
  1. Book Management
  2. Member Management
  3. Borrow / Return Books
  4. View Statistics
  5. Reset All Data
  0. Exit
------------------------------------------------------------
  Enter your choice:
```

---

### Adding a Book

```
  Enter your choice: 1

  --- BOOK MANAGEMENT ---
  1. Add a New Book
  ...
  Enter choice: 1

  -- Add New Book --
  Title: The Great Gatsby
  Author: F. Scott Fitzgerald
  Genre: Fiction
  Publication Year: 1925

  [SUCCESS] Book added successfully!
  [B001] 'The Great Gatsby' by F. Scott Fitzgerald | Genre: Fiction | Year: 1925 | Status: Available
```

---

### Registering a Member

```
  Enter your choice: 2

  --- MEMBER MANAGEMENT ---
  Enter choice: 1

  -- Register New Member --
  Full Name: Alice Johnson
  Email: alice@gisma.com
  Phone: +44123456789

  [SUCCESS] Member registered successfully!
  [M001] Alice Johnson | Email: alice@gisma.com | Phone: +44123456789 | Joined: 2024-03-15 | Books Borrowed: 0/3
```

---

### Borrowing a Book

```
  Enter your choice: 3

  --- BORROW / RETURN ---
  Enter choice: 1

  -- Borrow a Book --
  Book ID: B001
  Member ID: M001

  [SUCCESS] Book borrowed successfully!
  [T0001] Member M001 borrowed Book B001 at 2024-03-15 10:30:22 (Processed by Staff S001)
```

---

### Error Handling Examples

**Invalid email:**
```
  Email: notanemail
  [ERROR] 'notanemail' is not a valid email address. Expected format: name@example.com
```

**Invalid publication year:**
```
  Publication Year: 2099
  [ERROR] Publication year must be between 1000 and 2026.
```

**Borrowing an already-borrowed book:**
```
  [ERROR] 'The Great Gatsby' is currently not available for borrowing.
```

**Exceeding borrow limit:**
```
  [ERROR] 'Alice Johnson' has reached the borrow limit (3 books).
```

**Removing a borrowed book:**
```
  [ERROR] Cannot remove 'The Great Gatsby' — it is currently borrowed.
```

---

### Viewing Statistics

```
  --- LIBRARY STATISTICS ---
  Total Books         : 10
  Available Books     : 7
  Currently Borrowed  : 3
  Registered Members  : 5
  Total Transactions  : 18
```

---

## Key Features

### Book Management
- Add new books with title, author, genre, and publication year
- View all books in the catalogue with availability status
- Search books by title, author, or genre (case-insensitive)
- Remove books (only if not currently borrowed)
- Year validation — rejects impossible years (before 1000 or in the future)

### Member Management
- Register new members with name, email, and phone number
- Email format validation — rejects malformed addresses
- View all registered members with borrowing status
- Search members by name or email
- Remove members (only if no books currently borrowed)

### Borrow and Return System
- Process book borrowing with full validation
- Process book returns linked to correct member
- Enforce a maximum borrow limit of 3 books per member
- Full transaction history with timestamps

### Data Persistence
- All data automatically saved to CSV files after every change
- Data fully restored on next startup — nothing is lost
- Graceful handling of missing files on first run

### Exception Handling
- Invalid inputs caught and reported with clear error messages
- File I/O errors caught without crashing the program
- Business rule violations (borrow limit, unavailable books) handled gracefully
- `KeyboardInterrupt` and `EOFError` handled at top level

### Librarian Audit Trail
- Every action logged with timestamp and staff ID
- Action log viewable within the session





## Data File Format

### books.csv
```
book_id,title,author,genre,year,is_available
B001,The Great Gatsby,F. Scott Fitzgerald,Fiction,1925,True
B002,Clean Code,Robert C. Martin,Technology,2008,False
```

### members.csv
```
member_id,name,email,phone,join_date,borrowed_books
M001,Alice Johnson,alice@gisma.com,+44123456789,2024-03-15,B002
M002,Bob Smith,bob@gisma.com,+44987654321,2024-03-16,
```

### transactions.csv
```
transaction_id,book_id,member_id,staff_id,transaction_type,timestamp
T0001,B002,M001,S001,BORROW,2024-03-15 10:30:22
T0002,B002,M001,S001,RETURN,2024-03-16 09:15:44
```
