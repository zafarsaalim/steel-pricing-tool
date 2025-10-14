from gui.inventory_tab import InventoryTab
from gui.sales_tab import SalesTab
from gui.invoice_tab import InvoiceTab

import customtkinter as ctk
from db.database import init_db


def main():
    init_db()
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Shop Management")
    app.geometry("1280x768")

    # Tabview
    from customtkinter import CTkTabview

    tabview = CTkTabview(app, width=1280, height=768)
    tabview.pack(padx=10, pady=10)

    tabview.add("Inventory")
    tabview.add("Sales")
    tabview.add("Invoice")
    inventory_tab = InventoryTab(tabview.tab("Inventory"))
    sales_tab = SalesTab(tabview.tab("Sales"), inventory_tab)
    invoice_tab = InvoiceTab(tabview.tab("Invoice"), inventory_tab)

    app.mainloop()


if __name__ == "__main__":
    main()
