# example triggering relay
import time
import RPi.GPIO as GPIO

# GPIO SETUP
relay_pin = 27
sensor_pin = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(sensor_pin, GPIO.IN)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def check_sensor():
    if GPIO.input(relay_pin):
        return "closed"
    else:
        return "open"


def toggle_door():
    GPIO.output(relay_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(relay_pin, GPIO.LOW)