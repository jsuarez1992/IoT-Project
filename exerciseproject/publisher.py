# MQTT Publisher part

import paho.mqtt.client as paho
import sys

client = paho.Client()

if client.connect("local host", 1886, 60) != 0:
    print("Could not connect to MQTT broker.")
    sys.exit(-1)

client.publish("test/status", "Hello", 0)

client.disconnect