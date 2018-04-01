#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time

def check_identification(colour):
    colour_codes = {"black": 1, "blue": 2, "green": 3, "yellow": 4, "red": 5, "white": 6, "brown": 7}
    try:
        colour_code = colour_codes[colour]
    except:
        print('Invalid colour')
        return False

    cl = ev3.ColorSensor(ev3.INPUT_3)
    cl.mode = 'COL-COLOR'

    start_time = time.time()

    ev3.Sound.speak("Please scan identification").wait()
    time.sleep(1)

    while time.time() < start_time + 20:
        if (cl.value() == colour_code):
            ev3.Sound.speak("Identification scan successful, please remove identification tag").wait()
            time.sleep(5)
            return True

    return False
