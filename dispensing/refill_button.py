#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time
import paho.mqtt.client as mqtt
import dispense_package_colour
import dispense_number
import refill_indi
import refill_pack

btn = ev3.Button()

start_time = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with code: " + str(rc))
    client.subscribe("dispensing")

def enter(state):
    global start_time
    if state:
        start_time = time.time()
    else:
        if (time.time() - start_time > 3):
            client.publish("dispensing", refill_indi)
        else:
            #Tell pi to find out how many need to be refilled
            client.publish("dispensing", refill_pack(2))

def dispense(client, userdata, msg):
    msg = msg.payload.decode()

    if msg[0] == 0:
        client.publish("dispensing", dispense_package_colour(msg[1]))
    else:
        client.publish("dispensing", dispense_number([msg[1], msg[2]]))

btn.on_enter = enter

# This loop checks buttons state continuously,
# calls appropriate event handlers
btn.process() # Check for currently pressed buttons.
# If the new state differs from the old state,
# call the appropriate button event handlers.
time.sleep(0.01)  # buttons state will be checked every 0.01 second

client = mqtt.Client()
client.connect("192.168.17.130", 1883, 60)

client.on_connect = on_connect
client.on_message = dispense

client.loop_forever()
