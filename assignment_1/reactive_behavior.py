from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from urandom import randint
hub = PrimeHub()
sensorRight = ColorSensor(Port.B)
sensorLeft = ColorSensor(Port.A)
sensorMiddle = ColorSensor(Port.D)

rightWheel = Motor(Port.F)
leftWheel = Motor(Port.E, Direction.COUNTERCLOCKWISE)

robot = DriveBase(leftWheel, rightWheel, wheel_diameter=55, axle_track=115)

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

def printDirection(direction):
    if direction == Direction.LEFT:
        print("Left")
    elif direction == Direction.RIGHT:
        print("Right")

class Detection:
    EDGE = 1
    OBSTACLE = 2
    CLEAR = 3

class Direction:
    LEFT = 0
    RIGHT = 2

def opposite(direction):
    if direction == Direction.LEFT:
        return Direction.RIGHT
    elif direction == Direction.RIGHT:
        return Direction.LEFT


def epsilonGreedy(chance = 1):
    return randint(1,100) <= chance 

def exploreTurn(sen_vec, degrees = 90, direction = Direction.RIGHT):
    turned = 0
    while (sen_vec[direction] == Detection.CLEAR and turned < degrees):
        if turned > 10 and sen_vec[opposite(direction)] == Detection.EDGE:
            break
        turn(1,direction)
        sen_vec = getDetectionVec()
        turned += 1

def brakeWheels():
    leftWheel.hold()
    rightWheel.hold()

def turn(degrees, direction):
    if direction == Direction.RIGHT:
        turnRight(degrees)
    elif direction == Direction.LEFT:
        turnLeft(degrees)

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

def normalizeMiddle(value):
    return Detection.OBSTACLE if value > 0 else Detection.CLEAR

def normalizeSides(value):
    return Detection.CLEAR if value > 1 else Detection.EDGE

def getDetectionVec():
    LeftDetection = normalizeSides(sensorLeft.reflection())
    MiddleDetection = normalizeMiddle(sensorMiddle.reflection())
    RightDetection = normalizeSides(sensorRight.reflection())
    return [LeftDetection, MiddleDetection, RightDetection]

def behavior(Detection_vec):
    sense = Detection_vec
    explore = epsilonGreedy()
    if (sense == [Detection.CLEAR, Detection.CLEAR, Detection.CLEAR]):
        robot.straight(20,wait=False)
    elif (sense == [Detection.EDGE, Detection.CLEAR, Detection.CLEAR]):
        if explore:
            exploreTurn(sense,direction=Direction.RIGHT)
        else:   
            turnRight(2)  
    elif (sense == [Detection.CLEAR, Detection.CLEAR, Detection.EDGE]):
        if explore:
            exploreTurn(sense,direction=Direction.LEFT)
        else:
            turnLeft(3)
    elif sense == [Detection.EDGE, Detection.CLEAR, Detection.EDGE]:
        turnLeft(3)
    elif (sense == [Detection.CLEAR, Detection.OBSTACLE, Detection.CLEAR] or
          sense == [Detection.EDGE, Detection.OBSTACLE, Detection.CLEAR]):
        robot.straight(-20)
        turnRight(30)
    elif (sense == [Detection.CLEAR, Detection.OBSTACLE, Detection.EDGE]):
        robot.straight(-20)
        turnLeft(30)

while(True):
    #wait(1000)
    #printSensors(Detection_vec)
    Detection_vec = getDetectionVec()
    behavior(Detection_vec)



