#!/usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time

cl = ev3.ColorSensor(ev3.INPUT_2)
cl.mode = 'COL-COLOR'
motor = ev3.Motor('outC')
colour_codes = {"black": 1, "blue": 2, "green": 3, "yellow": 4, "red": 5, "white": 6, "brown": 7}
colour_code = 1
attempts_count = 0  # no. of attempts at finding empty slot

start_time = time.time()

ev3.Sound.speak('Entering package refill mode, please wait').wait()

time.sleep(2)

def attempt():
    skip = False
    timed_out = False
    if cl.value() == colour_code:
        skip = True

    if not skip:
        motor.run_forever(speed_sp=150)

    while cl.value() != colour_code:
        if time.time() - start_time > 10:
            print('Timed out. No free slots found.')
            motor.stop()
            exit()

    print('found potential free slot...double checking...')
    time.sleep(0.2)
    motor.stop()

while True:
    if attempts_count > 10:
        motor.stop()
        raise Exception('Cannot find empty slot!')
    if (cl.value() != colour_code):
        print(attempts_count)
        attempt()
        attempts_count += 1
       # if (cl.value == colour_code):
	#    break
    else:
        break

ev3.Sound.speak('Please place package into dispenser now').wait()

cl.mode = 'COL-REFLECT'

time.sleep(1)

initial = cl.value()

start_time = time.time()

while time.time() - start_time < 5:
    if cl.value() <= (initial - 2) or cl.value() >= (initial + 2):
        print('Hand detected')
        break

cl.mode = 'COL-COLOR'

time.sleep(2)
# check package has been placed in

start_time = time.time()
placed = False

while time.time() - start_time < 5:
    if (cl.value() in colour_codes.values()):
        if cl.value() != colour_code:
            placed = True
            break

if placed:
    colour = list(colour_codes.keys())[list(colour_codes.values()).index(cl.value())]
    print(colour)
else:
    raise Exception('Nothing placed!')

while True:
    if attempts_count > 10:
        motor.stop()
        raise Exception('Cannot find empty slot!')
    if (cl.value() != colour_code):
        print(attempts_count)
        attempt()
        attempts_count += 1
    else:
        break
ev3.Sound.volume =100
ev3.Sound.speak('Hello, refilling was sucessful, you added a ' + colour + ' package, good job').wait()
