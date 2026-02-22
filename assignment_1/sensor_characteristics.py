from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Port
from pybricks.tools import StopWatch, wait
hub = PrimeHub()
middle_sensor = ColorSensor(Port.D)
right_sensor = ColorSensor(Port.B)

watch = StopWatch()

watch.reset()
print("Right_sensor_value_test")
print("Time (ms), Reflection")
while watch.time() < 10000:  # Run for 10 seconds   
    var = right_sensor.reflection()
    print(watch.time(), ",", var)
 #  dl.log(var)
    wait(500) 