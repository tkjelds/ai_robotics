from umath import cos, sin, radians, degrees
from pybricks.tools import wait
...


# Constants: Robot physical parameters (fixed)
DT = 0.1  # Time step for odometry updates (seconds)
...


# dynamic variables
x, y, theta = 0.0, 0.0, 0.0  # Position (in meters) and orientation (in radians)


def get_wheel_velocities():
    """Get wheel angular velocities in radians per second."""
    left_motor_degree_per_sec = left_motor.speed() 
    right_motor_degree_per_sec = right_motor.speed()  
    
    left_motor_radian_per_sec = radians(left_motor_degree_per_sec) 
    right_motor_radian_per_sec = radians(right_motor_degree_per_sec)  
    
    return left_motor_radian_per_sec, right_motor_radian_per_sec
    # use motor.speed() to return the current angular velocity. Note that it returns values in degree per second
    # you need to change from degree to radian so that you can use it later in calculations safely
    ...

def update_odometry():
    """Update the robot's position using kinematic equations."""
    global x, y, theta
    
    left_w, right_w = get_wheel_velocities()



def move_robot(left_speed, right_speed, duration):
    """Move the robot with given wheel speeds for a given duration and do odometry."""
    left_motor.run(left_speed)
    right_motor.run(right_speed)

    for _ in range(int(duration / DT)):
        update_odometry()
        # print of you want:
        # print(x,y,degrees(theta))
        wait(int(DT * 1000))  # Convert seconds to milliseconds

    left_motor.stop()
    right_motor.stop()


# Example movement sequence:
# move forward for n sec
move_robot(...)
# turn in place for m sec
move_robot(...)
# move forward for k seconds
move_robot(...)
print("Final Position:", x, y, degrees(theta))