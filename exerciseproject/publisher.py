import paho.mqtt.client as paho
import sys
import time

# Connect to the MQTT broker
client = paho.Client()
if client.connect("localhost", 1883, 60) != 0:  # Assuming MQTT broker is running on localhost
    print("Could not connect to MQTT broker.")
    sys.exit(-1)

# Define a function to send message and time log
def send_message_and_log(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    payload = f"{current_time}: {message}"
    client.publish("robot/delivery", payload, qos=0)

# Example usage:
send_message_and_log("Package delivered at delivery point 1")

# Disconnect from the MQTT broker
client.disconnect()