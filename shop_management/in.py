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
        self.pack(fill = "both", expand = True)
        self.create_widgets()
        self.inventory_tab = inventory_tab
        self.refresh_sales_list()
        self.refresh_invoice_list()
        self.inventory_tab = inventory_tab


