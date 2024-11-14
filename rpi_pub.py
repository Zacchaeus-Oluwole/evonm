from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

# RANGE, ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, TOPIC and MESSAGE
RANGE = 10

ENDPOINT = "a3q0luzlp8dot-ats.iot.us-east-1.amazonaws.com"  
CLIENT_ID = "iotconsole-49bb8a89-bff8-4f69-84c9-ba3af977bd9a"
PATH_TO_CERTIFICATE = "device_packages/rpi_device_certificate.crt"
PATH_TO_PRIVATE_KEY = "device_packages/private_key.key"
PATH_TO_PUBLIC_KEY = "device_packages/public_key.key"  
PATH_TO_AMAZON_ROOT_CA_1 = "device_packages/AmazonRootCA1.pem"  
TOPIC = "device/data"
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
    keep_alive_secs=30
)
print("Connecting to {} with client ID '{}'...".format(ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a connection result is available
connect_result = connect_future.result()

# 
if connect_result["session_present"] == True :
    print("Connection Status" + ": "+ str(connect_result["session_present"]) + "\nConnected!")
    # Publish message to server desired number of times.
    print('Begin Publish')
    for i in range (RANGE):
        data = "{} [{}]".format(MESSAGE, i+1)
        message = {"message" : data}
        mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
        print("Published: '" + json.dumps(message) + "' to the topic: " + TOPIC)
        t.sleep(0.1)
        print('Publish End')

else:
    print("Connection Status" + ": "+ str(connect_result["session_present"]) + "\nNot connected!....")

disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
