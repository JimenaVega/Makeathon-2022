import pycom
import time
from mqtt import MQTTClient
from pycoproc_1 import Pycoproc
from connections import wifi_connect
import config
from sensors import Sensors
import ujson
import uos
import _thread

WIND_SPEED_OFFSET = 10
AIR_QUALITY_OFFSET = 20


def send_data():
    global client, device_id
    while True:
        wind_speed = (uos.urandom(1)[0] / 256) * 2 + WIND_SPEED_OFFSET
        air_quality = (uos.urandom(1)[0] / 256) * 3 + AIR_QUALITY_OFFSET
        print("Sending data")
        data = [
            {
                "variable": "temperature{}".format(device_id),
                "value": pySensor.get_temperature()
            },
            {
                "variable": "humidity{}".format(device_id),
                "value": pySensor.get_humidity()
            },
            {
                "variable": "wind_speed{}".format(device_id),
                "value": wind_speed
            },
            {
                "variable": "air_quality{}".format(device_id),
                "value": air_quality
            },
            {
                "variable": "location{}".format(device_id),
                "value": air_quality,
                "location": {
                    "lat": -34.891900,
                    "lng": -56.178802
                },
            },
        ]
        client.publish(topic="data/{}".format(device_id), msg=ujson.dumps(data), qos=1)
        time.sleep(60)


pycom.heartbeat(False)

device_id = wifi_connect()
time.sleep(1)
client = MQTTClient("makeathon", config.MQTT_TAGO_HOST, user=config.MQTT_TAGO_USER, password=config.MQTT_TAGO_PASS, port=config.MQTT_TAGO_PORT)
client.connect()


py = Pycoproc(Pycoproc.PYSENSE)
pySensor = Sensors(py)

_thread.start_new_thread(send_data, ())
