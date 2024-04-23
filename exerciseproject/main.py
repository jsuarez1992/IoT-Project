#!/usr/bin/env pybricks-micropython

# from ./my_packages import guidemo > if we decide to run GUI also from main
# from my_packages import mqtt_client > the computer's MQTT server, we need to add this main the robot's mqtt parameters


import socket # Do we use this? 
import json
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

from umqtt.robust import MQTTClient

# MQTT setup
MQTT_ClientID = 'Robot'
MQTT_Broker = '192.168.218.115' # Change ip address to correct one
MQTT_Topic_Delivery = 'Delivery'
client = MQTTClient(MQTT_ClientID, MQTT_Broker)

# Subscribe to the MQTT topic
client.subscribe(MQTT_Topic_Delivery)

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# Initialize. 
#CSensor = ColorSensor(Port.S3)

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, wheel_diameter=54, axle_track=105)

#color = CSensor.color()

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
        ev3.screen.print('Item picked from {origin_to}')
        back_func()  # Move back to BASE

    if dest_to in station_functions and dest_to != 'BASE':
        drop_func, back_func = station_functions[dest_to]
        drop_func()  # Move from BASE to destination
        ev3.speaker.beep(frequency=440.00, duration=100)  # Adjust frequency based on destination
        ev3.screen.print('Item dropped at {dest_to}')

        # Generate timestamp
        timestamp = time.time()
        # Prepare message with timestamp
        message = "Item delivered at {dest_to} - Timestamp: {}".format(timestamp)

        # Publish message to the MQTT broker when item is dropped at destination
        client.publish(MQTT_Topic_Delivery, message.encode())

        time.sleep(10)
        back_func()  # Move back to BASE

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

# but while true loop here?
    client.close() # have main loop here to run? 
    s.close() # check this! Robot can stop but program cannot!!!

# Start the server to listen for commands from the GUI.
setup_server()