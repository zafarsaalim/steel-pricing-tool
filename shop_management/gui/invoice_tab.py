import customtkinter as ctk
from tkinter import messagebox
from db.database import get_connection
from utils.export import export_invoices_csv
from gui.inventory_tab import InventoryTab
from datetime import datetime
import tkinter.ttk as ttk


class InvoiceTab(ctk.CTkFrame):
    """Invoice Tab GUI"""

    def __init__(self, parent, inventory_tab: InventoryTab):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.inventory_tab = inventory_tab
        self.create_widgets()
        self.refresh_sales_list()
        self.refresh_invoice_list()

    def create_widgets(self):
        # Title
        ctk.CTkLabel(
            self,
            text="Invoice Management",
            font=("Arial", 18)
        ).pack(pady=10)

        # Entry Frame
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(entry_frame, text="Sale ID").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.sale_id_entry = ctk.CTkEntry(entry_frame)
        self.sale_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(entry_frame, text="Client Name").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.client_name_entry = ctk.CTkEntry(entry_frame)
        self.client_name_entry.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(entry_frame, text="Client Contact").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.client_contact_entry = ctk.CTkEntry(entry_frame)
        self.client_contact_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(entry_frame, text="Paid").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.paid_var = ctk.CTkCheckBox(entry_frame, text="")
        self.paid_var.grid(row=1, column=3, padx=5, pady=5)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Create Invoice", command=self.create_invoice).grid(row=0, column=0, padx=5)
        ctk.CTkButton(button_frame, text="Refresh Lists", command=self.refresh_invoice_list).grid(row=0, column=1, padx=5)
        ctk.CTkButton(button_frame, text="Export CSV", command=self.export_csv).grid(row=0, column=2, padx=5)

        # ===== Invoice Table =====
        invoice_label = ctk.CTkLabel(self, text="Invoices", font=ctk.CTkFont(size=16, weight="bold"))
        invoice_label.pack(anchor="w", pady=(10, 5))

        invoice_columns = ("Invoice ID", "Sale ID", "Client", "Contact", "Paid", "Total", "Date")
        self.invoice_table = ttk.Treeview(self, columns=invoice_columns, show="headings", height=7)

        for col in invoice_columns:
            self.invoice_table.heading(col, text=col)
            self.invoice_table.column(col, width=120, anchor="center")

        invoice_scroll = ttk.Scrollbar(self, orient="vertical", command=self.invoice_table.yview)
        self.invoice_table.configure(yscroll=invoice_scroll.set)
        self.invoice_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        invoice_scroll.pack(side="right", fill="y")

        # ===== Pending Sales Table =====
        pending_label = ctk.CTkLabel(self, text="Pending Sales for Invoice", font=ctk.CTkFont(size=16, weight="bold"))
        pending_label.pack(anchor="w", pady=(15, 5))

        pending_columns = ("Sale ID", "Product", "SKU", "Qty", "Total", "Date")
        self.pending_sales_table = ttk.Treeview(self, columns=pending_columns, show="headings", height=6)

        for col in pending_columns:
            self.pending_sales_table.heading(col, text=col)
            self.pending_sales_table.column(col, width=120, anchor="center")

        pending_scroll = ttk.Scrollbar(self, orient="vertical", command=self.pending_sales_table.yview)
        self.pending_sales_table.configure(yscroll=pending_scroll.set)
        self.pending_sales_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        pending_scroll.pack(side="right", fill="y")

    # ----------------------------
    # Database Operations
    # ----------------------------
    def create_invoice(self):
        sale_id = self.sale_id_entry.get()
        client_name = self.client_name_entry.get()
        client_contact = self.client_contact_entry.get()
        paid = 1 if self.paid_var.get() else 0

        if not sale_id or not client_name:
            messagebox.showerror("Error", "Sale ID and Client Name required")
            return

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = get_connection()
        cursor = conn.cursor()

        # Check sale exists
        cursor.execute('SELECT sale_id FROM sales WHERE sale_id=?', (sale_id,))
        sale = cursor.fetchone()
        if not sale:
            messagebox.showerror("Error", f"No sale found with ID {sale_id}")
            conn.close()
            return

        # Check invoice already exists
        cursor.execute('SELECT invoice_id FROM invoices WHERE sale_id=?', (sale_id,))
        if cursor.fetchone():
            messagebox.showinfo("Info", f"Invoice already exists for Sale ID {sale_id}")
            conn.close()
            return

        # Create invoice
        cursor.execute('''
            INSERT INTO invoices(sale_id, client_name, client_contact, paid, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (sale_id, client_name, client_contact, paid, date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Invoice for Sale ID {sale_id} created")
        self.refresh_invoice_list()
        self.refresh_sales_list()
        self.inventory_tab.refresh_summary()

    def refresh_invoice_list(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.invoice_id, s.sale_id, i.client_name, i.client_contact, i.paid, i.date, s.total_price
            FROM invoices i
            JOIN sales s ON i.sale_id = s.sale_id
            ORDER BY i.invoice_id DESC
        ''')
        invoices = cursor.fetchall()
        conn.close()

        for row in self.invoice_table.get_children():
            self.invoice_table.delete(row)

        for inv in invoices:
            paid_text = "Yes" if inv[4] else "No"
            self.invoice_table.insert("", "end", values=(inv[0], inv[1], inv[2], inv[3], paid_text, inv[6], inv[5]))

    def refresh_sales_list(self):
        """List all sales without invoice yet"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.sale_id, p.name, p.sku, s.quantity, s.total_price, s.date
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            WHERE s.sale_id NOT IN (SELECT sale_id FROM invoices)
            ORDER BY s.sale_id DESC
        ''')
        sales = cursor.fetchall()
        conn.close()

        for row in self.pending_sales_table.get_children():
            self.pending_sales_table.delete(row)

        for s in sales:
            self.pending_sales_table.insert("", "end", values=(s[0], s[1], s[2], s[3], s[4], s[5]))

    def export_csv(self):
        try:
            export_invoices_csv()
            messagebox.showinfo("Success", "Invoices exported to 'invoices_export.csv'")
        except Exception as e:
            messagebox.showerror("Error", str(e))
