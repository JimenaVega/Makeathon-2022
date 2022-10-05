import pycom
import time
from mqtt import MQTTClient
from pycoproc_1 import Pycoproc
from connections import wifi_connect
import config
from sensors import Sensors
import ujson

pycom.heartbeat(False)

device_id = wifi_connect()

client = MQTTClient("makeathon", config.MQTT_TAGO_HOST, user=config.MQTT_TAGO_USER, password=config.MQTT_TAGO_PASS, port=config.MQTT_TAGO_PORT)
# client = MQTTClient("makeathon", config.MQTT_TB_HOST, user=config.MQTT_TB_USER, password=config.MQTT_TB_PASS, port=config.MQTT_TB_PORT)
client.connect()


py = Pycoproc(Pycoproc.PYSENSE)
pySensor = Sensors(py)

try:
    while True:
        print("Sending data")
        t = pySensor.get_temperature()
        data = [
            {
                "variable": "temperature",
                "value": t
            },
            {
                "variable": "humidity",
                "value": pySensor.get_humidity()
            },
            {
                "variable": "pressure",
                "value": pySensor.get_pressure()
            },
            {
                "variable": "location",
                "value": t,
                "location": {
                    "lat": -34.88677,
                    "lng": -57.1588
                }
            },
            {
                "variable": "light",
                "value": pySensor.get_light()[0]
            }
        ]
        client.publish(topic="data/{}".format(device_id), msg=ujson.dumps(data))
        time.sleep(5)
except KeyboardInterrupt:
    client.disconnect()
    print("Disconnected")
