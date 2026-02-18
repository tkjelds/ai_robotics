from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import multitask, run_task
from urandom import randint

hub = PrimeHub()
sensorRight = ColorSensor(Port.B)
sensorLeft = ColorSensor(Port.A)
sensorVertical = ColorSensor(Port.D)

rightWheel = Motor(Port.F)
leftWheel = Motor(Port.E, Direction.COUNTERCLOCKWISE)

robot = DriveBase(leftWheel, rightWheel, wheel_diameter=55, axle_track=115)

hsvRight = None
colorRight = None
ambientRight = None
hsvLeft = None
colorLeft = None
ambientLeft = None
hsvVert = None
colorVert = None
ambientVert = None

def measureLeft():
    global hsvLeft
    hsvLeft = sensorLeft.hsv(surface=True)
    global colorLeft
    colorLeft = sensorLeft.color(surface=True)
    global ambientLeft
    ambientLeft = sensorLeft.ambient()

def measureRight():
    global hsvRight
    hsvRight = sensorRight.hsv(surface=True)
    global colorRight
    colorRight = sensorRight.color(surface=True)
    global ambientRight
    ambientRight = sensorRight.ambient()

"""def measureVert():
    global hsvVert
    hsvVert = sensorVertical.hsv(surface=True)
    global colorVert
    colorVert = sensorVertical.color(surface=True)
    global ambientVert
    ambientVert = sensorVertical.ambient()"""

def measureAll():
    measureLeft()
    measureRight()
    #measureVert()

def printVals():
    print("hsvRight =", hsvRight, ", colorRight = ", colorRight, ", ambientRight = ", ambientRight)
    print("hsvLeft =", hsvLeft, ", colorLeft = ", colorLeft, ", ambientLeft = ", ambientLeft)
    print("hsvVert =", hsvVert, ", colorVert = ", colorVert, ", ambientVert = ", ambientVert)

def goStraight(dist):
    wheel_circ = 3.1415 * 5.5 # 2.75 = radius of wheel
    rightWheel.dc(50)
    leftWheel.dc(50)
    wait((800/wheel_circ) * dist)

def goBackwards(dist):
    wheel_circ = 3.1415 * 5.5 # 2.75 = radius of wheel
    rightWheel.dc(-50)
    leftWheel.dc(-50)
    wait((800/wheel_circ) * dist)

def brakeWheels():
    leftWheel.hold()
    rightWheel.hold()

def turnRight(degrees):
    rightWheel.dc(-50)
    leftWheel.dc(50)
    wait(degrees*5.33) #5.33 temp value, works best w/ speed50 and 180degrees

def turnLeft(degrees):
    rightWheel.dc(50)
    leftWheel.dc(-50)
    wait(degrees*5.33) #5.33 temp value, works best w/ speed50 and 180degrees 

vertReflectionLimit = 10

robot.settings(500,1000,500,500)

Sen_Vec = [0,0,0]

def normalizeMiddle(x):
    if x > 0:
        return 1
    else:
        return 0

def normalizeSides(x):
    if x != 2:
        return 1
    else:
        return 0

def behavior(Sen_Vec):
    leftOrRight = randint(0,1)
    if(Sen_Vec == [0,1,1] or Sen_Vec == [1,0,1] or Sen_Vec == [1,1,1]):
        if(leftOrRight == 0):
            turnLeft(3)
        else:
            turnRight(3)
    elif(Sen_Vec == [0,0,0]):
        robot.straight(20, wait=False)
    elif(Sen_Vec == [1,0,0]):
        turnRight(3)
    elif(Sen_Vec == [0,1,0]):
        turnLeft(3)
    elif(Sen_Vec == [1,1,0]):
        #Go backwards:
        # robot.straight(-20, wait=False)
        degrees = randint(45,180)
        if(leftOrRight == 0):
            turnLeft(degrees)
        else:
            turnRight(degrees)

while(True):
    sensorLeftVal = normalizeSides(sensorLeft.reflection())
    sensorRightVal = normalizeSides(sensorRight.reflection())
    sensorVerticalVal = normalizeMiddle(sensorVertical.reflection())

    #print("left", sensorLeft.reflection())
    #print("right", sensorRight.reflection())

    Sen_Vec = [sensorLeftVal, sensorRightVal, sensorVerticalVal]

    behavior(Sen_Vec)