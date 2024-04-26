import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import threading
import paho.mqtt.client as mqtt
#from paho.mqtt.client import Client  # Direct import of the Client class

MQTT_HOST = '172.20.10.2'  # Use the correct broker IP address
MQTT_PORT = 1883
MQTT_TOPIC = 'Delivery'

# MQTT Client Setup
mqtt_client = mqtt.Client()  # Directly using the imported Client class
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_start()

def update_status_label(status_label, message):
    status_label.config(text=message)

def send_command_to_ev3(origin_to, dest_to, status_label):
    if origin_to == dest_to and origin_to != 'BASE':
        messagebox.showerror("Invalid Input", "Invalid input. Lines cannot be the same.")
    else:
        command = json.dumps({"origin": origin_to, "destination": dest_to})
        mqtt_client.publish(MQTT_TOPIC, command)
        update_status_label(status_label, f"Command sent: from {origin_to} to {dest_to}")

# GUI Setup
def setup_gui():
    root = tk.Tk()
    root.geometry('600x400')
    root.title("EV3 Robot Controller")

    origin_to_var = tk.StringVar()
    origin_to_label = tk.Label(root, text="From:")
    origin_to_label.pack(pady=5)
    origin_to_combobox = ttk.Combobox(root, textvariable=origin_to_var, values=['BASE', 'Line A', 'Line B', 'Line C'], state="readonly")
    origin_to_combobox.pack(padx=20, pady=5)
    origin_to_combobox.current(0)

    dest_to_var = tk.StringVar()
    dest_to_label = tk.Label(root, text="Drop to:")
    dest_to_label.pack(pady=5)
    dest_to_combobox = ttk.Combobox(root, textvariable=dest_to_var, values=['Line A', 'Line B', 'Line C'], state="readonly")
    dest_to_combobox.pack(padx=20, pady=5)
    dest_to_combobox.current(0)

    start_button = tk.Button(root, text="Start Operation", command=lambda: threading.Thread(target=send_command_to_ev3, args=(origin_to_var.get(), dest_to_var.get(), status_label)).start())
    start_button.pack(padx=20, pady=5)

    status_label = tk.Label(root, text="Ready")
    status_label.pack(padx=20, pady=10)

    root.mainloop()

setup_gui()