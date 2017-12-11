# example triggering relay
import RPi.GPIO as GPIO
import time

relay_pin = 27
sensor_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(sensor_pin, GPIO.IN)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# High = On
# GPIO.output(relay_pin, GPIO.HIGH)
# # Low = Off
# GPIO.output(relay_pin, GPIO.LOW)

# Wired as NC
# # COM -> BCM17, NC -> GROUND
# GPIO.input(sensor_pin)
# # 1 When closed
# GPIO.input(sensor_pin)
# 0 When Opened


def sensor_callback(event):
    print("sensor changed to " + str(GPIO.input(sensor_pin)))
    print(event)


GPIO.add_event_detect(sensor_pin, GPIO.BOTH, callback=sensor_callback)