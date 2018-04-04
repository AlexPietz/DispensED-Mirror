#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time

def check_identification(colour):
    print('checking for id colour ' + colour)

    colour_codes = {"black": 1, "blue": 2, "green": 3, "yellow": 4, "red": 5, "white": 6, "brown": 7}
    try:
        colour_code = colour_codes[colour]
    except:
        print('Invalid colour')
        return False

    cl = ev3.ColorSensor(ev3.INPUT_3)
    cl.mode = 'COL-REFLECT'

    start_time = time.time()
    initial = cl.value()

    ev3.Sound.speak("Please insert and hold identification tag").wait()
    #time.sleep(1)

    while time.time() < start_time + 40:
        if cl.value() <= (initial - 3) or cl.value() >= (initial + 3):
            cl.mode = 'COL-COLOR'
            time.sleep(1)
            if (cl.value() == colour_code):
                ev3.Sound.speak("Identification check successful, please remove identification tag").wait()
                time.sleep(5)
                return True

    ev3.Sound.speak("Identification check unsuccessful, moving to next patient").wait()
    time.sleep(5)
    return False
