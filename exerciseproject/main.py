#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import json
from umqtt.robust import MQTTClient
import time

# MQTT setup
MQTT_ClientID = 'Robot'
MQTT_Broker = '127.0.0.1' # Change ip address to correct one
MQTT_Topic_Delivery = 'Delivery'
client = MQTTClient(MQTT_ClientID, MQTT_Broker)

# Callback to test connection
def listen(topic,msg):
    if topic == MQTT_Topic_Delivery.encode():
        message = str(msg.decode())

        ev3.screen.print(message)

# Callback to handle MQTT messages
def message_callback(topic, msg):
    command = json.loads(msg.decode())
    origin_to = command['origin']
    dest_to = command['destination']
    run_robot(client,origin_to, dest_to)


# Subscribe to the MQTT topic
client.connect()
#client.set_callback(listen)
client.set_callback(message_callback)
client.subscribe(MQTT_Topic_Delivery)

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

#adjust the turning to take the wheels in consideration:
def adjusted_turn(degrees):
    correction_factor=1.06
    robot.turn(degrees*correction_factor)

#Function from base(origin) to lines A, B & C
def base_linea():
        robot.straight(1050) 

def base_linec():
    adjusted_turn(90)
    robot.straight(600)
    adjusted_turn(-90)
    robot.straight(750)
    adjusted_turn(90)
    robot.straight(150)
    adjusted_turn(-90)
    robot.straight(300)
       

def base_lineb():
    adjusted_turn(-90)
    robot.straight(300)
    adjusted_turn(90)
    robot.straight(750)
    adjusted_turn(-90)
    robot.straight(150)
    adjusted_turn(90)
    robot.straight(300)

#Return function from lines A, B & C to BASE (origin)
def linea_base():
        adjusted_turn(180)
        robot.straight(1050) 
        robot.stop()

def linec_base():
    adjusted_turn(180)
    robot.straight(300)
    adjusted_turn(90)
    robot.straight(150)
    adjusted_turn(-90)
    robot.straight(750)
    adjusted_turn(90)
    robot.straight(600)
    adjusted_turn(-90)
    robot.stop()  

def lineb_base():
    adjusted_turn(180)
    robot.straight(300)
    adjusted_turn(-90)
    robot.straight(150)
    adjusted_turn(90)
    robot.straight(750)
    adjusted_turn(-90)
    robot.straight(300)

def turn_base_on_origin(origin_to):
    if origin_to=='Line A':
        adjusted_turn(180)
    elif origin_to=='Line B':
        adjusted_turn(-90)
    elif origin_to=='Line C':
        adjusted_turn(-90)

# Dictionary mapping for our stations:
station_functions = {
    'Line A': (base_linea, linea_base),
    'Line B': (base_lineb, lineb_base),
    'Line C': (base_linec, linec_base),
}

# Run robot operations based on stations, takes two parameters:
def run_robot(client,origin_to, dest_to):
    if origin_to=='BASE' and dest_to in station_functions:
        #CASE 1: Robot goes from BASE(starting point) to one of the lines
        drop_func, back_func = station_functions[dest_to]
        ev3.speaker.beep(frequency=329.63, duration=100)  # Beep for picking item
        ev3.screen.clear()
        ev3.screen.print('Item picked from \nBASE)') 
        send_status(client,'Item picked from \nBASE')
        drop_func()  # Move from BASE to origin selected
        ev3.speaker.beep(frequency=440.00, duration=100)  # Beep for dropping items
        ev3.screen.clear()
        ev3.screen.print('Item dropped at \n%s' % dest_to) #In case it does not work, change to ev3.screen.print('Item dropped at %s' % dest_to)
        send_status(client,'Item dropped at {dest_to}') 
        time.sleep(5)
        back_func()  # Move back to BASE
        
        


    elif origin_to in station_functions and dest_to in station_functions and origin_to != dest_to:
        #CASE 2: Robot goes from one of the lines to anothe line. Cannot be the same line for origin/destination.
        #First movement: from base to first point, back to base
        drop_func_origin, back_func_origin = station_functions[origin_to]
        drop_func_origin()  # Move from BASE to line selected
        ev3.speaker.beep(frequency=329.63, duration=100)  # Beep for picking item
        ev3.screen.clear()
        ev3.screen.print('Item picked from \n%s' % origin_to) #In case it does not work, change to ev3.screen.print('Item dropped at %s' % origin_to)
        timestamp = time.time()        
        send_status(client,'Item picked from {origin_to}') 
        time.sleep(5)
        back_func_origin()  # Move back to BASE
        #Second movement: from base to second point, back to base
        turn_base_on_origin(origin_to)
        drop_func_dest, back_func_dest = station_functions[dest_to]
        drop_func_dest()
        ev3.speaker.beep(frequency=440.00, duration=100)  # Beep for dropping items
        ev3.screen.print('Item dropped at \n%s' % dest_to) #In case it does not work, change to ev3.screen.print('Item dropped at %s' % dest_to)
        message = "Item delivered at {dest_to} - Timestamp: {}".format(timestamp)        
        send_status(client,'Item dropped at {dest_to}') 
        client.publish(MQTT_Topic_Delivery, message.encode())
        time.sleep(5)
        back_func_dest()  # Move back to BASE     
       
        

def send_status(client, message):
    """ Send a status update to the GUI. """
    response = json.dumps({'status': 'update', 'message': message})
    #client.sendall(response.encode('utf-8'))

# Main loop to keep checking for new messages
def main_loop():
    while True:
        client.check_msg()
        wait(100)  # Slight delay to reduce CPU usage

ev3.speaker.beep()
main_loop()