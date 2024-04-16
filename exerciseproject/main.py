#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from threading import Thread
import tkinter as tk
import time


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
root = tk.Tk()

# Initialize. 
CSensor = ColorSensor(Port.S3)

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, wheel_diameter=54, axle_track=105)

color = CSensor.color()

def base_linea():
    if color == Color.RED:
        robot.straight(350) 

def base_linec():
    robot.turn(90)
    if color == Color.BLUE:
        robot.straight(200)
        robot.turn(-90)
        robot.straight(250)
        robot.turn(90)
        robot.straight(50)
        robot.turn(-90)
        robot.straight(100)
       

def base_lineb():
    robot.turn(-90)
    if color == Color.YELLOW:
        robot.straight(100)
        robot.turn(90)
        robot.straight(250)
        robot.turn(-90)
        robot.straight(50)
        robot.turn(90)
        robot.straight(100)

def linea_base():
    if color == Color.RED:
        robot.turn(180)
        robot.straight(350) 
        robot.stop()

def linec_base():
    robot.turn(180)
    if color == Color.BLUE:
        robot.straight(100)
        robot.turn(90)
        robot.straight(50)
        robot.turn(-90)
        robot.straight(250)
        robot.turn(90)
        robot.straight(200)
        robot.turn(90)
        robot.stop()  

def lineb_base():
    robot.turn(180)
    if color == Color.YELLOW:
        robot.straight(100)
        robot.turn(-90)
        robot.straight(50)
        robot.turn(90)
        robot.straight(250)
        robot.turn(-90)
        robot.straight(100)

# Mapping to avoid redundance:
station_functions = {
    'Line A': (base_linea, linea_base),
    'Line B': (base_lineb, lineb_base),
    'Line C': (base_linec, linec_base),
}

# Run robot operations based on stations:
def run_robot(origin_to, dest_to):
    if origin_to != 'BASE' and origin_to in station_functions:
        drop_func, back_func = station_functions[origin_to]
        drop_func()  # Move from BASE to origin selected
        ev3.screen.print(f'Item picked from {origin_to}')
        back_func()  # Move back to BASE

    if dest_to in station_functions and dest_to != 'BASE':
        drop_func, back_func = station_functions[dest_to]
        drop_func()  # Move from BASE to destination
        ev3.speaker.beep(frequency=440.00, duration=100)  # Adjust frequency based on destination
        ev3.screen.print(f'Item dropped at {dest_to}')
        time.sleep(10)
        back_func()  # Move back to BASE

# GUI Setup
def start_robot_thread(origin_to, dest_to):
    Thread(target=run_robot, args=(origin_to, dest_to)).start()

def setup_gui():
    root = tk.Tk()
    root.title("EV3 Robot Controller")

    # Dropdown for "From:"
    origin_to_var = tk.StringVar()
    origin_to_label = tk.Label(root, text="From:")
    origin_to_label.pack(padx=20,pady=5)
    origin_to_combobox = tk.ttk.Combobox(root, textvariable=origin_to_var, values=['BASE', 'Line A', 'Line B', 'Line C'], state="readonly")
    origin_to_combobox.pack(padx=20,pady=5)
    origin_to_combobox.current(0)

    # Dropdown for "Drop to:"
    dest_to_var = tk.StringVar()
    dest_to_label = tk.Label(root, text="Drop to:")
    dest_to_label.pack(padx=20,pady=5)
    dest_to_combobox = tk.ttk.Combobox(root, textvariable=dest_to_var, values=['BASE', 'Line A', 'Line B', 'Line C'], state="readonly")
    dest_to_combobox.pack(padx=20,pady=5)
    dest_to_combobox.current(0)

    # Start button
    start_button = tk.Button(root, text="Start Operation", command=lambda: start_robot_thread(origin_to_var.get(), dest_to_var.get()))
    start_button.pack(padx=20,pady=5)

    root.mainloop()

# Run the GUI
setup_gui()