import garage
import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

with open("/home/pi/.garage_config.json") as f:
    config = json.load(f)


def delta_callback(payload, responseStatus, token):
    payload = json.loads(payload)
    desired_state = payload['state']['state']
    current_state = garage.check_sensor()
    if current_state != desired_state:
        print("Changing door state to: {}".format(desired_state))
        garage.toggle_door()
        # wait some time
        time.sleep(3)
        update_garage_state(shadow)
    else:
        print("Already at desired state")
        update_garage_state(shadow)


def update_garage_state(deviceShadow):
    newPayload = {'state': {'reported': garage.check_sensor()}}
    deviceShadow.shadowUpdate(json.dumps(newPayload), None, 5)


myShadowClient = AWSIoTMQTTShadowClient("rpi-iot")
myShadowClient.configureEndpoint(config['endpoint'], 8883)
myShadowClient.configureCredentials(config['root_ca'], config['private_key'], config['certificate'])
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()
shadow = myShadowClient.createShadowHandlerWithName("shadow-garage", True)
update_garage_state(shadow)
shadow.shadowRegisterDeltaCallback(delta_callback)


while True:
    time.sleep(1)
