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
    client.subscribe("refilling")

def enter(state):
    global start_time
    if state:
        start_time = time.time()
    else:
        if (time.time() - start_time > 3):
            ev3.Sound.speak("Entered refill mode, please select medications to refill on the software system").wait()
            time.sleep(2)
            client.publish("refilling/out", "refill_start")
            return

def dispense(client, userdata, msg):
    msg_string = msg.payload.decode()
    print(msg_string)
    m_list = msg_string.split(',')

    print('dispensing ' + msg_string)

    # refilling
    if msg.topic == "refilling":
        if m_list[0] == "1":
            refill_indi()
        if m_list[1:] != []:
            # publishes "0" if package refill failure, "1" if success
            client.publish("refilling/out", refill_pack(m_list[1:]))

    # dispensing
    elif msg.topic == "dispensing":
        if not check_identification(m_list[0]):
            client.publish("dispensing/out", "0")
            return
        print(m_list[1:3])
        if m_list[1:3] != ['0','0']:
            if not dispense_number(m_list[1:3]): # List of pills to dispense for each dispenser
                client.publish("dispensing/out", "0")
                return
        if m_list[3] == "None":
            time.sleep(10)
        elif not dispense_package_colour(m_list[3]): # Colour of package to dispense
            client.publish("dispensing/out", "0")
            return
        print("returning sucess")
        for i in range(0, 10):
            client.publish("dispensing/out", "1")
        return

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
