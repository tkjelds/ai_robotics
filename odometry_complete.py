from umath import cos, sin, radians, degrees
from pybricks.tools import wait
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from urandom import randint
from pybricks.tools import StopWatch, wait


left_motor = Motor(Port.F)
right_motor = Motor(Port.E, Direction.COUNTERCLOCKWISE)


# Constants: Robot physical parameters (fixed)
DT = 0.05  # Time step for odometry updates (seconds)
...


# dynamic variables
x, y, theta = 0.0, 0.0, 0.0  # Position (in meters) and orientation (in radians)


def get_wheel_velocities():
    """Get wheel angular velocities in radians per second."""
    # use motor.speed() to return the current angular velocity. Note that it returns values in degree per second
    # you need to change from degree to radian so that you can use it later in calculations safely
    velocities = [0,0]
    velocities[0] = radians(left_motor.speed())
    velocities[1] = radians(right_motor.speed())
    return velocities

def update_odometry():
    """Update the robot's position using kinematic equations."""
    global x, y, theta
    velocities = get_wheel_velocities()
    WHEEL_RADIUS = 28
    x = x + (WHEEL_RADIUS/2)*(velocities[0]+ velocities[1])*cos(theta)*DT
    y = y + (WHEEL_RADIUS/2)*(velocities[0] + velocities[1])*sin(theta)*DT
    theta = theta + (WHEEL_RADIUS/81)*(velocities[1] - velocities[0])*DT
    return x, y, theta


def move_robot(left_speed, right_speed, duration):
    """Move the robot with given wheel speeds for a given duration and do odometry."""
    left_motor.run(left_speed)
    right_motor.run(right_speed)

    for _ in range(int(duration / DT)):
        update_odometry()

        print(x,y,degrees(theta))
        
        wait(int(DT * 1000))  # Convert seconds to milliseconds

    left_motor.stop()
    right_motor.stop()

# Example movement sequence:
# move forward for n sec
FORWARD_SPEED = 150  
move_robot(FORWARD_SPEED,FORWARD_SPEED,2)
#move_robot(500,-500,1)
# turn in place for m sec
# move_robot(...)
# # move forward for k seconds
# move_robot(...)
print("Final Position:", x, y, degrees(theta))