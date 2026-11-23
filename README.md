# Automated Library Database & Inventory Management System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-MySQL%20%7C%20SQLite-orange.svg)](https://www.mysql.com/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-blueviolet.svg)](https://docs.python.org/3/library/tkinter.html)
[![Excel](https://img.shields.io/badge/Excel-Export%20Engine-217346.svg)](https://microsoft.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A robust, normalized desktop database application designed to automate book borrowing, returning, overdue penalty tracking, and multi-sheet audit reporting into **MS Excel**.

---

## 🌟 Highlights & Architecture
- **Normalized Relational Schema (3NF)**: Structured tables for `books`, `members`, `transactions`, and `audit_logs` with foreign key integrity.
- **Dual Engine Architecture**: Supports enterprise **MySQL** production databases as well as lightweight zero-config **SQLite** for local demonstrations.
- **Automated MS Excel Reports**: One-click generation of overdue ledgers, daily circulation activity, and inventory summaries using `openpyxl`.
- **Defensive Query Parameterization**: Complete protection against SQL injection vulnerabilities.

```text
┌───────────────────────────────────────────────┐
│              Tkinter Desktop GUI              │
│   (Search Catalog | Issue / Return | Reports) │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│           Database Manager Layer              │
│       (Parameterized CRUD Operations)         │
└──────────────┬─────────────────┬──────────────┘
               ▼                 ▼
   ┌──────────────────────┐  ┌───────────────────────┐
   │ MySQL / SQLite Store │  │  Automated Excel Logs │
   │ (Normalized Schema)  │  │  (Daily Ledger/Audit) │
   └──────────────────────┘  └───────────────────────┘
```

---

## 🚀 Features
1. **Catalog Management**: Add, update, and search titles by ISBN, Title, Author, or Category with sub-millisecond indexed lookup.
2. **Circulation Workflow**:
   - Issue books with automated return deadline stamping (14-day loan window).
   - Return processing with automated late fee calculation ($1.00/day).
3. **Automated Excel Reporting Engine**:
   - Generates formatted `.xlsx` workbooks containing current stock status, active loans, and overdue accounts.
4. **Member Authentication & History**:
   - Tracks member contact details, active borrowings, and historical transaction logs.

---

## 📁 Repository Structure
```text
library-management-system/
│
├── sql/
│   └── schema.sql             # Relational 3NF MySQL/SQLite schema
│
├── src/
│   ├── app.py                 # Tkinter Graphical User Interface
│   ├── db_manager.py          # Database abstraction and CRUD transactions
│   └── export_excel.py        # Automated Excel reporting engine
│
├── output/                    # Exported Excel audit reports
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone repository
```bash
git clone https://github.com/sanskar-soni/library-management-system.git
cd library-management-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch application
```bash
python src/app.py
```

---

## 👤 Author
- **Sanskar Soni** - [LinkedIn](https://linkedin.com/in/sanskar-soni-669382311) • [GitHub](https://github.com/sanskar-soni)
