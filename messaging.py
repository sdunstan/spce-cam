import sys
import time
import uuid
import paho.mqtt.client as mqtt

mqtt_client = None


def an_id():
    return str(uuid.uuid4())


def on_mqtt_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print('Connected to mosquito')
    else:
        print(f"Something went wrong connecting to mosquito: {rc}")
        sys.exit(1)


def get_mqtt_client(callback):
    global mqtt_client
    if not mqtt_client:
        mqtt.Client.connected_flag = False
        mqtt_client = mqtt.Client(f"spce-camera-{an_id()}")
        mqtt_client.on_connect=on_mqtt_connect
        mqtt_client.on_message=callback
        mqtt_client.loop()
        mqtt_client.connect("localhost")
        while not mqtt_client.connected_flag:
            print('Connecting to mqtt...')
            mqtt_client.loop()
            time.sleep(0.5)
        mqtt_client.subscribe('shopper/request')
    return mqtt_client

