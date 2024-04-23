import tkinter as tk
from tkinter import ttk
from tkinter import messagebox #for input error
import socket
import json
import paho.mqtt.publish as publish
import threading


MQTT_HOST= 'replace.for.mqtt.broker.address'
MQTT_PORT=1883 #has to be the same as used in main.py
MQTT_TOPIC='ev3/commands'

def update_status_label(status_label, message):
    status_label.config(text=message)

def send_command_to_ev3(origin_to, dest_to, status_label):
    if origin_to == dest_to and origin_to != 'BASE':
        messagebox.showerror("Invalid Input", "Invalid input. Lines cannot be the same.")
    else:
        command = json.dumps({"origin":origin_to, "destination":dest_to})
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((MQTT_HOST, MQTT_PORT))
            s.sendall(command.encode('utf-8'))

            while True:
                data = s.recv(1024).decode('utf-8')
                if not data:
                    break
                response = json.loads(data)
                if response['status'] == 'update' or response['status'] == 'complete':
                    status_label.after(0, update_status_label, status_label, response['message']) #implement after to update status_label from thread to avoid GUI freexing
                    if response['status'] == 'complete':
                        break

            s.close()
        except Exception as e:
            status_label.after(0, update_status_label, status_label, "Connection Error")


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

    start_button = tk.Button(root, text="Start Operation", command=lambda: threading.Thread(target=send_command_to_ev3, args=(origin_to_var.get(), dest_to_var.get(), status_label)).start())
    start_button.pack(padx=20,pady=5)

    status_label = tk.Label(root, text="Ready")
    status_label.pack(padx=20, pady=10)    

    root.mainloop()

setup_gui()
