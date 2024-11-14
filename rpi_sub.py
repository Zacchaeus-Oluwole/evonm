from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
import json
import time

# Configurations
ENDPOINT = "a3q0luzlp8dot-ats.iot.us-east-1.amazonaws.com"  
CLIENT_ID = "iotconsole-49bb8a89-bff8-4f69-84c9-ba3af977bd9a"
PATH_TO_CERTIFICATE = "device_packages/rpi_device_certificate.crt"
PATH_TO_PRIVATE_KEY = "device_packages/private_key.key"
PATH_TO_AMAZON_ROOT_CA_1 = "device_packages/AmazonRootCA1.pem"  
TOPIC = "device/data"

# Initialize MQTT connection
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERTIFICATE,
    pri_key_filepath=PATH_TO_PRIVATE_KEY,
    ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=60
)

# Callback when a message is received
def on_message_received(topic, payload, **kwargs):
    message = json.loads(payload.decode("utf-8"))
    print("Received message from topic '{}': {}".format(topic, message))

# Connect to AWS IoT
print("Connecting to {} with client ID '{}'...".format(ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a connection result is available
connect_result = connect_future.result()

# 
if connect_result["session_present"] == True :
    print("Connection Status" + ": "+ str(connect_result["session_present"]) + "\nConnected!")

    # Subscribe to the topic
    print("Subscribing to topic '{}'...".format(TOPIC))
    subscribe_future, _ = mqtt_connection.subscribe(
        topic=TOPIC,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received
    )
    subscribe_future.result()
    print("Subscribed!")

    # Keep script running to receive messages
    try:
        print("Listening for messages. Press Ctrl+C to exit.")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Disconnecting...")
    finally:
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")

else:
    print("Connection Status" + ": "+ str(connect_result["session_present"]) + "\nNot connected!....")