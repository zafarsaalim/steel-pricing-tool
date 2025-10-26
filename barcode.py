#!/usr/bin/env python3
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# ------------------------
# Functions
# ------------------------

def scan_barcode_from_image(path):
    try:
        img = Image.open(path)
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open image:\n{e}")
        return None

    decoded = decode(img)
    if decoded:
        return decoded[0].data.decode("utf-8")
    else:
        return None

def scan_barcode_webcam(entry_widget):
    """
    Open webcam and detect barcode/QR
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showwarning("Webcam Error", "Cannot open webcam. Try selecting an image instead.")
        return

    cv2.namedWindow("Scan Barcode/QR (Press q to quit)")
    barcode_found = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoded_objs = decode(frame)
        for obj in decoded_objs:
            barcode_found = obj.data.decode("utf-8")
            # Draw rectangle
            pts = obj.polygon
            if len(pts) > 4:
                hull = cv2.convexHull(np.array([p for p in pts], dtype=np.float32))
                pts = list(map(tuple, hull.squeeze()))
            for i in range(len(pts)):
                cv2.line(frame, pts[i], pts[(i + 1) % len(pts)], (0, 255, 0), 2)
            x, y = pts[0]
            cv2.putText(frame, barcode_found, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Scan Barcode/QR (Press q to quit)", frame)

        if barcode_found:
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    if barcode_found:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, barcode_found)

def on_scan_button(entry_widget):
    # Try webcam in separate thread so GUI doesn't freeze
    threading.Thread(target=scan_barcode_webcam, args=(entry_widget,), daemon=True).start()

def on_load_image(entry_widget):
    path = filedialog.askopenfilename(title="Select image",
                                      filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if path:
        result = scan_barcode_from_image(path)
        if result:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, result)
        else:
            messagebox.showinfo("Result", "No barcode/QR found in the image.")

# ------------------------
# GUI
# ------------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Barcode/QR Scanner GUI")
root.geometry("450x200")

frame = ctk.CTkFrame(root, corner_radius=10)
frame.pack(padx=20, pady=20, fill="both", expand=True)

label = ctk.CTkLabel(frame, text="Barcode / QR value:")
label.pack(pady=(10,5))

entry = ctk.CTkEntry(frame, width=300)
entry.pack(pady=5)

btn_frame = ctk.CTkFrame(frame)
btn_frame.pack(pady=10)

scan_btn = ctk.CTkButton(btn_frame, text="Scan from Webcam", command=lambda: on_scan_button(entry))
scan_btn.grid(row=0, column=0, padx=5)

load_btn = ctk.CTkButton(btn_frame, text="Load Image", command=lambda: on_load_image(entry))
load_btn.grid(row=0, column=1, padx=5)

root.mainloop()
