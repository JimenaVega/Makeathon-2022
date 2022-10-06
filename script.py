from os import device_encoding
import paho.mqtt.client as mqtt
import time
import json
from pymongo import MongoClient
import datetime

MQTT_HOST = "mqtt.tago.io"
MQTT_PORT = 1883
MQTT_USER = "Default"
MQTT_PASS = "536ce64e-3e51-4a80-9115-26aefbb25a20"
CLIENT_ID = '1333'

db_client = MongoClient('10.4.100.180', 27017, username='root', password='example')
collection = db_client['FireDetector']['devices']


def get_days_without_rain(device_id):
    global collection
    last_rain = collection.find({'device_id': device_id, 'raining': True}).sort('timestamp', -1).limit(1)
    if len(list(last_rain)) == 0:
        last_rain = collection.find({'device_id': device_id}).sort('timestamp', 1).limit(1)
    now = int(time.time())
    days_without_rain = (now - last_rain[0]['timestamp']) // 86400
    return days_without_rain


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("data/#")


def on_message(client, userdata, msg):
    global collection
    dict_msg = json.loads(msg.payload.decode('utf-8'))
    device_unique_id = msg.topic.split('/')[1]
    humidity = next((x['value'] for x in dict_msg if x['variable'] == 'humidity'), None)
    temperature = next((x['value'] for x in dict_msg if x['variable'] == 'temperature'), None)
    wind_speed = next((x['value'] for x in dict_msg if x['variable'] == 'wind_speed'), None)
    air_quality = next((x['value'] for x in dict_msg if x['variable'] == 'air_quality'), None)
    doc = {
        'device_id': device_unique_id,
        'timestamp': int(time.time()),
        'humidity': humidity,
        'raining': humidity > 50,
        'temperature': temperature,
        'wind_speed': wind_speed,
        'air_quality': air_quality,
    }
    collection.insert_one(doc)
    days_without_rain = get_days_without_rain(device_unique_id)
    if days_without_rain is not None:
        print('Days without rain: {}'.format(days_without_rain))


client = mqtt.Client(CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_forever()
while True:
    time.sleep(10)
