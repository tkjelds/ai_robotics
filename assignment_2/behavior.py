#import planner as pl
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from urandom import randint
from pybricks.tools import StopWatch, wait

#state = pl.State([0,0], pl.Directions.NORTH, [[3,1],[0,1]])
#initialNode = pl.Node(pl.State([0,0], pl.Directions.NORTH, [[1,2],[2,2]]), None, None)
# route = pl.getActions (initialNode)
#route = ['RIGHT', 'FORWARD', 'LEFT', 'PUSH_VERTICAL', 'PUSH_VERTICAL', 'RIGHT', 'FORWARD', 'LEFT', 'FORWARD', 'LEFT', 'PUSH_HORIZONTAL', 'LEFT', 'FORWARD', 'FORWARD', 'FORWARD', 'LEFT', 'FORWARD', 'FORWARD', 'LEFT', 'PUSH_VERTICAL', 'PUSH_VERTICAL', 'LEFT', 'FORWARD', 'LEFT', 'PUSH_VERTICAL']

route = ["RIGHT","RIGHT","RIGHT"]
# route = ["RIGHT","RIGHT","RIGHT","RIGHT"]
hub = PrimeHub()
left_sensor = ColorSensor(Port.A)
right_sensor = ColorSensor(Port.B)
middle_sensor = ColorSensor(Port.C)

left_motor = Motor(Port.F)
right_motor = Motor(Port.E, Direction.COUNTERCLOCKWISE)
robot = DriveBase(left_motor, right_motor, wheel_diameter=55, axle_track=84)
robot.settings(500,1000,500,1500) #settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)¶

class Detection:
    LINE = 1
    NO_LINE = 0
class SensorPosition:
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


ColorValues = [1,2,3]
def normalize(value):
    return Detection.NO_LINE if value > 4 else Detection.LINE

def normalizeSide(value):
    return Detection.NO_LINE if value > 4 else Detection.LINE

def getDetectionVec():
    LeftDetection = normalizeSide(left_sensor.reflection())
    MiddleDetection = normalize(middle_sensor.reflection())
    RightDetection = normalizeSide(right_sensor.reflection())
    return [LeftDetection, MiddleDetection, RightDetection]

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


def forward(offset = 0, backwards = False):
    direction = 1
    if backwards: direction = -1
    detection_vec = getDetectionVec()
    godBool = False
    while True:
        detection_vec = getDetectionVec()
        if detection_vec == [Detection.NO_LINE, Detection.LINE,Detection.NO_LINE]:
            robot.straight(10 * direction, wait=False)
        elif detection_vec == [Detection.NO_LINE, Detection.NO_LINE,Detection.LINE]:
            print("Turning left")
            robot.brake()
            robot.turn(-15 * direction)
            robot.straight(10,wait=False),
        elif detection_vec == [Detection.LINE, Detection.NO_LINE,Detection.NO_LINE]:
            print("Turning right")
            robot.brake()
            robot.turn(15)
            robot.straight(10, wait=False)
        elif detection_vec == [Detection.NO_LINE, Detection.NO_LINE,Detection.NO_LINE]:
            print("Lost line", end="")
            robot.brake()
            if godBool:
                robot.turn(3 * direction)
                godBool = False
            else:
                robot.turn(6 * direction)
                godBool = True
        elif detection_vec == [Detection.LINE, Detection.LINE,Detection.LINE]:
            break
        elif detection_vec == [Detection.LINE, Detection.NO_LINE,Detection.LINE]:
            break
        elif detection_vec == [Detection.LINE, Detection.LINE,Detection.NO_LINE]:
            break
        elif detection_vec == [Detection.NO_LINE, Detection.LINE,Detection.LINE]:
            break
    #printSensors(detection_vec)
    robot.straight(offset)

def push(vertical = False):
    
    forward(100)
    forward(-120)
    if not vertical:
        robot.turn(170)
        forward(100)
        robot.turn(170)
    # forward(100)
    # forward(-100)
    # forward(40, backwards=True)


    

def left():
    print("TBD")
    
def right():
    print("TBD")


reflectionCalibation = False
if reflectionCalibation:
    while(True):
        print("right: ", end="")
        print(right_sensor.reflection())
        # print("left: ", end="")
        # print(left_sensor.reflection())
        # print("middle: ", end="")
        # print(middle_sensor.reflection())
        wait(1000)
else: 
    for action in route:
        print(action)
        if action == "FORWARD":
            print("FORWARD")
            forward(80)
        elif action == "PUSH_HORIZONTAL":
            print("PUSH_HORIZONTAL")
            push()
        elif action == "PUSH_VERTICAL":
            print("PUSH_VERTICAL")
            push(vertical=True)
        elif action == "LEFT":
            print("LEFT")
            robot.turn(90)
        elif action == "RIGHT":
            print("RIGHT")
            robot.turn(-90)


    