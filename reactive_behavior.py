from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()
sensorRight = ColorSensor(Port.B)
sensorLeft = ColorSensor(Port.A)
sensorMiddle = ColorSensor(Port.D)

rightWheel = Motor(Port.F)
leftWheel = Motor(Port.E, Direction.COUNTERCLOCKWISE)

robot = DriveBase(leftWheel, rightWheel, wheel_diameter=55, axle_track=115)

class Detection:
    EDGE = 1
    OBSTACLE = 2
    CLEAR = 3

def printSensors(Detection_vec):
    print("Left: ", end="")
    printDetection(Detection_vec[0])
    print("Middle: ", end="")
    printDetection(Detection_vec[1])
    print("Right: ", end="")
    printDetection(Detection_vec[2])

def printDetection(detection):
    if detection == Detection.EDGE:
        print("Edge")
    elif detection == Detection.OBSTACLE:
        print("Obstacle")
    elif detection == Detection.CLEAR:
        print("Clear")

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


robot.settings(500,1000,500,500)

Detection_vec = [Detection.CLEAR,Detection.CLEAR,Detection.CLEAR]

def normalizeMiddle(x):
    return Detection.OBSTACLE if x > 0 else Detection.CLEAR

def normalizeSides(x):
    return Detection.CLEAR if x > 1 else Detection.EDGE

def behavior(Detection_vec):
    # Vec = [Left, Middle, Right]
    sense = Detection_vec
    if (sense == [Detection.CLEAR, Detection.CLEAR, Detection.CLEAR]):
        robot.straight(20,wait=False)
    elif (sense == [Detection.EDGE, Detection.CLEAR, Detection.CLEAR]):
        turnRight(2)  
    elif (sense == [Detection.CLEAR, Detection.CLEAR, Detection.EDGE] or
          sense == [Detection.EDGE, Detection.CLEAR, Detection.EDGE]):
        turnLeft(3)
    elif (sense == [Detection.CLEAR, Detection.OBSTACLE, Detection.CLEAR] or
          sense == [Detection.EDGE, Detection.OBSTACLE, Detection.CLEAR]):
        robot.straight(-20)
        turnRight(15)
    elif (sense == [Detection.CLEAR, Detection.OBSTACLE, Detection.EDGE]):
        robot.straight(-20)
        turnLeft(15)

while(True):
    LeftDetection = normalizeSides(sensorLeft.reflection())
    MiddleDetection = normalizeMiddle(sensorMiddle.reflection())
    RightDetection = normalizeSides(sensorRight.reflection())


    #wait(1000)
    Detection_vec = [LeftDetection, MiddleDetection, RightDetection]
    printSensors(Detection_vec)
    behavior(Detection_vec)



