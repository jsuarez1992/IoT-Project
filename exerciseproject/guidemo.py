import tkinter as tk
from tkinter import ttk

# Function to perform the selected operation based on dropping station
def perform_operation():
    dropping_station = dropping_station_var.get()
    number1 = 10  # Example number, replace or make inputtable as needed
    number2 = 5   # Example number, replace or make inputtable as needed

    if dropping_station == 'Line A':
        result = number1 * number2
    elif dropping_station == 'Line B':
        result = number1 + number2
    elif dropping_station == 'Line C':
        result = number1 / number2 if number2 != 0 else 'Error: Division by zero'

    # Update the result label with the result
    result_label.config(text=f"Result: {result}")

# Set up the main application window
root = tk.Tk()
root.title("Operation Selector")

# Variables for each combobox
dropping_station_var = tk.StringVar()
starting_line_var = tk.StringVar()

# Dropdown to select the dropping station
station_label = ttk.Label(root, text="Select dropping station")
station_label.pack(pady=5)

station_combobox = ttk.Combobox(root, textvariable=dropping_station_var, state="readonly")
station_combobox['values'] = ('Line A', 'Line B', 'Line C')
station_combobox.pack(padx=10, pady=10)
station_combobox.current(0)  # set default selection

# Dropdown to select the starting line
line_label = ttk.Label(root, text="Select starting line / dropping station")
line_label.pack(pady=5)

line_combobox = ttk.Combobox(root, textvariable=starting_line_var, state="readonly")
line_combobox['values'] = ('Line A - Line C', 'Line A - Line B')
line_combobox.pack(padx=10, pady=10)
line_combobox.current(0)  # set default selection

# Button to perform operation
perform_button = ttk.Button(root, text="Perform Operation", command=perform_operation)
perform_button.pack(pady=20)

# Start the main event loop
root.mainloop()