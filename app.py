import garage
import time

print("Checking Sensor")
print("Door is currently: {}".format(garage.check_sensor()))

time.sleep(3)
print("Toggle Doors")
garage.toggle_door()
