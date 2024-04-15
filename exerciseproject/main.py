#!/usr/bin/env pybricks-micropython
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

# Initialize. 
CSensor = ColorSensor(Port.S3)

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, wheel_diameter=54, axle_track=105)

def linea_drop():
    if color == Color.RED:
        robot.straight(350) 
        ev3.speaker.beep(frequency=440.00, duration=100)  # A note for dropping items in line A
        ev3.screen.print('Item dropped!')
        time.sleep(10) 

def linec_drop():
    robot.turn(90)
    if color == Color.BLUE:
        robot.straight(200)
        robot.turn(-90)
        robot.straight(250)
        robot.turn(90)
        robot.straight(50)
        robot.turn(-90)
        robot.straight(100)
        ev3.speaker.beep(frequency=329.63, duration=100)  # E note for dropping items in line C
        ev3.screen.print('Item dropped!')
        time.sleep(10)         

def lineb_drop():
    robot.turn(-90)
    if color == Color.YELLOW:
        robot.straight(100)
        robot.turn(90)
        robot.straight(250)
        robot.turn(-90)
        robot.straight(50)
        robot.turn(90)
        robot.straight(100)
        ev3.speaker.beep(frequency=261.63, duration=100)  # C note for dropping items in line B
        ev3.screen.print('Item dropped!')
        time.sleep(10) 

def linea_back():
    if color == Color.RED:
        robot.turn(180)
        robot.straight(350) 
        robot.stop()

def linec_back():
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

while True:  #if and only if line A is selected
    color = CSensor.color()
    linea_drop()
    linea_back()
    wait(100)