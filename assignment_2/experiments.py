from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from urandom import randint
from pybricks.tools import StopWatch, wait

hub = PrimeHub()
left_sensor = ColorSensor(Port.B)
right_sensor = ColorSensor(Port.A)
middle_sensor = ColorSensor(Port.C)

left_motor = Motor(Port.F)
right_motor = Motor(Port.E, Direction.COUNTERCLOCKWISE)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55, axle_track=84)

__baseline__ = [4,5,6]

def printSensors(Detection_vec):
    print("Left: ", end="")
    printDetection(Detection_vec[0])
    print("Middle: ", end="")
    printDetection(Detection_vec[1])
    print("Right: ", end="")
    printDetection(Detection_vec[2])

def printDetection(detection):
    if detection == Detection.LINE:
        print("Line")
    else:
        print("No Line")

def turnChance(chance = 50):
    return randint(1,100) <= chance 

class Detection:
    LINE = 1
    NO_LINE = 0
    
class SensorPosition:
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

def normalize(value):
    return Detection.NO_LINE if value != 1  else Detection.LINE

def getDetectionVec():
    LeftDetection = normalize(left_sensor.reflection())
    MiddleDetection = normalize(middle_sensor.reflection())
    RightDetection = normalize(right_sensor.reflection())
    return [LeftDetection, MiddleDetection, RightDetection]

def realign(detection_vec):
    # print("Realign: ", detection_vec)
    turn = turnChance()
    if detection_vec == [Detection.NO_LINE, Detection.NO_LINE,Detection.LINE]:
        robot.turn(90)
        robot.straight(30)
    elif detection_vec == [Detection.LINE, Detection.NO_LINE,Detection.LINE]:
        if turn:
            robot.turn(90)
            robot.straight(30)  
        else:
            robot.turn(-90)
            robot.straight(30)  
    elif detection_vec == [Detection.LINE, Detection.NO_LINE,Detection.NO_LINE]:
        robot.turn(-90)
        robot.straight(30)
    elif detection_vec == [Detection.NO_LINE, Detection.NO_LINE,Detection.NO_LINE]:
        robot.turn(3, wait=False)
        
def explore(detection_vec):
    turn = turnChance()
    if detection_vec == [Detection.NO_LINE, Detection.LINE,Detection.LINE]:
        if turn: 
            robot.turn(90)
            robot.straight(50)
        else:
            robot.straight(100, wait=False)
            
    elif detection_vec == [Detection.LINE, Detection.LINE,Detection.NO_LINE]:
        if turn: 
            robot.turn(-90)
            robot.straight(50)
        else:
            robot.straight(100, wait=False)
    elif detection_vec == [Detection.LINE, Detection.LINE,Detection.LINE]:
        turn = turnChance(66)
        if turn: 
            turn = turnChance()            
            if turn: 
                robot.turn(90)
                robot.straight(50)
            else:
                robot.turn(-90)
                robot.straight(50)
        else:
            robot.straight(100, wait=False)
    elif detection_vec == [Detection.NO_LINE, Detection.LINE,Detection.NO_LINE]:
        robot.straight(100, wait=False)
    


def straight():
    robot.straight(10,wait=False)

# print("Reflection Test")
# print("Time (ms), Left Reflection, Right Reflection")
while True: 
    Detection_vec = getDetectionVec()
    printSensors(Detection_vec)
    if Detection_vec[SensorPosition.MIDDLE] == Detection.NO_LINE:
        print("Realign")
        realign(Detection_vec)
    else :
        print("explore")
        explore(Detection_vec)
    
    # print("left: ",left_sensor.reflection())
    # print("middle: ",middle_sensor.reflection())
    # print("right: ",right_sensor.reflection())
    # wait(500)
