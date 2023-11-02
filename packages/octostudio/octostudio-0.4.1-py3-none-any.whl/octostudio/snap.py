# from codelab_adapter_client import send_message
import random
import paho.mqtt.client as mqtt
from octostudio import OctoStudio

client_id = f'octostudio-{random.randint(0, 100000)}'
mqtt_client = mqtt.Client(client_id)

mqtt_client.connect("broker.emqx.io", 1883)

def on_message(shape):
    mqtt_client.publish("octo_message", shape)

def main():
    print("λ ❤️  🐙")
    octo = OctoStudio()
    octo.on_message = on_message
    octo.start()
