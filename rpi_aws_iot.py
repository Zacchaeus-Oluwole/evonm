import sys
import time
from awscrt import mqtt
from awsiot import mqtt_connection_builder


ENDPOINT = "a33ngcpde4nm4d-ats.iot.eu-north-1.amazonaws.com"  
CLIENT_ID = "iotconsole-b218bdd8-a9b8-45c7-b9d0-28d6ad3206f8"
PATH_TO_CERTIFICATE = "connect_device_package/raspberry_thing.cert.pem"
PATH_TO_PRIVATE_KEY = "connect_device_package/raspberry_thing.private.key"
PATH_TO_PUBLIC_KEY = "connect_device_package/raspberry_thing.public.key"  
PATH_TO_AMAZON_ROOT_CA_1 = "connect_device_package/AmazonRootCA1.pem"  
TOPIC = "raspberry/pi/message"
MESSAGE = "Hello from Evon Medics Raspberry Pi!"

def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted:", error)

def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. Return code:", return_code, "Session present:", session_present)


mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERTIFICATE,
    pri_key_filepath=PATH_TO_PRIVATE_KEY,
    client_bootstrap=None,
    ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=6,
    on_connection_interrupted=on_connection_interrupted,
    on_connection_resumed=on_connection_resumed
)


print("Connecting to AWS IoT endpoint...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")


print("Publishing message to topic '{}': {}".format(TOPIC, MESSAGE))
publish_future = mqtt_connection.publish(
    topic=TOPIC,
    payload=MESSAGE,
    qos=mqtt.QoS.AT_LEAST_ONCE
)
publish_future.result()
print("Message published successfully!")


time.sleep(2)
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print("Disconnected from AWS IoT!")
