import json
import customtkinter as ctk
from tkinter import messagebox

# Load settings
with open("settings.json", "r") as f:
    config = json.load(f)

# Discount calculation
def get_discounted_price(qty, base, discounts):
    for min_qty in sorted(map(int, discounts.keys()), reverse=True):
        if qty >= min_qty:
            return base * discounts[str(min_qty)]
    return base

def calculate():
    try:
        qty = int(quantity.get())
        bar_type = bar_type_var.get()
        base = config["base_price"]
        unit_price = get_discounted_price(qty, base, config["discounts"])
        cutting_cost = config["cutting_cost_per_unit"] * qty if bar_type == "Cut Bar" else 0
        packaging = config["packaging_cost"]
        shipping = config["shipping_cost"]
        scrap = (unit_price * qty) * (config["scrap_percent"] / 100)
        subtotal = (unit_price * qty) + cutting_cost + packaging + shipping + scrap
        finance = subtotal * (config["finance_percent"] / 100)
        total = subtotal + finance
        result_label.configure(text=f"₹ {total:.2f}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# UI setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("Steel Pricing Tool")
app.geometry("400x600")

ctk.CTkLabel(app, text="Bar Type").pack(pady=5)
bar_type_var = ctk.StringVar(value="Full Bar")
ctk.CTkComboBox(app, variable=bar_type_var, values=["Full Bar", "Cut Bar"]).pack()

ctk.CTkLabel(app, text="Quantity").pack(pady=5)
quantity = ctk.CTkEntry(app)
quantity.pack()

ctk.CTkButton(app, text="Calculate Total", command=calculate).pack(pady=20)
result_label = ctk.CTkLabel(app, text="", font=("Arial", 20))
result_label.pack(pady=10)

app.mainloop()
