import tkinter as tk

root = tk.Tk()
root.title("Inben Demo App")
root.geometry("300x200")

tk.Label(root, text="✅ Inben Demo App Running!!", font=("Segoe UI", 12)).pack(pady=30)
tk.Button(root, text="Close", command=root.destroy).pack(pady=10)

root.mainloop()
