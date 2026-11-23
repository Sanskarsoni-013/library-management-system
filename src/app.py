"""
Tkinter Desktop User Interface & CLI entry point for Library Management System.
"""

import sys
import os
from db_manager import DatabaseManager
from export_excel import generate_excel_audit_report

def run_cli_mode():
    print("=" * 60)
    print("Automated Library Management & Inventory System")
    print("=" * 60)
    db = DatabaseManager()
    
    books = db.search_books()
    print(f"Loaded {len(books)} titles from relational database:")
    for b in books:
        print(f" - [{b['isbn']}] {b['title']} by {b['author']} | Available: {b['available_copies']}/{b['total_copies']}")
    
    print("\n-> Running automated Excel ledger generation...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "..", "output")
    report_file = generate_excel_audit_report(output_dir)
    print(f"-> Audit successfully exported to: {report_file}")
    print("=" * 60)

def main():
    # If DISPLAY/GUI is available, Tkinter can be launched, otherwise run CLI mode
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox

        root = tk.Tk()
        root.title("Library Inventory & Management System")
        root.geometry("680x420")

        db = DatabaseManager()

        frame = ttk.Frame(root, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        lbl = ttk.Label(frame, text="Library Inventory Management", font=("Helvetica", 14, "bold"))
        lbl.pack(pady=5)

        # Treeview for Books
        tree = ttk.Treeview(frame, columns=("ISBN", "Title", "Author", "Available"), show="headings", height=10)
        tree.heading("ISBN", text="ISBN")
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Available", text="Available Copies")
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        for b in db.search_books():
            tree.insert("", tk.END, values=(b["isbn"], b["title"], b["author"], f"{b['available_copies']}/{b['total_copies']}"))

        def handle_export():
            script_dir = os.path.dirname(os.path.abspath(__file__))
            out = os.path.join(script_dir, "..", "output")
            f = generate_excel_audit_report(out)
            messagebox.showinfo("Export Successful", f"Excel report generated:\n{f}")

        btn_export = ttk.Button(frame, text="Export Excel Audit Report", command=handle_export)
        btn_export.pack(pady=5)

        root.mainloop()
    except Exception:
        run_cli_mode()

if __name__ == "__main__":
    main()
