from os import device_encoding
import paho.mqtt.client as mqtt
import time
import json
from pymongo import MongoClient
import datetime
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MQTT_HOST = "mqtt.tago.io"
MQTT_PORT = 1883
MQTT_USER = "Default"
MQTT_PASS = "06ae8dda-dce6-4a06-b0aa-d57c79e9df92"
CLIENT_ID = '1333'
EMAIL_TO = "example@gmail.com"
EMAIL_FROM = 'fire.detector.pycom@gmail.com'
EMAIL_PW = 'tnzdkbsqeiwgmuep'
EMAIL_SUBJECT = "FIRE ALERT"

db_client = MongoClient('10.4.100.180', 27017, username='root', password='example')
collection = db_client['FireDetector']['devices']
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(EMAIL_FROM, EMAIL_PW)
last_email_sent = None


def get_days_without_rain(device_id):
    global collection
    last_rain = list(collection.find({'device_id': device_id, 'raining': True}).sort('timestamp', -1).limit(1))
    if len(last_rain) == 0:
        last_rain = list(collection.find({'device_id': device_id}).sort('timestamp', 1).limit(1))
    now = int(time.time())
    days_without_rain = (now - last_rain[0]['timestamp']) // 86400
    return days_without_rain


def decide_risk(temperature, humidity, air_quality, wind_speed, days_without_rain):
    temp_risk = 1 if temperature > 30 else 0
    hum_risk = 1 if humidity < 30 else 0
    wind_risk = 1 if wind_speed > 30 else 0
    days_risk = 1 if days_without_rain > 30 else 0

    risk = temp_risk + hum_risk + wind_risk + days_risk

    if(air_quality > 250):
        return 2
    if(risk < 3):
        return 0
    elif(risk >= 3):
        return 1


def send_email():
    global last_email_sent
    print('fire detected')
    if last_email_sent is not None and (datetime.datetime.now() - last_email_sent).total_seconds() < 10800:
        return
    msg = MIMEMultipart('alternative')
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    with open('fireAlert.html', 'r') as f:
        BODY = MIMEText(f.read(), 'html')
        msg.attach(BODY)
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        print('email sent')
    last_email_sent = datetime.datetime.now()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("data/#")


def on_message(client, userdata, msg):
    global collection
    dict_msg = json.loads(msg.payload.decode('utf-8'))
    device_unique_id = msg.topic.split('/')[1]
    humidity = next((x['value'] for x in dict_msg if x['variable'].startswith('humidity')), None)
    temperature = next((x['value'] for x in dict_msg if x['variable'].startswith('temperature')), None)
    wind_speed = next((x['value'] for x in dict_msg if x['variable'].startswith('wind_speed')), None)
    air_quality = next((x['value'] for x in dict_msg if x['variable'].startswith('air_quality')), None)
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
    print(doc)
    days_without_rain = get_days_without_rain(device_unique_id)
    risk = decide_risk(temperature, humidity, air_quality, wind_speed, days_without_rain)
    if risk > 0:
        send_email()


client = mqtt.Client(CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_forever()
while True:
    time.sleep(10)
