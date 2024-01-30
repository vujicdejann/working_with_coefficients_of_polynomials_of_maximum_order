import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for matplotlib, especially for macOS
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import math

# Global variables
img = None
image_on_canvas = None

def plot_graph():
    try:
        coefficients = [float(entry.get()) for entry in entries]
        x = np.linspace(float(x_min_entry.get()), float(x_max_entry.get()), 400)
        y = sum(c * x**i for i, c in enumerate(coefficients[::-1]))
        plt.figure(figsize=(6, 4))
        plt.plot(x, y, label='f(x)')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid(True)
        plt.legend()
        plt.show()
    except ValueError:
        error_label.config(text="Greška: Unesite sve koeficijente i validan interval.")

def find_root():
    try:
        coefficients = [float(entry.get()) for entry in entries]
        a, b = float(x_min_entry.get()), float(x_max_entry.get())
        if a >= b:
            error_label.config(text="Greška: Interval nije validan.")
            return

        def f(x):
            return sum(c * x**i for i, c in enumerate(coefficients[::-1]))

        for _ in range(100):  # Max iterations
            mid = (a + b) / 2
            if f(mid) == 0 or (b - a) < 1e-6:
                root_label.config(text=f"Koren: {mid:.6f}")
                return
            if f(a) * f(mid) < 0:
                b = mid
            else:
                a = mid
        root_label.config(text="Koren nije pronađen u datom intervalu.")
    except ValueError:
        error_label.config(text="Greška: Unesite sve koeficijente i validan interval.")

def load_image():
    global img, image_on_canvas
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        tk_img = ImageTk.PhotoImage(img)
        if image_on_canvas is not None:
            canvas.delete(image_on_canvas)
        image_on_canvas = canvas.create_image(300, 200, image=tk_img, anchor=tk.CENTER)
        canvas.image = tk_img  # Keep a reference.

def apply_log_transform():
    global img, image_on_canvas
    if img is None:
        return
    c = float(log_scale.get())
    log_image = c * np.log(1 + np.array(img))
    log_image = np.array(log_image, dtype=np.uint8)
    img_log = Image.fromarray(log_image)
    tk_img_log = ImageTk.PhotoImage(img_log)
    if image_on_canvas is not None:
        canvas.delete(image_on_canvas)
    image_on_canvas = canvas.create_image(300, 200, image=tk_img_log, anchor=tk.CENTER)
    canvas.image = tk_img_log  # Keep a reference.

root = tk.Tk()
root.title("Polinom i Slika")

coefficients_frame = tk.Frame(root)
coefficients_frame.pack()

entries = [tk.Entry(coefficients_frame, width=10) for _ in range(6)]
for i, entry in enumerate(entries):
    entry.pack(side=tk.LEFT)
    tk.Label(coefficients_frame, text=f"k{i}").pack(side=tk.LEFT)

x_min_entry = tk.Entry(root, width=10)
x_min_entry.pack(side=tk.LEFT)
tk.Label(root, text="Min X").pack(side=tk.LEFT)

x_max_entry = tk.Entry(root, width=10)
x_max_entry.pack(side=tk.LEFT)
tk.Label(root, text="Max X").pack(side=tk.LEFT)

plot_button = tk.Button(root, text="Plotuj Grafik", command=plot_graph)
plot_button.pack()

root_button = tk.Button(root, text="Pronađi Koren", command=find_root)
root_button.pack()

root_label = tk.Label(root, text="Koren: ")
root_label.pack()

error_label = tk.Label(root, text="")
error_label.pack()

image_frame = tk.Frame(root)
image_frame.pack()

load_button = tk.Button(image_frame, text="Učitaj Sliku", command=load_image)
load_button.pack(side=tk.LEFT)

log_scale = tk.Spinbox(image_frame, from_=0, to=100, increment=1, width=5)
log_scale.pack(side=tk.LEFT)
apply_button = tk.Button(image_frame, text="Primeni Log Transformaciju", command=apply_log_transform)
apply_button.pack(side=tk.LEFT)

canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()
image_on_canvas = canvas.create_image(300, 200, anchor=tk.CENTER, image=None)

root.mainloop()