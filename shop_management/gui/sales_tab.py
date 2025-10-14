import customtkinter as ctk
from tkinter import messagebox
from db.database import get_connection
from models.product import Product
from datetime import datetime
from gui.inventory_tab import InventoryTab 
import tkinter.ttk as ttk
class SalesTab(ctk.CTkFrame):
    """Sales Tab GUI"""

    def __init__(self, parent, inventory_tab: InventoryTab):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.create_widgets() 
        self.inventory_tab = inventory_tab
        self.refresh_product_list()
        self.refresh_sales_list()
        #self.inventory_tab = inventory_tab

    def create_widgets(self):
        # Title
        ctk.CTkLabel(self, text="Sales Management", font=("Arial", 18)).pack(pady=10)

        # Sale Entry Frame
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=10, padx=10, fill="x")

        # Product SKU
        ctk.CTkLabel(entry_frame, text="Product SKU").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.sku_entry = ctk.CTkEntry(entry_frame)
        self.sku_entry.grid(row=0, column=1, padx=5, pady=5)

        # Quantity
        ctk.CTkLabel(entry_frame, text="Quantity").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.qty_entry = ctk.CTkEntry(entry_frame)
        self.qty_entry.grid(row=0, column=3, padx=5, pady=5)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Add Sale", command=self.add_sale).grid(row=0, column=0, padx=5)
        ctk.CTkButton(button_frame, text="Refresh List", command=self.refresh_sales_list).grid(row=0, column=1, padx=5)

       
        # ===== Sales Frame =====
        self.sales_frame = ctk.CTkFrame(self, corner_radius=12)
        self.sales_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # ===== Sales List Table =====
        sales_label = ctk.CTkLabel(self.sales_frame, text="Sales List",
                           font=ctk.CTkFont(size=16, weight="bold"))
        sales_label.pack(anchor="w", pady=(5, 10))

        sales_columns = ("ID", "Product", "SKU", "Qty", "Total", "Date")
        self.sales_table = ttk.Treeview(self.sales_frame, columns=sales_columns, show="headings", height=8)

        for col in sales_columns:
            self.sales_table.heading(col, text=col)
            self.sales_table.column(col, width=120, anchor="center")

        # Scrollbar for Sales Table
        sales_scrollbar = ttk.Scrollbar(self.sales_frame, orient="vertical", command=self.sales_table.yview)
        self.sales_table.configure(yscroll=sales_scrollbar.set)

        self.sales_table.pack(fill="both", expand=True, padx=5, pady=5)
        sales_scrollbar.pack(side="right", fill="y")


        # ===== Available Products Table =====
        product_label = ctk.CTkLabel(self.sales_frame, text="Available Products",
                             font=ctk.CTkFont(size=16, weight="bold"))
        product_label.pack(anchor="w", pady=(15, 10))

        product_columns = ("Name", "SKU", "Selling Price", "Quantity")

        self.product_table = ttk.Treeview(self.sales_frame, columns=product_columns, show="headings", height=6)

        for col in product_columns:
            self.product_table.heading(col, text=col)
            self.product_table.column(col, width=120, anchor="center")

        # Scrollbar for Product Table
        product_scrollbar = ttk.Scrollbar(self.sales_frame, orient="vertical", command=self.product_table.yview)
        self.product_table.configure(yscroll=product_scrollbar.set)

        self.product_table.pack(fill="both", expand=True, padx=5, pady=5)
        product_scrollbar.pack(side="right", fill="y")

    # ----------------------------
    # Database Operations
    # ----------------------------
    def add_sale(self):
        sku = self.sku_entry.get()
        try:
            qty = int(self.qty_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")
            return

        conn = get_connection()
        cursor = conn.cursor()

        # Check product exists and enough stock
        cursor.execute('SELECT product_id, name, quantity, selling_price FROM products WHERE sku=?', (sku,))
        product = cursor.fetchone()
        if not product:
            messagebox.showerror("Error", f"No product found with SKU '{sku}'")
            conn.close()
            return
        product_id, name, stock_qty, price = product
        if qty > stock_qty:
            messagebox.showerror("Error", f"Not enough stock. Available: {stock_qty}")
            conn.close()
            return

        total_price = price * qty
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert sale
        cursor.execute('''
            INSERT INTO sales(product_id, quantity, total_price, date)
            VALUES (?, ?, ?, ?)
        ''', (product_id, qty, total_price, date))

        # Update inventory
        cursor.execute('''
            UPDATE products SET quantity = quantity - ? WHERE product_id = ?
        ''', (qty, product_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Sale of {qty} '{name}' recorded!")
        self.refresh_sales_list()
        self.refresh_product_list()
        self.inventory_tab.refresh_summary()


    def refresh_sales_list(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.sale_id, p.name, p.sku, s.quantity, s.total_price, s.date
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            ORDER BY s.sale_id DESC
        ''')
        sales = cursor.fetchall()
        conn.close()

        # Clear existing rows in the Treeview
        for row in self.sales_table.get_children():
            self.sales_table.delete(row)

        # Insert new rows into the Treeview
        for s in sales:
            # s[0]=ID, s[1]=Product, s[2]=SKU, s[3]=Qty, s[4]=Total, s[5]=Date
            self.sales_table.insert("", "end", values=(s[0], s[1], s[2], s[3], s[4], s[5]))
    def refresh_product_list(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name, sku, selling_price, quantity FROM products ORDER BY name')
        products = cursor.fetchall()
        conn.close()

        for row in self.product_table.get_children():
            self.product_table.delete(row)

        # Insert new rows
        for p in products:
            self.product_table.insert("", "end", values=(p[0], p[1], p[2], p[3]))
