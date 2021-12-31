import time
import math

a1 = 180           #90    #0
a2 = 60            #210  #120
a3 = 300           #330 #240

plane = 0,0



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

        print("lm: " + str(m2))
        print("rm: " + str(m3))
        print("bm: " + str(m1))

        print("plane: " + str(plane))
        print("")

for i in range(20):
    run(100,0,0,0)
