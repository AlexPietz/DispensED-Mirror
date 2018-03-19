#!/usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time

cl = ev3.ColorSensor(ev3.INPUT_2)
cl.mode='COL-COLOR'
motor = ev3.Motor('outD')
colour = sys.argv[1]
colour_codes = {"black":1, "blue":2, "green":3, "yellow":7, "red":5, "white":6, "brown":7}
stop_times = {1:0.1, 2:0.12, 3:0.08, 4:0.1, 5:0.1, 6:0.1, 7:0.2}
skip = False
timed_out = False
colour_code = 7

num_packages_to_load = sys.argv[1]
if (num_packages_to_load > 5):
    print('Can\'t load that many packages')
    sys.exit(0)

start_time = time.time()

for n in range(0, int(num_packages_to_load)):
    print ('Package to load: ' + str(n+1))

    find_slot

    cl.mode='COL-REFLECT'

    time.sleep(1)

    initial = cl.value()

    while True:
        if cl.value() <= (initial-2) or cl.value() >= (initial+2):
            print('Hand detected')
            break

    cl.mode='COL-COLOR'
    # check package has been placed in
    print('Waiting for package to be placed in')
    while True:
        #if (cl.value in package_colour_codes):
        if (cl.value != colour_code):
            print('Package placed in')
            time.sleep(2)
            break
exit()

def find_slot:
    if (cl.value() == colour_code):
        skip = True
        
        if not skip:
            motor.run_forever(speed_sp=150)
            
            while ((cl.value() != colour_code) and (not timed_out)):
                if ((time.time() - start_time) > (10.0 * int(num_packages_to_load))):
                    timed_out = True
                    motor.stop()
                pass
            
            time.sleep(stop_times[colour_code])
            motor.stop()
        
        if (timed_out):
            print('Timed out. No free slots found.')
            sys.exit(0)
        else:
            print('found free slot')

    if cl.value() != colour_code:
        find_slot

