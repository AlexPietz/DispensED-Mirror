#!/usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time

def dispense_package_colour(colour):

    if colour == "None":
        return True

    cl = ev3.ColorSensor(ev3.INPUT_2)
    cl.mode = 'COL-COLOR'
    motor = ev3.Motor('outC')
    colour_codes = {"black": 1, "blue": 2, "green": 3, "yellow": 4, "red": 5, "white": 6, "brown": 7}
    stop_times = {1: 0.1, 2: 0.12, 3: 0.1, 4: 0.1, 5: 0.1, 6: 0.1, 7: 0.2}
    skip = False
    timed_out = False
    try:
        colour_code = colour_codes[colour]
    except:
        print('Invalid colour')
        return False

    start_time = time.time()

    if cl.value() == colour_code:
        skip = True

    if not skip:
        motor.run_forever(speed_sp=150)

        while (cl.value() != colour_code) and (not timed_out):
            if (time.time() - start_time) > 6.0:
                # if timed out go to brown segment
                while (cl.value() != 7):
                    pass
                print('Timed out')
                time.sleep(stop_times[7])
                motor.stop()
                return False

        time.sleep(stop_times[colour_code])
        motor.stop()

    print('found ' + colour)

    cl.mode = 'COL-REFLECT'

    ev3.Sound.speak("Package now ready for collection").wait()

    time.sleep(1)

    initial = cl.value()

    start_time = time.time()

    while True:
        if cl.value() <= (initial - 2) or cl.value() >= (initial + 2):
            print('Package taken')
            time.sleep(5)
            return True
        if time.time() > start_time + 30:
            return False
