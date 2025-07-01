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

        # Read discounts
        discounts = {
            discount1_qty.get(): float(discount1_val.get()),
            discount2_qty.get(): float(discount2_val.get())
        }

        # Weight/meter formula
        weight_per_meter = diameter ** 2 * 0.006165
        weight_per_bar = weight_per_meter * length
        total_weight = weight_per_bar * quantity

        discounted_price = get_discounted_price(quantity, base_price, discounts)
        steel_cost = total_weight * discounted_price
        total_cutting = cutting_cost * quantity if bar_type == "Cut Bar" else 0
        scrap = steel_cost * (scrap_percent / 100)
        subtotal = steel_cost + total_cutting + packaging_cost + shipping_cost + scrap
        finance = subtotal * (finance_percent / 100)
        total_cost = subtotal + finance

        result_label.configure(text=(
            f"Weight per Bar: {weight_per_bar:.2f} kg\n"
            f"Total Weight: {total_weight:.2f} kg\n"
            f"Discounted Price: €{discounted_price:.2f}/kg\n"
            f"Steel Cost: €{steel_cost:.2f}\n"
            f"Cutting: €{total_cutting:.2f}, Scrap: €{scrap:.2f}\n"
            f"Packaging: €{packaging_cost:.2f}, Shipping: €{shipping_cost:.2f}\n"
            f"Finance Charges: €{finance:.2f}\n"
            f"-----------------------------\n"
            f"Total Cost: €{total_cost:.2f}"
        ))

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# === GUI Setup ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Steel Price Calculator (Ireland – Weight Based)")
app.geometry("820x700")
app.resizable(False, False)

ctk.CTkLabel(app, text="Steel Price Calculator", font=("Arial", 24, "bold")).pack(pady=15)

main_frame = ctk.CTkFrame(app)
main_frame.pack(pady=10, padx=20, fill="x")

# Bar Type
bar_type_var = ctk.StringVar(value="Full Bar")
ctk.CTkLabel(main_frame, text="Bar Type").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ctk.CTkComboBox(main_frame, variable=bar_type_var, values=["Full Bar", "Cut Bar"], width=180).grid(row=0, column=1, padx=5, pady=5)

# Diameter
ctk.CTkLabel(main_frame, text="Diameter (mm)").grid(row=1, column=0, padx=5, pady=5, sticky="e")
diameter_entry = ctk.CTkEntry(main_frame)
diameter_entry.grid(row=1, column=1, padx=5, pady=5)

# Length
ctk.CTkLabel(main_frame, text="Length per Bar (m)").grid(row=2, column=0, padx=5, pady=5, sticky="e")
length_entry = ctk.CTkEntry(main_frame)
length_entry.grid(row=2, column=1, padx=5, pady=5)

# Quantity
ctk.CTkLabel(main_frame, text="Quantity (bars)").grid(row=3, column=0, padx=5, pady=5, sticky="e")
quantity_entry = ctk.CTkEntry(main_frame)
quantity_entry.grid(row=3, column=1, padx=5, pady=5)

# Base Price
ctk.CTkLabel(main_frame, text="Base Price (€/kg)").grid(row=4, column=0, padx=5, pady=5, sticky="e")
base_price_entry = ctk.CTkEntry(main_frame)
base_price_entry.insert(0, "100")
base_price_entry.grid(row=4, column=1, padx=5, pady=5)

# Cutting
ctk.CTkLabel(main_frame, text="Cutting Cost per Bar (€)").grid(row=5, column=0, padx=5, pady=5, sticky="e")
cutting_cost_entry = ctk.CTkEntry(main_frame)
cutting_cost_entry.insert(0, "5")
cutting_cost_entry.grid(row=5, column=1, padx=5, pady=5)

# Packaging
ctk.CTkLabel(main_frame, text="Packaging Cost (€)").grid(row=6, column=0, padx=5, pady=5, sticky="e")
packaging_entry = ctk.CTkEntry(main_frame)
packaging_entry.insert(0, "200")
packaging_entry.grid(row=6, column=1, padx=5, pady=5)

# Shipping
ctk.CTkLabel(main_frame, text="Shipping Cost (€)").grid(row=7, column=0, padx=5, pady=5, sticky="e")
shipping_entry = ctk.CTkEntry(main_frame)
shipping_entry.insert(0, "300")
shipping_entry.grid(row=7, column=1, padx=5, pady=5)

# Scrap %
ctk.CTkLabel(main_frame, text="Scrap Percent (%)").grid(row=8, column=0, padx=5, pady=5, sticky="e")
scrap_entry = ctk.CTkEntry(main_frame)
scrap_entry.insert(0, "3")
scrap_entry.grid(row=8, column=1, padx=5, pady=5)

# Finance %
ctk.CTkLabel(main_frame, text="Finance Percent (%)").grid(row=9, column=0, padx=5, pady=5, sticky="e")
finance_entry = ctk.CTkEntry(main_frame)
finance_entry.insert(0, "2")
finance_entry.grid(row=9, column=1, padx=5, pady=5)

# Discounts
discounts_frame = ctk.CTkFrame(app)
discounts_frame.pack(pady=10, padx=20, fill="x")
ctk.CTkLabel(discounts_frame, text="Discount Tiers (Qty ➜ Rate)", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=5)

discount1_qty = ctk.CTkEntry(discounts_frame, width=80)
discount1_qty.insert(0, "100")
discount1_qty.grid(row=1, column=0, padx=5, pady=5)
discount1_val = ctk.CTkEntry(discounts_frame, width=80)
discount1_val.insert(0, "0.9")
discount1_val.grid(row=1, column=1, padx=5, pady=5)

discount2_qty = ctk.CTkEntry(discounts_frame, width=80)
discount2_qty.insert(0, "50")
discount2_qty.grid(row=2, column=0, padx=5, pady=5)
discount2_val = ctk.CTkEntry(discounts_frame, width=80)
discount2_val.insert(0, "0.95")
discount2_val.grid(row=2, column=1, padx=5, pady=5)

# Calculate button
ctk.CTkButton(app, text="Calculate Total", command=calculate, height=40, font=("Arial", 14)).pack(pady=20)

# Result
result_label = ctk.CTkLabel(app, text="", font=("Arial", 16), justify="left", text_color="#064f04")
result_label.pack(pady=10)

# Footer
ctk.CTkLabel(app, text="© 2025 Saalim Zafar", font=("Arial", 10), text_color="gray").pack(side="bottom", pady=10)

app.mainloop()
