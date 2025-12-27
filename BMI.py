#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import re

# ---------- Helpers ----------
def parse_number(s):
    """Extract a float from a string like '175', '1.75', '1,75', '175 cm' etc."""
    if s is None:
        raise ValueError("Empty input")
    s = s.strip().replace(',', '.')
    m = re.search(r'[-+]?\d*\.?\d+', s)
    if not m:
        raise ValueError(f"Couldn't parse number from '{s}'")
    return float(m.group())

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "#00BFFF"
    elif bmi < 25:
        return "Normal weight", "#32CD32"
    elif bmi < 30:
        return "Overweight", "#FFD700"
    else:
        return "Obese", "#FF4500"

# ---------- UI Setup ----------
root = tk.Tk()
root.title("Animated BMI Calculator")
root.geometry("440x360")
root.configure(bg="#222831")

title = tk.Label(root, text="💪 BMI CALCULATOR", font=("Segoe UI", 20, "bold"),
                 bg="#222831", fg="#FFD369")
title.pack(pady=12)

frm = tk.Frame(root, bg="#393E46", bd=6, relief="ridge")
frm.pack(padx=12, pady=10, fill="x")

tk.Label(frm, text="Weight (kg):", bg="#393E46", fg="white").grid(row=0, column=0, sticky="w", padx=6, pady=6)
weight_var = tk.StringVar()
weight_entry = tk.Entry(frm, textvariable=weight_var, font=("Segoe UI", 12))
weight_entry.grid(row=0, column=1, padx=6, pady=6)

tk.Label(frm, text="Height (m or cm):", bg="#393E46", fg="white").grid(row=1, column=0, sticky="w", padx=6, pady=6)
height_var = tk.StringVar()
height_entry = tk.Entry(frm, textvariable=height_var, font=("Segoe UI", 12))
height_entry.grid(row=1, column=1, padx=6, pady=6)

calc_btn = tk.Button(root, text="Calculate BMI", font=("Segoe UI", 12, "bold"),
                     bg="#FFD369", fg="#222831", command=lambda: calculate_bmi())
calc_btn.pack(pady=8)

bmi_var = tk.StringVar(value="")
bmi_label = tk.Label(root, textvariable=bmi_var, font=("Segoe UI", 16, "bold"),
                     bg="#222831", fg="#EEEEEE")
bmi_label.pack()

result_var = tk.StringVar(value="")
result_label = tk.Label(root, textvariable=result_var, font=("Segoe UI", 14, "bold"),
                        bg="#222831")
result_label.pack(pady=4)

pb = ttk.Progressbar(root, orient="horizontal", length=340, mode="determinate", maximum=40)
pb.pack(pady=8)

# ---------- Animation functions (non-blocking) ----------
def animate_title(colors=("#FFD369", "#00ADB5", "#FF2E63", "#76ABAE"), i=0):
    title.config(fg=colors[i % len(colors)])
    root.after(350, lambda: animate_title(colors, i+1))

def animate_progress(target_bmi):
    """Smoothly move the progressbar value toward target_bmi"""
    current = pb['value']
    if abs(current - target_bmi) < 0.5:
        pb['value'] = target_bmi
        return
    step = min(1.8, abs(target_bmi - current))
    pb['value'] = current + step if target_bmi > current else current - step
    root.after(12, lambda: animate_progress(target_bmi))

def animate_result_color(i=0):
    """Gently cycle result label colors"""
    colors = ("#FFD369", "#FFFFFF", "#00ADB5", "#FF2E63")
    result_label.config(fg=colors[i % len(colors)])
    root.after(250, lambda: animate_result_color(i+1))

# ---------- Calculation ----------
def calculate_bmi():
    try:
        w = parse_number(weight_var.get())
        h_raw = height_var.get()
        h = parse_number(h_raw)

        # If height looks like centimeters (e.g. 170), convert to meters
        if h > 3:  # anything > 3 meters is almost certainly cm, convert
            h = h / 100.0

        if h <= 0:
            raise ValueError("Height must be > 0")
        if w <= 0:
            raise ValueError("Weight must be > 0")

        bmi = w / (h * h)
        bmi_var.set(f"Your BMI: {bmi:.2f}")
        cat, color = bmi_category(bmi)
        result_var.set(cat)
        result_label.config(fg=color)

        # animate progress bar mapped to 0..40 (clamp)
        animate_progress(min(max(bmi, 0), 40))
        animate_result_color()

    except ValueError as e:
        messagebox.showerror("Input error", str(e))

# ---------- Start UI ----------
animate_title()
root.mainloop()
