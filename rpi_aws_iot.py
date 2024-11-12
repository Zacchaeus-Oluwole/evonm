from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

#RANGE, ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, TOPIC and MESSAGE
RANGE = 20

ENDPOINT = "a33ngcpde4nm4d-ats.iot.us-east-1.amazonaws.com"  
CLIENT_ID = "basicPubSub"
PATH_TO_CERTIFICATE = "connect_device_package/rpithing.cert.pem"
PATH_TO_PRIVATE_KEY = "connect_device_package/rpithing.private.key"
PATH_TO_PUBLIC_KEY = "connect_device_package/rpithing.public.key"  
PATH_TO_AMAZON_ROOT_CA_1 = "connect_device_package/AmazonRootCA1.pem"  
TOPIC = "sdk/test/python"
MESSAGE = "Hello from Evon Medics Raspberry Pi!"

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
# Publish message to server desired number of times.
print('Begin Publish')
for i in range (RANGE):
    data = "{} [{}]".format(MESSAGE, i+1)
    message = {"message" : data}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + TOPIC)
    t.sleep(0.1)
print('Publish End')
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()