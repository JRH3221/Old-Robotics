#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from pybricks.iodevices import Ev3devSensor
import time
import math

ev3 = EV3Brick()

lm = Motor(Port.A)
rm = Motor(Port.B)
back = Motor(Port.C)
ir = Ev3devsensor(Port.S1)
compass = Ev3devsensor(Port.S3)
##sonic = Ultrasonicsensor(Port.S2)##

a1 = 180           #90    #0
a2 = 60            #210  #120
a3 = 300           #330 #240

plane = 0,0

Running = True

margin_y = 100
margin_x = 50
point = 1


def run(speed, heading, turn_speed, degrees): #speed in mm/s

        global plane

        ###
        heading = heading * -1 #invert heading

        o1 = a1 - heading
        m1 = speed * math.sin(math.radians(o1)) #calculate ground speed for back wheel

        o2 = a2 - heading
        m2 = speed * math.sin(math.radians(o2)) #calculate ground speed for left wheel

        o3 = a3 - heading
        m3 = speed * math.sin(math.radians(o3)) #calculate ground speed for right wheel

        m1 = int(round(m1)) #round all wheel speeds
        m2 = int(round(m2))
        m3 = int(round(m3))

        m1 = m1 + turn_speed #if any turn speed is needed it adds it so it moves while turning
        m2 = m2 + turn_speed
        m3 = m3 + turn_speed
        ###

        back.run(m1) #runs the motors
        lm.run(m2)
        rm.run(m3)


        heading = heading * -1

        ##
        if heading + degrees > 359:
            heading = (heading + degrees) - 360 #accounts for the robots rotation
        else:
            heading = heading + degrees
        ##

        ###
        if heading == 90: #####plotting the y and x of the robot in mm
            plane = plane[0],plane[1] + speed

        elif heading == 180:
            plane = plane[0] = speed * -1,plane[1]

        elif heading == 270:
            plane = plane[0],plane[1] + speed * -1

        else:
            plane = (plane[0] + (speed * math.cos(math.radians(heading))), plane[1] + (speed * math.sin(math.radians(heading))))


        plane = int(round(plane[0])),int(round(plane[1])) #rounds the y and x value

        plane = str(plane[0]/10000),str(plane[1]/10000) #to calculate the division number, take the raw (probably close to 200000) from 1 measured point to another, then divide the raw by the actual distance to get the number to input here



while Running == True:
    
    degrees = int(compass('DC'))

    if point == 1:
        if plane[0] < margin_y:
            run(100,0,0,0)
        else:
            point = 2
            time.sleep(1)

    elif point == 2:
        if plane[0] > 0:
            run(-100,0,0,0)
        else:
            point = 3
            time.sleep(1)

    elif point == 3:
        if plane[1] < margin_x:
            run(90,0,0,0)
        else:
            point = 4
            time.sleep(1)

    elif point == 4:
        if plane[1] > 0:
            run(270,0,0,0)
        else:
            point = 5
            ev3.speaker.beep()
            time.sleep()

    ######
    elif point == 5:
        if plane[0] < margin_y:
            run(100, 360 - degrees, 50, degrees)
        else:
            point = 6
            time.sleep()

    elif point == 6:
        if plane[0] > 0:
            run(100, 360 - degrees, -50, degrees)
        else:
            point = 10
            Running = False



    
