# example triggering relay
import time
import RPi.GPIO as GPIO


# GPIO SETUP
relay_pin = 27
sensor_pin = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, GPIO.LOW) # Set to Off might neet to check and set at boot if failed while open?
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def check_sensor(status):
    if status:
        return "closed"
    else:
        return "open"


print("Testing Setup....")
print("Current State = {} Which is {}".format(GPIO.input(sensor_pin), check_sensor(GPIO.input(sensor_pin))))
print("Triggering Relay")
GPIO.output(relay_pin, GPIO.HIGH)
print("Sleeping 2")
time.sleep(1)
print("Closing relay")
GPIO.output(relay_pin, GPIO.LOW)
