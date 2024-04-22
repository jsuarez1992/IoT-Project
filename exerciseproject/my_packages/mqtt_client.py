import paho.mqtt.client as mqtt # DON'T USE PAHO ON ROBOT SIDE -> use umqtt. PAHO ON THE COMPUTER SIDE
import time

class MQTTClient:
    def __init__(self, broker_address, client_id):
        self.broker_address = "172.0.0.1" # the address of the MQTT broker
        self.client_id = "Anna" # the ID to identify this MQTT client
        self.client = mqtt.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(self.broker_address)
        self.client.loop_start()  # Start the MQTT client loop

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code " + str(rc))
        # Subscribe to topics upon successful connection
        self.client.subscribe("topic/to/subscribe")

    def on_message(self, client, userdata, msg):
        print("Received message: " + msg.topic + " " + str(msg.payload))
        # Process incoming messages
        if msg.topic == "topic/to/subscribe":
            self.process_message(msg.payload.decode())

    def process_message(self, message):
        # Implement your message processing logic here
        print("Processing message:", message)

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def disconnect(self):
        self.client.loop_stop()  # Stop the MQTT client loop
        self.client.disconnect()

# Example usage
if __name__ == "__main__":
    # Replace 'localhost' with the address of your MQTT broker
    client = MQTTClient("localhost", "ev3_client")
    client.connect()

    try:
        while True:
            # Publish message every 20 seconds
            client.publish("topic/to/publish", "Hello, MQTT!")
            time.sleep(20)
    except KeyboardInterrupt:
        client.disconnect()