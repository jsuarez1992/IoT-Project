import paho.mqtt.client as paho
import sys

# Define the on_message callback function
def on_message(client, userdata, msg):
    print("Received message:", msg.payload.decode())

# Connect to the MQTT broker
client = paho.Client()
client.on_message = on_message
if client.connect("localhost", 1883, 60) != 0:  # Assuming MQTT broker is running on localhost
    print("Could not connect to MQTT broker.")
    sys.exit(-1)

# Subscribe to the topic where the messages will be published by the robot
client.subscribe("robot/delivery")

try:
    # Enter a loop to continuously listen for messages
    print("Waiting for messages...")
    client.loop_forever()
except KeyboardInterrupt:
    print("Disconnecting from broker...")
    client.disconnect()