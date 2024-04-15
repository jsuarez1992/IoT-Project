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

# Run robot operations based on selected paths
def run_robot(origin_to, dest_to):
    if origin_to != 'BASE':
        if origin_to == 'Line A' & dest_to=='Line C':
            base_linea()
            ev3.screen.print('Item picked from Line A')
            linea_base()
            base_linec()
            ev3.speaker.beep(frequency=261.63, duration=100)  # C note for dropping items in line B
            ev3.screen.print('Item dropped!')
            time.sleep(10)             
            linec_base()
        elif origin_to == 'Line B' & dest_to=='Line A':
            base_lineb()
            ev3.screen.print('Item picked from Line B')
            lineb_base()
            base_linea()
            ev3.speaker.beep(frequency=440.00, duration=100)  # A note for dropping items in line A
            ev3.screen.print('Item dropped!')
            time.sleep(10)             
            linea_base()
        elif origin_to == 'Line C' & dest_to=='Line A':
            base_linec()
            ev3.screen.print('Item picked from Line C')
            linec_base()
            base_linea()
            ev3.speaker.beep(frequency=440.00, duration=100)  # A note for dropping items in line A
            ev3.screen.print('Item dropped!')
            time.sleep(10) 
            linea_base()
        elif origin_to == 'Line C' & dest_to=='Line B':
            base_linec()
            ev3.screen.print('Item picked from Line C')
            linec_base()
            base_lineb()
            ev3.speaker.beep(frequency=261.63, duration=100)  # C note for dropping items in line B
            ev3.screen.print('Item dropped!')
            time.sleep(10) 
            lineb_base()      
        elif origin_to == 'Line A' & dest_to=='Line B':
            base_linea()
            ev3.screen.print('Item picked from Line A')
            linea_base()
            base_lineb()
            ev3.speaker.beep(frequency=261.63, duration=100)  # C note for dropping items in line B
            ev3.screen.print('Item dropped!')
            time.sleep(10)             
            lineb_base()
        elif origin_to == 'Line B' & dest_to=='Line C':                      
            base_lineb()
            ev3.screen.print('Item picked from Line B')
            lineb_base()
            base_linec()
            ev3.speaker.beep(frequency=440.00, duration=100)  # A note for dropping items in line A
            ev3.screen.print('Item dropped!')
            time.sleep(10)             
            linec_base()
    if dest_to == 'Line A':        
        base_linea()
        ev3.speaker.beep(frequency=440.00, duration=100)  # A note for dropping items in line A
        ev3.screen.print('Item dropped!')
        time.sleep(10) 
        linea_base()
        
    elif dest_to == 'Line B':        
        base_lineb()
        ev3.speaker.beep(frequency=261.63, duration=100)  # C note for dropping items in line B
        ev3.screen.print('Item dropped!')
        time.sleep(10) 
        lineb_base()
    elif dest_to == 'Line C':        
        base_linec()
        ev3.speaker.beep(frequency=329.63, duration=100)  # E note for dropping items in line C
        ev3.screen.print('Item dropped!')
        time.sleep(10)         
        linec_base()

# GUI Setup
def start_robot_thread(origin_to, dest_to):
    Thread(target=run_robot, args=(origin_to, dest_to)).start()

def setup_gui():
    root = tk.Tk()
    root.title("EV3 Robot Controller")

    # Dropdown for "Drop to"
    origin_to_var = tk.StringVar()
    origin_to_label = tk.Label(root, text="From:")
    origin_to_label.pack(pady=5)
    origin_to_combobox = tk.ttk.Combobox(root, textvariable=origin_to_var, values=['Line A', 'Line B', 'Line C','Base'], state="readonly")
    origin_to_combobox.pack(pady=5)
    origin_to_combobox.current(0)

    # Dropdown for "Pickup to"
    dest_to_var = tk.StringVar()
    dest_to_label = tk.Label(root, text="Drop to:")
    dest_to_label.pack(pady=5)
    dest_to_combobox = tk.ttk.Combobox(root, textvariable=dest_to_var, values=['BASE', 'Line A', 'Line B', 'Line C'], state="readonly")
    dest_to_combobox.pack(pady=5)
    dest_to_combobox.current(0)

    # Start button
    start_button = tk.Button(root, text="Start Operation", command=lambda: start_robot_thread(origin_to_var.get(), dest_to_var.get()))
    start_button.pack(pady=20)

    root.mainloop()

# Run the GUI
setup_gui()