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

max_speed = 200
run_speed = 100

plane = 0,0

margin_y = 20 #from start to forward goal
margin_x = 10 # from start to the right

ev3.screen.print("On")

def reset():
    global plane

    lm.stop()
    rm.stop()
    back.stop()

    plane = 0,0

    time.sleep(1)
    resetting = True
    while resetting:
        if str(ev3.buttons.pressed()) == "CENTER":
            resetting = False
            ev3.speaker.beep()
            break


class robot():

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


while True:
    #AC mode is more tuned to the modern ball and beacons
    #DC has no filtering and will pick up anything
    degrees = int(compass('DC'))
    ball = str(ir.read("AC"))

    if str(ev3.buttons.pressed()) == "CENTER":
        ev3.speaker.beep()
        ev3.screen.print("Off")
        reset()
        ev3.screen.print("On")
        


    if plane[0] < (margin_y - 20) and plane[1] < (margin_x - 20) and plane[1] > (margin_x * -1) + 20:

        if ball != "(0,)":

            if degrees > 350 and degrees < 10:
                if ball == "(1,)" or ball == "(9,":
                    robot.drive(run_speed,180,0,degrees)
                elif ball == "(2,)":
                    robot.drive(run_speed,240,0,degrees)
                elif ball == "(3,)":
                    robot.drive(run_speed,270,0,degrees)
                elif ball == "(4,)":
                    robot.drive(run_speed,300,0,degrees)
                elif ball == "(5,)":
                    robot.drive(max_speed,0,0,degrees)
                elif ball == "(6,)":
                    robot.drive(run_speed,60,0,degrees)
                elif ball == "(7,)":
                    robot.drive(run_speed,90,0,degrees)
                elif ball == "(8,)":
                    robot.drive(run_speed,120,0,degrees)

            elif degrees > 180:
                #rotate clockwise
                if ball == "(1,)" or ball == "(9,":
                    robot.drive(run_speed,180,0,degrees)
                elif ball == "(2,)":
                    robot.drive(run_speed,240,45,degrees)
                elif ball == "(3,)":
                    robot.drive(run_speed,90,45,degrees)
                elif ball == "(4,)":
                    robot.drive(run_speed,90,45,degrees)
                elif ball == "(5,)":
                    robot.drive(run_speed,315,45,degrees)
                elif ball == "(6,)":
                    robot.drive(run_speed,0,degrees,degrees)
                elif ball == "(7,)":
                    robot.drive(run_speed,0,degrees,degrees)
                elif ball == "(8,)":
                    robot.drive(run_speed,120,45,degrees)
    
            else:
                #rotate anticlockwise
                if ball == "(1,)" or ball == "(9,":
                    robot.drive(run_speed,180,0,degrees)  
                elif ball == "(2,)":
                    robot.drive(run_speed,240,-45,degrees)
                elif ball == "(3,)":
                    robot.drive(run_speed,0,degrees *-1,degrees)
                elif ball == "(4,)":
                    robot.drive(run_speed,0,degrees *-1,degrees)
                elif ball == "(5,)":
                    robot.drive(run_speed,45,-45,degrees)
                elif ball == "(6,)":
                    robot.drive(run_speed,90,-45,degrees)
                elif ball == "(7,)":
                    robot.drive(run_speed,90,-45,degrees)
                elif ball == "(8,)":
                    robot.drive(run_speed,120,-45,degrees)

        elif str(ir.read("DC")) != "(0,)": ##DC detect lower latency move straight towards ball unaccounting for rotation and current position on the field
            print("DC detect")
            if ball == "(1,)":
                #240
                robot.drive(max_speed,240,0,degrees)
            if ball == "(2,)":
                #270
                robot.drive(max_speed,270,0,degrees)
            if ball == "(3,)":
                robot.drive(max_speed,300,0,degrees)
            if ball == "(4,)":
                robot.drive(max_speed,330,0,degrees)
            if ball == "(5,)":
                robot.drive(max_speed,0,0,degrees)
            if ball == "(6,)":
                robot.drive(max_speed,30,0,degrees)
            if ball == "(7,)":
                robot.drive(max_speed,60,0,degrees)
            if ball == "(8,)":
                robot.dribr(max_speed,90,0,degrees)
            if ball == "(9,)":
                robot.drive(max_speed,120,0,degrees)

        else:
            robot.drive(0,0,360)
    elif plane[0] >= margin_y + 20:
        ## place holder
        # this means the robot is close to the front bounderies
        back.stop()
        lm.stop()
        rm.stop()

    elif plane[1] >= margin_x + 20:
        # this means the robot is close to the right side of the pitch
        if ball == "(0,)":
            if degrees != 0:
                if degrees > 180:
                    robot.drive(0,0,90,degrees)
                else:
                    robot.drive(0,0,-90,degrees)
            else:
                robot.drive(max_speed,270,0,degrees)
        else:
            if degrees > 350 and degrees < 10:
                if ball == "(1,)" or ball == "(9,":
                    robot.drive(run_speed,180,0,degrees)
                elif ball == "(2,)":
                    robot.drive(run_speed,240,0,degrees)
                elif ball == "(3,)":
                    robot.drive(run_speed,270,0,degrees)
                elif ball == "(4,)":
                    robot.drive(run_speed,300,0,degrees)
                elif ball == "(5,)":
                    robot.drive(max_speed,0,0,degrees)
                elif ball == "(6,)":
                    robot.drive(run_speed,60,0,degrees)
                elif ball == "(7,)":
                    robot.drive(run_speed,90,0,degrees)
                elif ball == "(8,)":
                    robot.drive(run_speed,120,0,degrees)

            elif degrees > 180:
                #rotate clockwise
                if ball == "(1,)" or ball == "(9,":
                    robot.drive(run_speed,180,0,degrees)
                elif ball == "(2,)":
                    robot.drive(run_speed,240,45,degrees)
                elif ball == "(3,)":
                    robot.drive(run_speed,90,45,degrees)
                elif ball == "(4,)":
                    robot.drive(run_speed,90,45,degrees)
                elif ball == "(5,)":
                    robot.drive(run_speed,315,45,degrees)
                elif ball == "(6,)":
                    robot.drive(run_speed,0,degrees,degrees)
                elif ball == "(7,)":
                    robot.drive(run_speed,0,degrees,degrees)
                elif ball == "(8,)":
                    robot.drive(run_speed,120,45,degrees)
    
            else:
                #rotate anticlockwise
                if ball == "(1,)" or ball == "(9,":
                    robot.drive(run_speed,180,0,degrees)  
                elif ball == "(2,)":
                    robot.drive(run_speed,240,-45,degrees)
                elif ball == "(3,)":
                    robot.drive(run_speed,0,degrees *-1,degrees)
                elif ball == "(4,)":
                    robot.drive(run_speed,0,degrees *-1,degrees)
                elif ball == "(5,)":
                    robot.drive(run_speed,45,-45,degrees)
                elif ball == "(6,)":
                    robot.drive(run_speed,90,-45,degrees)
                elif ball == "(7,)":
                    robot.drive(run_speed,90,-45,degrees)
                elif ball == "(8,)":
                    robot.drive(run_speed,120,-45,degrees)

    else:
        ## place holder
        # this means the robot is close to the left of the pitch
        back.stop()
        lm.stop()
        rm.stop()