# Library Management System with Data Science Analytics

**Student Name:** Nisha  
**Course:** BCA Data Science - Final Year  
**Roll No:** Nisha-543  
**Session:** 2025-26  
**Project Size:** 565 Lines (480 LOC) - 19.9 KB  
**GitHub:** Nisha-543 / Library-Management-System-BCA-Data-Science

### 📚 Project Overview
A complete Library Management System built using Python, integrating core **Data Structures** and **Data Science** modules. Developed as a Final Year Project for BCA Data Science.

### 🔧 PART A: Data Structures Implemented (4)

1.  **Linked List:** To store complete issue history with timestamp. O(n) traversal.
2.  **Stack (LIFO):** To implement UNDO feature for last issued book.
3.  **Queue (FIFO):** For Book Reservation System when book is not available.
4.  **Hash Table (Dictionary):** For O(1) Fast Book Search by ID and Title.

### 📊 PART B: Data Science Modules

1.  **Pandas:** For data analysis - Stock analysis, Top issued books, Fine collection.
2.  **Matplotlib:** 4 Graphs in 1 Image - Category wise books, Top 5 Issued, Availability, Fine Trend.
3.  **Dataset Export:** Auto-generates `library_dataset.csv` and `books_dataset.csv` for ML.
4.  **Recommendation System:** Suggests most popular category based on issue data.

### ✨ Features
- Add / View / Search / Issue / Return Books
- Student Management
- Fine Calculation (Rs. 5/day after due date)
- Undo Last Issue (Stack)
- Reservation Queue (Queue)
- Issue History (Linked List)
- SQLite Database (library.db)
- Data Science Report with Graphs

### 🚀 How to Run
```bash
pip install pandas matplotlib
python library_management_ds.py
