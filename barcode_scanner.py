import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
from pyzbar import pyzbar
from PIL import Image, ImageTk

# --- Barcode scanning functions ---
def decode_barcode(image):
    barcodes = pyzbar.decode(image)
    if barcodes:
        return barcodes[0].data.decode('utf-8')
    return None

def scan_from_camera():
    # Attempt to open camera; if fails, fallback to message
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot access camera")
            return
        messagebox.showinfo("Info", "Press 'q' to quit scanning")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            barcode = decode_barcode(frame)
            cv2.imshow("Scan Barcode - Press q to exit", frame)
            if barcode:
                messagebox.showinfo("Barcode Found", barcode)
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        messagebox.showerror("Camera Error", f"Cannot access camera:\n{e}")

def scan_from_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    image = cv2.imread(file_path)
    if image is None:
        messagebox.showerror("Error", "Failed to read image")
        return
    barcode = decode_barcode(image)
    if barcode:
        messagebox.showinfo("Barcode Found", barcode)
    else:
        messagebox.showinfo("Result", "No barcode detected")

def manual_input():
    code = entry.get()
    if code.strip() == "":
        messagebox.showwarning("Warning", "Enter a barcode manually")
        return
    messagebox.showinfo("Manual Input", f"Barcode: {code}")

# --- GUI setup ---
def main():
    global entry
    root = tk.Tk()
    root.title("Simple Barcode Scanner")

    tk.Label(root, text="Manual Barcode Input:").pack(pady=5)
    entry = tk.Entry(root, width=40)
    entry.pack(pady=5)
    tk.Button(root, text="Submit Manual Input", command=manual_input).pack(pady=5)

    tk.Label(root, text="OR").pack(pady=5)
    tk.Button(root, text="Scan from Camera", command=scan_from_camera).pack(pady=5)
    tk.Button(root, text="Scan from Image", command=scan_from_image).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
