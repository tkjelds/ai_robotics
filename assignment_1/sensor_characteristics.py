from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Port
from pybricks.tools import StopWatch, wait
hub = PrimeHub()
light_sensor = ColorSensor(Port.D)

watch = StopWatch()

watch.reset()
print("Time (ms), Reflection")
while watch.time() < 10000:  # Run for 10 seconds   
    var = light_sensor.reflection()
    print(watch.time(), ",", var)
 #  dl.log(var)
    wait(500) 