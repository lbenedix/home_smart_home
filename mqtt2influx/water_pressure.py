import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

INFLUXDB_HOST = '<HOSTNAME>'
INFLUXDB_PORT = 8086
INFLUXDB_USER = '<USERNAME>'
INFLUXDB_PASSWORD = '<PASSWORD>'
INFLUXDB_DATABASE = '<DB>'

MQTT_HOST = '<HOSTNAME>'
MQTT_PORT = 1883
MQTT_USER = '<USERNAME>'
MQTT_PASSWORD = '<PASSWORD>'


def on_connect(client, _userdata, _flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/kitchen/pressure")


def on_message(_client, _userdata, msg):
    influx_item = {
        'measurement': 'water_pressure',
        'tags': {},
        'fields': {
            'sensor': 'kitchen_sink',
            'value': float(msg.payload.decode('utf-8'))
        }
    }

    influxdb_client.write_points([influx_item])


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
