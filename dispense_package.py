#!/usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time

cl = ev3.ColorSensor(ev3.INPUT_2)
cl.mode='COL-COLOR'
motor = ev3.Motor('outD')
colour = sys.argv[1]
colour_codes = {"black":1, "blue":2, "green":3, "yellow":4, "red":5, "white":6, "brown":7}
stop_times = {1:0.1, 2:0.1, 3:0.04, 4:0.1, 5:0.1, 6:0.1, 7:0.2}
skip = False
try:
    colour_code = colour_codes[sys.argv[1]]
except:
    print('Invalid colour')

if (cl.value() == colour_code):
    skip = True

if not skip:
    motor.run_forever(speed_sp=150)

    while (cl.value() != colour_code):
        pass

    time.sleep(stop_times[colour_code])
    motor.stop()

print('found ' + colour)

cl.mode='COL-REFLECT'

time.sleep(1)

initial = cl.value()

while True:
    if cl.value() <= (initial-2) or cl.value() >= (initial+2):
        print('Package taken')
