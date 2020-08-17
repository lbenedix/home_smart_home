from datetime import datetime
import math

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json

from paho.mqtt.client import Client

INFLUXDB_HOST = '<HOSTNAME>'
INFLUXDB_PORT = 8086
INFLUXDB_USER = '<USERNAME>'
INFLUXDB_PASSWORD = '<PASSWORD>'
INFLUXDB_DATABASE = '<DB>'

MQTT_HOST = '<HOSTNAME>'
MQTT_PORT = 1883
MQTT_USER = '<USERNAME>'
MQTT_PASSWORD = '<PASSWORD>'


def get_dew_point_c(t_air_c, rel_humidity):
    """Compute the dew point in degrees Celsius
       :param t_air_c: current ambient temperature in degrees Celsius
       :type t_air_c: float
       :param rel_humidity: relative humidity in %
       :type rel_humidity: float
       :return: the dew point in degrees Celsius
       :rtype: float
    """
    A = 17.27
    B = 237.7
    alpha = ((A * t_air_c) / (B + t_air_c)) + math.log(rel_humidity/100.0)
    dew_point = round((B * alpha) / (A - alpha), 2)
    return dew_point


# The callback for when the client receives a CONNACK response from the server.
# 0     Connection accepted
# 1     Connection refused, unacceptable protocol version
# 2     Connection refused, identifier rejected
# 3     Connection refused, server unavailable
# 4     Connection refused, bad user name or password
# 5     Connection refused, not authorized
def on_connect(client, _userdata, _flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp/#")


influx_item = {'measurement': 'bm280', 'tags': {}, 'fields': {'temperature': None, 'humidity': None, 'pressure': None}}
influx_items = {}

def on_message(_client, _userdata, msg):
    if 'bm280' in msg.topic:
        sensor = msg.topic.split('/')[1]
        if sensor not in influx_items:
            influx_items[sensor] = influx_item
        data = msg.payload.decode('utf-8')
        if 'temperature' in msg.topic:
            influx_items[sensor]['fields']['temperature'] = float(data)
        elif 'humidity' in msg.topic:
            influx_items[sensor]['fields']['humidity'] = float(data)
        elif 'pressure' in msg.topic:
            influx_items[sensor]['fields']['pressure'] = float(data)
            influx_items[sensor]['fields']['sensor'] = sensor
            print(datetime.now(), influx_items[sensor])
            influxdb_client.write_points([influx_items[sensor]])


influxdb_client = InfluxDBClient(INFLUXDB_HOST,
                                 INFLUXDB_PORT,
                                 INFLUXDB_USER,
                                 INFLUXDB_PASSWORD,
                                 None)

if __name__ == '__main__':
    # setup influx client
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

    # setup MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.username_pw_set(MQTT_USER, password=MQTT_PASSWORD)
    mqtt_client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)

    # loop loop
    mqtt_client.loop_forever()