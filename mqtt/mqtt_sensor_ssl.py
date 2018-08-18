#!/usr/bin/env python3
import sys
import time
import ssl
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Publishing a message in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("iot/switch/command/AA", 0)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.username_pw_set('switch', '123456')
client.on_connect = on_connect
client.on_message = on_message

### set ssl 
# Case A (not secure): Not to check certificate
#client.tls_set(cert_reqs=ssl.CERT_NONE)

# Case B: Check certificate
sslcontext = ssl.create_default_context()
sslcontext.load_cert_chain('sensor.crt', 'sensor.key')
sslcontext.load_verify_locations('ca.crt')
sslcontext.verify_mode = ssl.CERT_REQUIRED
sslcontext.check_hostname = False
client.tls_set_context(sslcontext)
#client.tls_set('./ca.crt', './sensor.crt', './sensor.key', cert_reqs=ssl.CERT_REQUIRED)



# connect
client.connect("192.168.123.30", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()

times=0
while True:
	client.loop(5)
	times += 1
	print("send status info ", times)
	msg = "switch A online %d"%times
	client.publish("iot/switch/", msg, 0)
	time.sleep(3)	

