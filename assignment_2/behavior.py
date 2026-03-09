import planner as pl
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from urandom import randint
from pybricks.tools import StopWatch, wait

state = pl.State([0,0], pl.Directions.NORTH, [[3,1],[0,1]])
route = pl.getActions (state)

hub = PrimeHub()
left_sensor = ColorSensor(Port.B)
right_sensor = ColorSensor(Port.A)
middle_sensor = ColorSensor(Port.C)

left_motor = Motor(Port.F)
right_motor = Motor(Port.E, Direction.COUNTERCLOCKWISE)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55, axle_track=84)

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

def forward(offset):
    detection_vec = getDetectionVec()
    while True:
        if detection_vec == [Detection.NO_LINE, Detection.LINE,Detection.NO_LINE]:
            robot.straight(10)
        elif detection_vec == [Detection.NO_LINE, Detection.NO_LINE,Detection.LINE]:
            robot.turn(3)
        elif detection_vec == [Detection.LINE, Detection.NO_LINE,Detection.NO_LINE]:
            robot.turn(-3)
        elif detection_vec == [Detection.LINE, Detection.LINE,Detection.LINE]:
            break
        elif detection_vec == [Detection.LINE, Detection.NO_LINE,Detection.LINE]:
            break
        elif detection_vec == [Detection.LINE, Detection.LINE,Detection.NO_LINE]:
            break
        elif detection_vec == [Detection.NO_LINE, Detection.LINE,Detection.LINE]:
            break
    robot.straight(offset)

def push():
    print("TBD")

def left():
    print("TBD")
def right():
    print("TBD")


for action in route:
    if action == "FORWARD":
        forward(10)
    elif action == "PUSH":
        forward(-10)
        
    elif action == "LEFT":
        left()
    elif action == "RIGHT":
        right()
    