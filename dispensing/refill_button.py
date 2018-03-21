#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time
import os

btn = ev3.Button()

start_time = 0

def enter(state):
    global start_time
    if state:
        start_time = time.time()
    else:
        if (time.time() - start_time > 3):
            print('individual dispenser refill')
            os.system('python3 refill_individual.py')
        else:
            print('package dispenser refill')
            os.system('python3 refill_package.py')

btn.on_enter = enter

while True:
    # This loop checks buttons state continuously,
    # calls appropriate event handlers
    btn.process() # Check for currently pressed buttons.
    # If the new state differs from the old state,
    # call the appropriate button event handlers.
    time.sleep(0.01)  # buttons state will be checked every 0.01 second
