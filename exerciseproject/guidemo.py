import tkinter as tk
from tkinter import ttk
from tkinter import messagebox #for input error
import socket
import json
import paho.mqtt.publish as publish

# Define the MQTT settings to use
MQTT_HOST= 'replace.for.mqtt.broker.address'
MQTT_PORT=1883 #has to be the same as used in main.py
MQTT_TOPIC='ev3/commands'

def send_command_to_ev3(origin_to, dest_to):
    if origin_to == dest_to and origin_to != 'BASE':  # Check if lines are the same. Otherwise, error message
        messagebox.showerror("Invalid Input", "Invalid input. Lines cannot be the same.")
    else:
        command = json.dumps({"origin":origin_to,"destination":dest_to})
        try:
            publish.single(MQTT_TOPIC,payload=command,hostname=MQTT_HOST,port=MQTT_PORT)
            print(f"Sent command to topic {MQTT_TOPIC}")
        except Exception as e:
            messagebox.showerror("Connection Error",f"Failed to send command:{e}")

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
    dest_to_combobox = ttk.Combobox(root, textvariable=dest_to_var, values=['Line A', 'Line B', 'Line C'], state="readonly")
    dest_to_combobox.pack(padx=20,pady=5)
    dest_to_combobox.current(0)

    start_button = tk.Button(root, text="Start Operation", command=lambda: send_command_to_ev3(origin_to_var.get(), dest_to_var.get()))
    start_button.pack(padx=20,pady=5)

    root.mainloop()

setup_gui()
