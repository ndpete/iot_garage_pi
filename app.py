import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import RPi.GPIO as GPIO


with open("/home/pi/.garage_config.json") as f:
    config = json.load(f)

# GPIO SETUP
relay_pin = 27
sensor_pin = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(sensor_pin, GPIO.IN)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def sensor_callback(pin):
    time.sleep(1)
    update_garage_state(shadow)


def check_sensor():
    if GPIO.input(sensor_pin):
        return "closed"
    else:
        return "open"


def toggle_door():
    GPIO.output(relay_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(relay_pin, GPIO.LOW)


def delta_callback(payload, responseStatus, token):
    print(payload)
    payload = json.loads(payload)
    desired_state = payload['state']['state']
    print(desired_state)
    current_state = check_sensor()
    print(current_state)
    if current_state != desired_state:
        print("Changing door state to: {}".format(desired_state))
        toggle_door()
        # wait some time
        time.sleep(3)
        update_garage_state(shadow)
    else:
        print("Already at desired state")
        update_garage_state(shadow)


def update_garage_state(deviceShadow):
    newPayload = {'state': {'reported': {'state': check_sensor()}}}
    print(json.dumps(newPayload))
    deviceShadow.shadowUpdate(json.dumps(newPayload), None, 5)
    print("Sent")


# IOT Setup
myShadowClient = AWSIoTMQTTShadowClient("rpi-iot")
myShadowClient.configureEndpoint(config['endpoint'], 8883)
myShadowClient.configureCredentials(config['root_ca'], config['private_key'], config['certificate'])
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()
shadow = myShadowClient.createShadowHandlerWithName("shadow-garage", True)

# Update initial state
print("setting current state")
update_garage_state(shadow)

# wait for events
shadow.shadowRegisterDeltaCallback(delta_callback)
GPIO.add_event_detect(sensor_pin, GPIO.BOTH, callback=sensor_callback)


while True:
    time.sleep(1)
