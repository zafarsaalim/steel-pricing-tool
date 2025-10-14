import customtkinter as ctk
from tkinter import messagebox

def get_discounted_price(qty, base_price, discounts):
    for min_qty in sorted(map(int, discounts.keys()), reverse=True):
        if qty >= min_qty:
            return base_price * discounts[str(min_qty)]
    return base_price

def calculate():
    try:
        bar_type = bar_type_var.get()
        diameter = float(diameter_entry.get())
        length = float(length_entry.get())
        quantity = int(quantity_entry.get())
        base_price = float(base_price_entry.get())
        cutting_cost = float(cutting_cost_entry.get()) if bar_type == "Cut Bar" else 0.0
        packaging_cost = float(packaging_entry.get())
        shipping_cost = float(shipping_entry.get())
        scrap_percent = float(scrap_entry.get())
        finance_percent = float(finance_entry.get())

        # Discount tiers
        discounts = {
            discount1_qty.get(): float(discount1_val.get()),
            discount2_qty.get(): float(discount2_val.get())
        }

        # Core calculations
        weight_per_meter = diameter ** 2 * 0.006165
        weight_per_bar = weight_per_meter * length
        total_weight = weight_per_bar * quantity

        discounted_price = get_discounted_price(quantity, base_price, discounts)
        steel_cost = total_weight * discounted_price
        total_cutting = cutting_cost * quantity
        scrap = steel_cost * (scrap_percent / 100)
        subtotal = steel_cost + total_cutting + packaging_cost + shipping_cost + scrap
        finance = subtotal * (finance_percent / 100)
        total_cost = subtotal + finance

        result = (
            f"• Weight per Bar: {weight_per_bar:.2f} kg\n"
            f"• Total Weight: {total_weight:.2f} kg\n"
            f"• €/kg (after discount): €{discounted_price:.2f}\n"
            f"• Steel Cost: €{steel_cost:.2f}\n"
            f"• Cutting: €{total_cutting:.2f} | Scrap: €{scrap:.2f}\n"
            f"• Packaging: €{packaging_cost:.2f} | Shipping: €{shipping_cost:.2f}\n"
            f"• Finance: €{finance:.2f}\n"
            f"———————————————\n"
            f"• Total Cost: €{total_cost:.2f}"
        )

        result_label.configure(text=result)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# === UI SETUP ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Steel Pricing Calculator")
app.geometry("800x600")
app.resizable(False, False)
app.minsize(600, 500)

ctk.CTkLabel(app, text="Steel Price Calculator (Internal Use)", font=("Arial", 20, "bold")).pack(pady=10)

frame = ctk.CTkFrame(app)
frame.pack(fill="both", expand=True, padx=10)

def field(row, label_text, default=""):
    ctk.CTkLabel(frame, text=label_text).grid(row=row, column=0, padx=5, pady=4, sticky="e")
    entry = ctk.CTkEntry(frame)
    entry.insert(0, default)
    entry.grid(row=row, column=1, padx=5, pady=4, sticky="ew")
    return entry

frame.grid_columnconfigure(1, weight=1)

# Grid Inputs
bar_type_var = ctk.StringVar(value="Full Bar")
ctk.CTkLabel(frame, text="Bar Type:").grid(row=0, column=0, padx=5, pady=4, sticky="e")
ctk.CTkComboBox(frame, variable=bar_type_var, values=["Full Bar", "Cut Bar"]).grid(row=0, column=1, padx=5, pady=4, sticky="ew")

diameter_entry     = field(1, "Diameter (mm):")
length_entry       = field(2, "Length per Bar (m):")
quantity_entry     = field(3, "Quantity (bars):")
base_price_entry   = field(4, "Base Price (€/kg):", "100")
cutting_cost_entry = field(5, "Cutting Cost per Bar (€):", "5")
packaging_entry    = field(6, "Packaging Cost (€):", "200")
shipping_entry     = field(7, "Shipping Cost (€):", "300")
scrap_entry        = field(8, "Scrap Percent (%):", "3")
finance_entry      = field(9, "Finance Percent (%):", "2")

# Discount section
ctk.CTkLabel(frame, text="Discount Tier 1 (Qty ➜ Rate)").grid(row=10, column=0, padx=5, pady=4, sticky="e")
discount1_qty = ctk.CTkEntry(frame, width=80)
discount1_qty.insert(0, "100")
discount1_qty.grid(row=10, column=1, sticky="w", padx=(5, 0))
discount1_val = ctk.CTkEntry(frame, width=80)
discount1_val.insert(0, "0.90")
discount1_val.grid(row=10, column=1, sticky="e", padx=(0, 5))

ctk.CTkLabel(frame, text="Discount Tier 2 (Qty ➜ Rate)").grid(row=11, column=0, padx=5, pady=4, sticky="e")
discount2_qty = ctk.CTkEntry(frame, width=80)
discount2_qty.insert(0, "50")
discount2_qty.grid(row=11, column=1, sticky="w", padx=(5, 0))
discount2_val = ctk.CTkEntry(frame, width=80)
discount2_val.insert(0, "0.95")
discount2_val.grid(row=11, column=1, sticky="e", padx=(0, 5))

# Calculate Button
ctk.CTkButton(app, text="CALCULATE", command=calculate, height=40).pack(pady=12)

# Result
result_label = ctk.CTkLabel(app, text="", font=("Arial", 14), justify="left", text_color="#0a570a")
result_label.pack(padx=10, pady=5)

# Footer
ctk.CTkLabel(app, text="© 2025 – Saalim Zafar", font=("Arial", 10), text_color="gray").pack(side="bottom", pady=5)

app.mainloop()
