#!/usr/bin/env python3
import sys
import time
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("iot/#")

# The callback for when a PUBLISH message is received from the server.
info = {'messages':0, 'cmd':0}
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    userdata['messages'] += 1

    if userdata['messages']%5 == 0:
        userdata['cmd'] += 1
        print("send command ", userdata['cmd'])
        client.publish("iot/switch/command/AA", "Command to AA with %d"%userdata['cmd'], 0) 

client = mqtt.Client()
client.username_pw_set('switch-x', '12345678')
client.user_data_set(info)
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.123.30", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
