import tkinter as tk
from tkinter import ttk
import socket
import json

# Replace HOST and PORT with your EV3 brick's network details
HOST = 'your.ev3.ip.address'
PORT = 12345

def send_command_to_ev3(origin_to, dest_to):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # Here we're sending a simple JSON string, but you can set up your own protocol
        command = json.dumps({"origin": origin_to, "destination": dest_to})
        s.sendall(command.encode('utf-8'))
        data = s.recv(1024)
    print(f"Received {data.decode('utf-8')}")

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

    start_button = tk.Button(root, text="Start Operation", command=lambda: send_command_to_ev3(origin_to_var.get(), dest_to_var.get()))
    start_button.pack(padx=20,pady=5)

    root.mainloop()

setup_gui()
