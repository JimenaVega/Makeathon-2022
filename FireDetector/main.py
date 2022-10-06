import pycom
import time
from mqtt import MQTTClient
from pycoproc_1 import Pycoproc
from connections import wifi_connect
import config
from sensors import Sensors
import ujson
import uos

pycom.heartbeat(False)

device_id = wifi_connect()
time.sleep(1)
client = MQTTClient("makeathon", config.MQTT_TAGO_HOST, user=config.MQTT_TAGO_USER, password=config.MQTT_TAGO_PASS, port=config.MQTT_TAGO_PORT)
client.connect()


py = Pycoproc(Pycoproc.PYSENSE)
pySensor = Sensors(py)

try:
    wind_speed = (uos.urandom(1)[0] / 256) * 2 + 10
    air_quality = (uos.urandom(1)[0] / 256) * 3 + 20
    print("Sending data")
    t = pySensor.get_temperature()
    data = [
        {
            "variable": "temperature",
            "value": t
        },
        {
            "variable": "humidity",
            "value": 51
        },
        {
            "variable": "wind_speed",
            "value": wind_speed
        },
        {
            "variable": "air_quality",
            "value": air_quality
        },
        {
            "variable": "location",
            "value": t,
            "location": {
                "lat": -34.88677,
                "lng": -56.1588
            }
        },
    ]
    client.publish(topic="data/{}".format(device_id), msg=ujson.dumps(data))
    while True:
        wind_speed = (uos.urandom(1)[0] / 256) * 2 + 10
        air_quality = (uos.urandom(1)[0] / 256) * 3 + 20
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
                "variable": "wind_speed",
                "value": wind_speed
            },
            {
                "variable": "air_quality",
                "value": air_quality
            },
            {
                "variable": "location",
                "value": t,
                "location": {
                    "lat": -34.88677,
                    "lng": -56.1588
                }
            },
        ]
        client.publish(topic="data/{}".format(device_id), msg=ujson.dumps(data))
        time.sleep(5)
except KeyboardInterrupt:
    client.disconnect()
    print("Disconnected")
