#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time
import paho.mqtt.client as mqtt
from dispense_package import *
from dispense_individual import *
from refill_individual import *
from refill_package import *
from check_id import *


def on_connect(client, userdata, flags, rc):
    print("Connected with code: " + str(rc))
    client.subscribe("dispensing")

def enter(state):
    global start_time
    if state:
        start_time = time.time()
    else:
        if (time.time() - start_time > 3):
            client.publish("dispensing/out", "refill_start")
            return

def dispense(client, userdata, msg):
    msg = msg.payload.decode()
    m_list = msg.split(',')

    # refilling
    if m_list[0] == "refill_counts":
        if m_list[1] == "1":
            refill_indi()
        if m_list[2:] != []:
            # publishes "0" if package refill failure, otherwise list of added colours
            client.publish("dispensing/out", refill_pack(m_list[2:]))

    # dispensing
    if m_list[0] == "dispense":
        if not check_identification(m_list[1]):
            client.publish("dispensing/out", "0")
            return

        if not dispense_number(m_list[2:4]): # List of pills to dispense for each dispenser
            client.publish("dispensing/out", "0")
            return

        if not dispense_package_colour(m_list[4]): # Colour of package to dispense
            client.publish("dispensing/out", "0")
            return

        client.publish("dispensing/out", "1")


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
