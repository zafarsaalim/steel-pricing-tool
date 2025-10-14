import customtkinter as ctk
from tkinter import messagebox
from db.database import get_connection
from models.product import Product
from utils.helpers import validate_positive_number
from utils.summary import get_summary
import tkinter.ttk as ttk
class InventoryTab(ctk.CTkFrame):
    """Inventory Tab GUI"""

    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        #self.refresh_product_list()
        self.summary_label = ctk.CTkLabel(self, text="")
        self.summary_label.pack(pady=5)
        self.refresh_summary()
        self.refresh_product_list()
    def create_widgets(self):
        # Title
        ctk.CTkLabel(self, text="Inventory Management", font=("Arial", 18)).pack(pady=10)

        # Entry frame
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=10, padx=10, fill="x")

        # Product Name
        ctk.CTkLabel(entry_frame, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ctk.CTkEntry(entry_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # SKU
        ctk.CTkLabel(entry_frame, text="SKU").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.sku_entry = ctk.CTkEntry(entry_frame)
        self.sku_entry.grid(row=0, column=3, padx=5, pady=5)

        # Purchase Price
        ctk.CTkLabel(entry_frame, text="Purchase Price").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.purchase_entry = ctk.CTkEntry(entry_frame)
        self.purchase_entry.grid(row=1, column=1, padx=5, pady=5)

        # Selling Price
        ctk.CTkLabel(entry_frame, text="Selling Price").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.selling_entry = ctk.CTkEntry(entry_frame)
        self.selling_entry.grid(row=1, column=3, padx=5, pady=5)

        # Quantity
        ctk.CTkLabel(entry_frame, text="Quantity").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.qty_entry = ctk.CTkEntry(entry_frame)
        self.qty_entry.grid(row=2, column=1, padx=5, pady=5)
        #total_sales, unpaid_count = get_summary()
        #ctk.CTkLabel(self, text=f"Total Sales: {total_sales:.2f} | Unpaid Invoices: {unpaid_count}").pack(pady=5)
        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Add Product", command=self.add_product).grid(row=0, column=0, padx=5)
        ctk.CTkButton(button_frame, text="Update Product", command=self.update_product).grid(row=0, column=1, padx=5)
        ctk.CTkButton(button_frame, text="Delete Product", command=self.delete_product).grid(row=0, column=2, padx=5)
        ctk.CTkButton(button_frame, text="Refresh List", command=self.refresh_product_list).grid(row=0, column=3, padx=5)

        # Product List
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        #self.product_listbox = ctk.CTkTextbox(self.list_frame, width=750, height=200)
        #self.product_listbox.pack(padx=5, pady=5)
        #import tkinter.ttk as ttk  # add at the top if not already imported

        # --- Clean, scrollable table view for products ---
        columns = ("ID", "Name", "SKU", "Purchase Price", "Sell Price", "Stock")
        self.product_table = ttk.Treeview(self.list_frame, columns=columns, show="headings", height=8)

        for col in columns:
            self.product_table.heading(col, text=col)
            self.product_table.column(col, width=120, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.product_table.yview)
        self.product_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.product_table.pack(fill="both", expand=True)

    # ----------------------------
    # Database Operations
    # ----------------------------
    def add_product(self):
        try:
            name = self.name_entry.get()
            sku = self.sku_entry.get()
            purchase = validate_positive_number(self.purchase_entry.get(), "Purchase Price")
            selling = validate_positive_number(self.selling_entry.get(), "Selling Price")
            qty = int(validate_positive_number(self.qty_entry.get(), "Quantity"))

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products(name, sku, purchase_price, selling_price, quantity)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, sku, purchase, selling, qty))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Product '{name}' added!")
            self.refresh_product_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_product(self):
        try:
            sku = self.sku_entry.get()
            if not sku:
                messagebox.showwarning("Warning", "Enter SKU to update product")
                return
            purchase = validate_positive_number(self.purchase_entry.get(), "Purchase Price")
            selling = validate_positive_number(self.selling_entry.get(), "Selling Price")
            qty = int(validate_positive_number(self.qty_entry.get(), "Quantity"))

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products
                SET purchase_price=?, selling_price=?, quantity=?
                WHERE sku=?
            ''', (purchase, selling, qty, sku))
            if cursor.rowcount == 0:
                messagebox.showinfo("Info", f"No product found with SKU '{sku}'")
            else:
                messagebox.showinfo("Success", f"Product '{sku}' updated!")
            conn.commit()
            conn.close()
            self.refresh_product_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_product(self):
        try:
            sku = self.sku_entry.get()
            if not sku:
                messagebox.showwarning("Warning", "Enter SKU to delete product")
                return
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM products WHERE sku=?', (sku,))
            if cursor.rowcount == 0:
                messagebox.showinfo("Info", f"No product found with SKU '{sku}'")
            else:
                messagebox.showinfo("Success", f"Product '{sku}' deleted!")
            conn.commit()
            conn.close()
            self.refresh_product_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_product_list(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT product_id, name, sku, purchase_price, selling_price, quantity FROM products')
        products = cursor.fetchall()
        conn.close()

        self.product_table.delete(*self.product_table.get_children())
        for p in products:
            self.product_table.insert("", "end", values=p)
        #self.check_low_stock()

    def check_low_stock(self, threshold=5):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name, sku, quantity FROM products WHERE quantity <= ?', (threshold,))
        low_stock = cursor.fetchall()
        conn.close()

        if low_stock:
            msg = "Low stock alert:\n"
            for p in low_stock:
                msg += f"{p[0]} ({p[1]}) - Qty: {p[2]}\n"
            messagebox.showwarning("Low Stock", msg)

    def refresh_summary(self):
        total_sales, unpaid_count = get_summary()
        self.summary_label.configure(text=f"Total Sales: {total_sales:.2f} | Unpaid Invoices: {unpaid_count}")



