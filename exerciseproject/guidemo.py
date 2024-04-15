import tkinter as tk
from tkinter import ttk
from threading import Thread
import time

# Simplified function for testing 
def run_robot(origin_to, dest_to):
    print(f"Operation started from {origin_to} to {dest_to}")
    time.sleep(5)
    print(f"Operation completed from {origin_to} to {dest_to}")

def start_robot_thread(origin_to, dest_to):
    Thread(target=run_robot, args=(origin_to, dest_to)).start()

# GUI Setup
def setup_gui():
    root = tk.Tk()
    root.title("EV3 Robot Controller")

    origin_to_var = tk.StringVar()
    origin_to_label = tk.Label(root, text="From:")
    origin_to_label.pack(pady=5)
    origin_to_combobox = ttk.Combobox(root, textvariable=origin_to_var, values=['BASE', 'Line A', 'Line B', 'Line C'], state="readonly")
    origin_to_combobox.pack(padx=20,pady=5)
    origin_to_combobox.current(0)

    dest_to_var = tk.StringVar()
    dest_to_label = tk.Label(root, text="Drop to:")
    dest_to_label.pack(pady=5)
    dest_to_combobox = ttk.Combobox(root, textvariable=dest_to_var, values=['BASE', 'Line A', 'Line B', 'Line C'], state="readonly")
    dest_to_combobox.pack(padx=20,pady=5)
    dest_to_combobox.current(0)

    start_button = tk.Button(root, text="Start Operation", command=lambda: start_robot_thread(origin_to_var.get(), dest_to_var.get()))
    start_button.pack(padx=20,pady=5)

    root.mainloop()

setup_gui()