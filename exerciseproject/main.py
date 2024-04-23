#!/usr/bin/env pybricks-micropython
import socket
import json
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time



# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# If we have time: implement color coded lines with
#CSensor = ColorSensor(Port.S3)

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, wheel_diameter=54, axle_track=105)

# color = CSensor.color()

#Function from base(origin) to lines A, B & C
def base_linea():
        robot.straight(350) 

def base_linec():
    robot.turn(90)
    robot.straight(200)
    robot.turn(-90)
    robot.straight(250)
    robot.turn(90)
    robot.straight(50)
    robot.turn(-90)
    robot.straight(100)
       

def base_lineb():
    robot.turn(-90)
    robot.straight(100)
    robot.turn(90)
    robot.straight(250)
    robot.turn(-90)
    robot.straight(50)
    robot.turn(90)
    robot.straight(100)

#Return function from lines A, B & C to BASE (origin)
def linea_base():
        robot.turn(180)
        robot.straight(350) 
        robot.stop()

def linec_base():
    robot.turn(180)
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
    robot.straight(100)
    robot.turn(-90)
    robot.straight(50)
    robot.turn(90)
    robot.straight(250)
    robot.turn(-90)
    robot.straight(100)

# Dictionary mapping for our stations:
station_functions = {
    'Line A': (base_linea, linea_base),
    'Line B': (base_lineb, lineb_base),
    'Line C': (base_linec, linec_base),
}

# Run robot operations based on stations, takes two parameters:
def run_robot(origin_to, dest_to):
    if origin_to=='BASE' and dest_to in station_functions:
        #CASE 1: Robot goes from BASE(starting point) to one of the lines
        drop_func, back_func = station_functions[dest_to]
        ev3.speaker.beep(frequency=329.63, duration=100)  # Beep for picking item
        ev3.screen.print('Item picked from BASE)')   
        drop_func()  # Move from BASE to origin selected
        ev3.speaker.beep(frequency=440.00, duration=100)  # Beep for dropping items
        ev3.screen.print('Item dropped at {}.format(dest_to)') #In case it does not work, change to ev3.screen.print('Item dropped at %s' % dest_to)
        time.sleep(10)
        back_func()  # Move back to BASE


    elif origin_to in station_functions and dest_to in station_functions and origin_to != dest_to:
        #CASE 2: Robot goes from one of the lines to anothe line. Cannot be the same line for origin/destination.
        #First movement: from base to first point, back to base
        drop_func_origin, back_func_origin = station_functions[origin_to]
        drop_func_origin()  # Move from BASE to line selected
        ev3.speaker.beep(frequency=329.63, duration=100)  # Beep for picking item
        ev3.screen.print('Item picked from {}.format(origin_to)') #In case it does not work, change to ev3.screen.print('Item dropped at %s' % origin_to)
        time.sleep(10)
        back_func_origin()  # Move back to BASE
        #Second movement: from base to second point, back to base
        drop_func_dest, back_func_dest = station_functions[dest_to]
        drop_func_dest()
        ev3.speaker.beep(frequency=440.00, duration=100)  # Beep for dropping items
        ev3.screen.print('Item dropped at {}.format(dest_to)') #In case it does not work, change to ev3.screen.print('Item dropped at %s' % dest_to)
        time.sleep(10)
        back_func_dest()  # Move back to BASE        


# Setup a server socket to listen for commands.
def setup_server():
    host = ''  # Symbolic name meaning all available interfaces
    port = 12345  # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    s.listen(1)
    print("Waiting for a connection...")
    client, address = s.accept()
    print('Connected by', address)
    
    while True:
        data = client.recv(1024).decode('utf-8')
        if not data:
            break
        # Parse the received command.
        command = json.loads(data)
        origin_to = command.get('origin')
        dest_to = command.get('destination')

        # Run the robot operation.
        run_robot(origin_to, dest_to)

        # Send a response back to the client.
        response = json.dumps({'status': 'complete'})
        client.sendall(response.encode('utf-8'))

    client.close()
    s.close()

# Start the server to listen for commands from the GUI.
setup_server()