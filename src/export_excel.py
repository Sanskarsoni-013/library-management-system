"""
Automated Excel Reporting Module for Library Management System.
Generates multi-sheet audit ledgers and overdue loan summaries.
"""

import os
import pandas as pd
from datetime import datetime
from db_manager import DatabaseManager

def generate_excel_audit_report(output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        # 1. Catalog Status
        df_books = pd.read_sql_query("""
            SELECT book_id, isbn, title, author, genre, total_copies, available_copies,
                   (total_copies - available_copies) AS checked_out_copies
            FROM books
        """, conn)

        # 2. Active Circulation
        df_loans = pd.read_sql_query("""
            SELECT t.transaction_id, b.title, m.full_name AS member_name, m.phone,
                   t.issue_date, t.due_date, t.status
            FROM transactions t
            JOIN books b ON t.book_id = b.book_id
            JOIN members m ON t.member_id = m.member_id
            WHERE t.status = 'ISSUED'
        """, conn)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"Library_Inventory_Audit_{timestamp}.xlsx")

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        df_books.to_excel(writer, sheet_name="Inventory_Catalog", index=False)
        df_loans.to_excel(writer, sheet_name="Active_Loans", index=False)
        
        # Summary Tab
        summary_df = pd.DataFrame([
            {"Metric": "Total Catalog Titles", "Value": len(df_books)},
            {"Metric": "Total Volumes Stocked", "Value": df_books["total_copies"].sum()},
            {"Metric": "Total Copies Currently Circulating", "Value": df_books["checked_out_copies"].sum()},
            {"Metric": "Active Borrowers", "Value": len(df_loans)}
        ])
        summary_df.to_excel(writer, sheet_name="Summary_Dashboard", index=False)

    print(f"[Report] Generated Excel Audit Workbook: {report_path}")
    return report_path

if __name__ == "__main__":
    generate_excel_audit_report()
