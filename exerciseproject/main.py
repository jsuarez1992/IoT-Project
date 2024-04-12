#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# Initialize. 
CSensor = ColorSensor(Port.S3)

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, wheel_diameter=54, axle_track=105)

# Write a program which makes the robot follow a black line.
# On RED, the robot shall stop.
# When the line turns blue, the robot shall reduce ist speed until the line becomes black again. 

while True:
    color = CSensor.color()
    robot.drive(200,0)    

    if color == Color.RED:
        robot.drive(200,0)         

    elif color == Color.BLUE:
        robot.stop()
        break 
    
    elif color == Color.YELLOW:
        robot.drive(50,0)
    
    wait(10)