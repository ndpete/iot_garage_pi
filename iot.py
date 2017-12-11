# iot example
import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

with open("/home/pi/.garage_config.json") as f:
    config = json.load(f)


def echo(payload, responseStatus, token):
    print(payload)


# For certificate based connection
myShadowClient = AWSIoTMQTTShadowClient("rpi-iot")
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
# Configurations
# For TLS mutual authentication
myShadowClient.configureEndpoint(
    config['endpoint'], 8883)
# For Websocket
# myShadowClient.configureEndpoint("YOUR.ENDPOINT", 443)
myShadowClient.configureCredentials(config['root_ca'], config['private_key'], config['certificate'])
# For Websocket, we only need to configure the root CA
# myShadowClient.configureCredentials("YOUR/ROOT/CA/PATH")
myShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

myShadowClient.connect()
# Create a device shadow instance using persistent subscription
myDeviceShadow = myShadowClient.createShadowHandlerWithName("NateRaspberryPi", True)
# Shadow operations
myDeviceShadow.shadowRegisterDeltaCallback(echo)
# myDeviceShadow.shadowUpdate(myJSONPayload, customCallback, 5)
# myDeviceShadow.shadowDelete(customCallback, 5)
# myDeviceShadow.shadowRegisterDeltaCallback(customCallback)
# myDeviceShadow.shadowUnregisterDeltaCallback()
# iot example

while True:
    time.sleep(1)
