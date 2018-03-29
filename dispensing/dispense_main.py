#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time
import paho.mqtt.client as mqtt
import dispense_package_colour
import dispense_number
import refill_indi
import refill_pack
import check_identification


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
    input = msg.split(',')
    
    if not check_identification(input[0]):
        client.publish("dispensing", "0")
        return

if not dispense_number(input[1:2]): # List of pills to dispense for each dispenser
        client.publish("dispensing", "0")
        return

    if not dispense_package_colour(input[3]): # Colour of package to dispense
        client.publish("dispensing", "0")
        return

    client.publish("dispensing", "1")


start_time = 0
btn = ev3.Button()
btn.on_enter = enter # on enter button pressed

client = mqtt.Client()
client.connect("192.168.17.130", 1883, 60)
client.on_connect = on_connect
client.on_message = dispense

client.loop_start()

while True:
    btn.process() # Check for currently pressed buttons
