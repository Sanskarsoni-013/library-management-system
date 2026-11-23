"""
Database Manager module for Library Management System.
Implements robust, parameterized SQLite/MySQL transactions.
"""

import sqlite3
import os
from datetime import datetime, timedelta

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "library.db")

class DatabaseManager:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT,
                total_copies INTEGER DEFAULT 1,
                available_copies INTEGER DEFAULT 1
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                issue_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_date TEXT,
                fine_amount REAL DEFAULT 0.0,
                status TEXT DEFAULT 'ISSUED',
                FOREIGN KEY (book_id) REFERENCES books(book_id),
                FOREIGN KEY (member_id) REFERENCES members(member_id)
            );
            """)
            
            # Seed demo data if empty
            cursor.execute("SELECT COUNT(*) FROM books")
            if cursor.fetchone()[0] == 0:
                self._seed_sample_data(cursor)
            conn.commit()

    def _seed_sample_data(self, cursor):
        books = [
            ("978-0134685991", "Effective Java", "Joshua Bloch", "Technology", 4, 3),
            ("978-0596009205", "Head First Design Patterns", "Eric Freeman", "Technology", 3, 2),
            ("978-0132350884", "Clean Code", "Robert C. Martin", "Technology", 5, 5),
            ("978-1491957660", "Fluent Python", "Luciano Ramalho", "Technology", 4, 3),
            ("978-0062316097", "Sapiens: A Brief History", "Yuval Noah Harari", "History", 6, 6)
        ]
        cursor.executemany("""
            INSERT INTO books (isbn, title, author, genre, total_copies, available_copies)
            VALUES (?, ?, ?, ?, ?, ?)
        """, books)

        members = [
            ("Aarav Sharma", "aarav@example.com", "+91 9876543210"),
            ("Pooja Verma", "pooja@example.com", "+91 9876543211"),
            ("Rohan Gupta", "rohan@example.com", "+91 9876543212")
        ]
        cursor.executemany("""
            INSERT INTO members (full_name, email, phone)
            VALUES (?, ?, ?)
        """, members)

        # Active Loan
        today = datetime.now()
        cursor.execute("""
            INSERT INTO transactions (book_id, member_id, issue_date, due_date, status)
            VALUES (1, 1, ?, ?, 'ISSUED')
        """, ((today - timedelta(days=5)).strftime("%Y-%m-%d"), (today + timedelta(days=9)).strftime("%Y-%m-%d")))

    def search_books(self, query=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if query:
                q = f"%{query}%"
                cursor.execute("""
                    SELECT * FROM books 
                    WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
                """, (q, q, q))
            else:
                cursor.execute("SELECT * FROM books")
            return [dict(row) for row in cursor.fetchall()]

    def issue_book(self, book_id, member_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT available_copies FROM books WHERE book_id = ?", (book_id,))
            book = cursor.fetchone()
            if not book or book["available_copies"] <= 0:
                return False, "Book is not available for issue."

            issue_date = datetime.now().strftime("%Y-%m-%d")
            due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

            cursor.execute("""
                INSERT INTO transactions (book_id, member_id, issue_date, due_date, status)
                VALUES (?, ?, ?, ?, 'ISSUED')
            """, (book_id, member_id, issue_date, due_date))

            cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id = ?", (book_id,))
            conn.commit()
            return True, "Book issued successfully."
