# MQTT Subscriber part

import paho.mqtt.client as paho
import sys

def onMessage(client, userdata, msg):
    print(msg.topic + ": " +msg.payload.decode())
    
client = paho.Client()
client.on_message = onMessage

if client.connect("local host", 1886, 60) != 0:
    print("Could not connect to MQTT broker.")
    sys.exit(-1)

client.subscribe("test/status")

try:
    print("Press CTRL+C to exit...")
    client.loop_forever()
except:
    print("Disconnecting from broker...")

client.disconnect