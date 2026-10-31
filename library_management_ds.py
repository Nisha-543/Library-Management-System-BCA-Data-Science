"""

 Project Title: Library Management System with Data Science Analytics
 Student Name : Nisha
 Roll No      : Nisha-543
 Course       : BCA Data Science - Final Year Project
 Session      : 2025-26
 GitHub       : Library-Management-System-BCA-Data-Science
 
 PART A - DATA STRUCTURES IMPLEMENTED:
 1. Linked List - For Issue History Tracking
 2. Stack (LIFO) - For Undo Last Issue Operation
 3. Queue (FIFO) - For Book Reservation System
 4. Hash Table (Dict) - For O(1) Fast Book Search

 PART B - DATA SCIENCE MODULES:
 1. Pandas - Data Analysis and Cleaning
 2. Matplotlib - Data Visualization (3 Graphs)
 3. CSV Dataset Export - For ML Model
 4. Recommendation System - Most Issued Books

"""

import sqlite3
import random
import csv
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict

# Data Science Libraries
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    DS_AVAILABLE = True
except ImportError:
    DS_AVAILABLE = False
    print("Note: Install pandas, matplotlib for Data Science features: pip install pandas matplotlib")

# ==================== PART A: DATA STRUCTURES ====================

class Node:
    """Node for Linked List"""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.timestamp = datetime.now()

class LinkedList:
    """Linked List for storing Issue History - BCA DS Concept"""
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
        print(f"[LinkedList] History Added: {data} | Total: {self.size}")

    def display(self):
        if not self.head:
            print("No Issue History Found.")
            return
        print("\n--- Issue History (Linked List Traversal) ---")
        current = self.head
        count = 1
        while current:
            print(f"{count}. {current.data} | Time: {current.timestamp.strftime('%Y-%m-%d %H:%M')}")
            current = current.next
            count += 1

    def get_all(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def search(self, keyword):
        result = []
        current = self.head
        while current:
            if keyword.lower() in str(current.data).lower():
                result.append(current.data)
            current = current.next
        return result

class Stack:
    """Stack (LIFO) for Undo Feature - BCA DS Concept"""
    def __init__(self):
        self.items = []
        print("[Stack] Initialized for Undo Operations")

    def push(self, item):
        self.items.append(item)
        print(f"[Stack] PUSH: {item}")

    def pop(self):
        if not self.is_empty():
            item = self.items.pop()
            print(f"[Stack] POP (Undo): {item}")
            return item
        else:
            print("[Stack] Stack is Empty - Nothing to Undo")
            return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def display(self):
        print(f"\n--- Undo Stack (Top to Bottom) - Size: {len(self.items)} ---")
        if self.is_empty():
            print("Stack Empty")
        else:
            for i in range(len(self.items)-1, -1, -1):
                print(f"{len(self.items)-i}. {self.items[i]}")

class Queue:
    """Queue (FIFO) for Book Reservation - BCA DS Concept"""
    def __init__(self):
        self.items = []
        print("[Queue] Initialized for Reservation System")

    def enqueue(self, item):
        self.items.append(item)
        print(f"[Queue] ENQUEUE (Reservation Added): {item} | Queue Length: {len(self.items)}")

    def dequeue(self):
        if not self.is_empty():
            item = self.items.pop(0)
            print(f"[Queue] DEQUEUE (Reservation Fulfilled): {item}")
            return item
        else:
            print("[Queue] No Reservations Pending")
            return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def display(self):
        print(f"\n--- Reservation Queue (FIFO) - Pending: {len(self.items)} ---")
        if self.is_empty():
            print("No Pending Reservations")
        else:
            for i, item in enumerate(self.items, 1):
                print(f"{i}. {item}")

    def front(self):
        if not self.is_empty():
            return self.items[0]
        return None

class HashTable:
    """Hash Table for Fast Search - O(1) Complexity"""
    def __init__(self):
        self.table = {}
        print("[HashTable] Initialized for O(1) Fast Search")

    def insert(self, key, value):
        hash_key = hash(key) % 1000
        self.table[key] = value
        print(f"[HashTable] Inserted: Key={key}, Hash={hash_key}")

    def search(self, key):
        if key in self.table:
            print(f"[HashTable] Found in O(1): {key}")
            return self.table[key]
        else:
            print(f"[HashTable] Not Found: {key}")
            return None

    def delete(self, key):
        if key in self.table:
            del self.table[key]
            print(f"[HashTable] Deleted: {key}")

    def display_stats(self):
        print(f"\n[HashTable] Total Indexed Books: {len(self.table)}")

# ==================== DATABASE MANAGEMENT ====================

def init_db():
    """Initialize SQLite Database"""
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            publisher TEXT,
            qty INTEGER,
            available INTEGER,
            price REAL,
            added_date TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT,
            course TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issued (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            student_name TEXT,
            book_id TEXT,
            book_title TEXT,
            issue_date TEXT,
            due_date TEXT,
            return_date TEXT,
            fine REAL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
    print("[Database] library.db initialized successfully")

# ==================== CORE LIBRARY SYSTEM ====================

class LibraryManagementSystem:
    def __init__(self):
        self.history = LinkedList()
        self.undo_stack = Stack()
        self.reservation_queue = Queue()
        self.fast_search = HashTable()
        self.load_hash_table()
        print("\n" + "="*70)
        print(" LIBRARY MANAGEMENT SYSTEM WITH DATA SCIENCE - By Nisha")
        print(" BCA Data Science - Final Year Project (2025-26)")
        print("="*70)

    def load_hash_table(self):
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, title FROM books")
            for book_id, title in cursor.fetchall():
                self.fast_search.insert(book_id, title)
                self.fast_search.insert(title.lower(), book_id)
        except:
            pass
        conn.close()

    def add_book(self):
        print("\n--- ADD NEW BOOK ---")
        title = input("Enter Book Title: ").strip()
        author = input("Enter Author Name: ").strip()
        category = input("Enter Category (CS/Data Science/Math/Novel/AI): ").strip()
        publisher = input("Enter Publisher: ").strip()
        try:
            qty = int(input("Enter Quantity: "))
            price = float(input("Enter Price: "))
        except:
            print("Invalid Qty/Price! Using default 1 and 299")
            qty = 1
            price = 299.0

        book_id = f"B{random.randint(1000,9999)}-{category[:2].upper()}"
        conn = sqlite3.connect("library.db")
        conn.execute("INSERT INTO books VALUES (?,?,?,?,?,?,?,?,?)",
                     (book_id, title, author, category, publisher, qty, qty, price, str(datetime.now().date())))
        conn.commit()
        conn.close()

        self.fast_search.insert(book_id, title)
        self.fast_search.insert(title.lower(), book_id)
        print(f"\n✅ Book Added Successfully! ID: {book_id}")
        print(f"   Title: {title} | Qty: {qty} | Developed for Nisha - BCA DS")

    def view_books(self):
        print("\n--- VIEW ALL BOOKS ---")
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, category, qty, available, price FROM books")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No Books in Library. Add Books First.")
            return

        print(f"\n{'ID':<12} {'Title':<25} {'Author':<15} {'Cat':<10} {'Avail/Qty':<10} Price")
        print("-"*90)
        for r in rows:
            print(f"{r[0]:<12} {r[1][:24]:<25} {r[2][:14]:<15} {r[3][:9]:<10} {r[5]}/{r[4]:<8} {r[6]}")
        print(f"\nTotal Books: {len(rows)}")
        self.fast_search.display_stats()

    def search_book(self):
        print("\n--- FAST SEARCH (Hash Table O(1)) ---")
        keyword = input("Enter Book ID or Title: ").strip()
        result = self.fast_search.search(keyword)
        if result:
            print(f"Found via HashTable: {result}")
        
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id LIKE ? OR title LIKE ? OR author LIKE ?",
                       (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        rows = cursor.fetchall()
        conn.close()
        if rows:
            for r in rows:
                print(f"ID: {r[0]} | Title: {r[1]} | Author: {r[2]} | Avail: {r[6]}/{r[5]}")
        else:
            print("No Book Found")

    def issue_book(self):
        print("\n--- ISSUE BOOK ---")
        student_id = input("Enter Student ID: ").strip()
        student_name = input("Enter Student Name: ").strip()
        book_id = input("Enter Book ID: ").strip()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, available FROM books WHERE id=?", (book_id,))
        row = cursor.fetchone()

        if not row:
            print("❌ Book ID Not Found!")
            conn.close()
            return

        title, available = row
        if available <= 0:
            print(f"❌ Book Not Available! Adding to Reservation Queue (FIFO)")
            self.reservation_queue.enqueue(f"Student {student_id} ({student_name}) -> Book {book_id} ({title}) on {datetime.now().date()}")
            conn.close()
            return

        issue_date = datetime.now().date()
        due_date = issue_date + timedelta(days=15)
        cursor.execute("UPDATE books SET available=available-1 WHERE id=?", (book_id,))
        cursor.execute("INSERT INTO issued (student_id, student_name, book_id, book_title, issue_date, due_date) VALUES (?,?,?,?,?,?)",
                       (student_id, student_name, book_id, title, str(issue_date), str(due_date)))
        conn.commit()
        conn.close()

        log_entry = f"{student_id} ({student_name}) issued '{title}' [ID:{book_id}] on {issue_date}"
        self.history.append(log_entry)
        self.undo_stack.push((student_id, book_id, title, str(issue_date)))

        print(f"\n✅ Issued Successfully: {title}")
        print(f"   Student: {student_name} | Due Date: {due_date} | Fine: Rs.5/day after due")

    def return_book(self):
        print("\n--- RETURN BOOK ---")
        student_id = input("Enter Student ID: ").strip()
        book_id = input("Enter Book ID: ").strip()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT issue_id, book_title, due_date FROM issued WHERE student_id=? AND book_id=? AND return_date IS NULL", (student_id, book_id))
        row = cursor.fetchone()

        if not row:
            print("❌ No Active Issue Found for this Student & Book")
            conn.close()
            return

        issue_id, title, due_date_str = row
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        fine = 0
        if today > due_date:
            days_late = (today - due_date).days
            fine = days_late * 5
            print(f"⚠️ Late Return! {days_late} days late | Fine: Rs.{fine}")

        cursor.execute("UPDATE issued SET return_date=?, fine=? WHERE issue_id=?", (str(today), fine, issue_id))
        cursor.execute("UPDATE books SET available=available+1 WHERE id=?", (book_id,))
        conn.commit()
        conn.close()

        print(f"\n✅ Returned Successfully: {title} | Fine Collected: Rs.{fine}")

        if not self.reservation_queue.is_empty():
            next_res = self.reservation_queue.front()
            print(f"📢 Next Reservation in Queue: {next_res}")

    def undo_last_issue(self):
        print("\n--- UNDO LAST ISSUE (Stack LIFO) ---")
        last = self.undo_stack.pop()
        if not last:
            return
        student_id, book_id, title, issue_date = last
        conn = sqlite3.connect("library.db")
        conn.execute("UPDATE books SET available=available+1 WHERE id=?", (book_id,))
        conn.execute("DELETE FROM issued WHERE student_id=? AND book_id=? AND issue_date=?", (student_id, book_id, issue_date))
        conn.commit()
        conn.close()
        print(f"✅ Undo Done: Issue of '{title}' by {student_id} has been reverted")

    # ==================== PART B: DATA SCIENCE ====================

    def data_science_report(self):
        print("\n" + "="*70)
        print(" DATA SCIENCE ANALYSIS REPORT - Nisha BCA DS Project")
        print("="*70)
        if not DS_AVAILABLE:
            print("Please install: pip install pandas matplotlib")
            return

        try:
            conn = sqlite3.connect("library.db")
            df_books = pd.read_sql_query("SELECT * FROM books", conn)
            df_issued = pd.read_sql_query("SELECT * FROM issued", conn)
            conn.close()

            if df_books.empty:
                print("No Data for Analysis - Add and Issue Books First")
                return

            print(f"\n[DATASET INFO]")
            print(f"Total Unique Books: {len(df_books)}")
            print(f"Total Issue Records: {len(df_issued)}")
            print(f"Total Categories: {df_books['category'].nunique()}")
            print(f"Categories: {list(df_books['category'].unique())}")

            print(f"\n[STOCK ANALYSIS - Pandas]")
            print(df_books[['category','qty','available']].groupby('category').sum())

            print(f"\n[TOP ISSUED BOOKS - Recommendation System]")
            if not df_issued.empty:
                top_books = df_issued['book_title'].value_counts().head(5)
                print(top_books)
                
                print(f"\n[TOP STUDENTS - Most Active]")
                print(df_issued['student_id'].value_counts().head(3))

                print(f"\n[FINE COLLECTION ANALYSIS]")
                print(f"Total Fine Collected: Rs.{df_issued['fine'].sum()}")
                print(f"Average Fine: Rs.{df_issued['fine'].mean():.2f}")

                # Export CSV
                df_issued.to_csv("library_dataset.csv", index=False)
                df_books.to_csv("books_dataset.csv", index=False)
                print(f"\n✅ Datasets Exported: library_dataset.csv, books_dataset.csv")

                # Graphs
                plt.figure(figsize=(12,8))

                plt.subplot(2,2,1)
                df_books.groupby('category')['qty'].sum().plot(kind='bar', color='skyblue', title='Books by Category - Nisha BCA')
                plt.ylabel('Quantity')

                plt.subplot(2,2,2)
                if not df_issued.empty:
                    df_issued['book_title'].value_counts().head(5).plot(kind='bar', color='orange', title='Top 5 Most Issued Books')
                    plt.ylabel('Issue Count')

                plt.subplot(2,2,3)
                df_books['available'].plot(kind='hist', bins=10, color='green', title='Availability Distribution')
                plt.xlabel('Available Copies')

                plt.subplot(2,2,4)
                if not df_issued.empty:
                    df_issued['fine'].plot(kind='line', title='Fine Trend')
                    plt.ylabel('Fine Rs.')

                plt.tight_layout()
                plt.savefig("data_science_analysis_Nisha_BCA.png", dpi=150)
                print(f"✅ Graph Saved: data_science_analysis_Nisha_BCA.png (4 Graphs in 1)")

                # Recommendation
                print(f"\n[RECOMMENDATION SYSTEM - For Students]")
                most_issued_cat = df_issued.merge(df_books, left_on='book_id', right_on='id')['category'].mode()
                if not most_issued_cat.empty:
                    print(f"Most Popular Category: {most_issued_cat[0]} -> Recommend more books in this category")

            else:
                print("\nNo Issued Data Yet - Issue some books to generate report")

        except Exception as e:
            print(f"Error in Data Science Module: {e}")
            print("Tip: pip install pandas matplotlib")

# ==================== MAIN MENU ====================

def main():
    init_db()
    lib = LibraryManagementSystem()
    
    # Add sample data for demo if empty
    conn = sqlite3.connect("library.db")
    count = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    conn.close()
    if count == 0:
        print("\n[Demo] Adding 3 sample books for testing...")
        conn = sqlite3.connect("library.db")
        sample = [
            (f"B{random.randint(1000,9999)}", "Python for Data Science", "Nisha Author", "Data Science", "BCA Publications", 5, 5, 450, str(datetime.now().date())),
            (f"B{random.randint(1000,9999)}", "Data Structures in Python", "Nisha Singh", "CS", "Tech Books", 3, 3, 399, str(datetime.now().date())),
            (f"B{random.randint(1000,9999)}", "Machine Learning Basics", "AI Expert", "AI", "AI Press", 4, 4, 550, str(datetime.now().date())),
        ]
        for b in sample:
            try:
                conn.execute("INSERT INTO books VALUES (?,?,?,?,?,?,?,?,?)", b)
                lib.fast_search.insert(b[0], b[1])
            except: pass
        conn.commit()
        conn.close()
        print("[Demo] Sample Books Added!")

    while True:
        print("\n" + "-"*70)
        print(" MENU: 1.Add Book 2.View Books 3.Search Book 4.Issue Book 5.Return")
        print("       6.Undo Issue (Stack) 7.Reservation Queue 8.History (LL) 9.Data Science Report 0.Exit")
        print("-"*70)
        choice = input("Enter Your Choice (0-9): ").strip()

        if choice == '1':
            lib.add_book()
        elif choice == '2':
            lib.view_books()
        elif choice == '3':
            lib.search_book()
        elif choice == '4':
            lib.issue_book()
        elif choice == '5':
            lib.return_book()
        elif choice == '6':
            lib.undo_last_issue()
        elif choice == '7':
            lib.reservation_queue.display()
        elif choice == '8':
            lib.history.display()
            print("\n--- Stack Status ---")
            lib.undo_stack.display()
        elif choice == '9':
            lib.data_science_report()
        elif choice == '0':
            print("\nThank You Nisha! Project By Nisha - BCA Data Science Final Year")
            print("GitHub: Library-Management-System-BCA-Data-Science")
            print("Data Science Graphs & CSV saved in folder")
            break
        else:
            print("Invalid Choice! Enter 0-9")

if __name__ == "__main__":
    main()
