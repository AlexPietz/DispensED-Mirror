#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time

cl = ev3.ColorSensor(ev3.INPUT_2)
cl.mode='COL-REFLECT'
motor=ev3.Motor('outA')

numberPills = int(sys.argv[1]) # number of pills to be dispensed
count_dispensed = 0 # number of pills that have been dispensed so far
forward = True # direction of motor
direction_count = 0 # number of iterations since direction change
dispensing = False # whether dispenser is curently in the process of dispensing
initial = cl.value() # initial value of colour sensor
less = False # represents whether cl.value() decreases (or increases) at start of dispensing
stopfor = 0 # if cl value increases, then we stop checking colour sensor for 10 iterations

motor.run_timed(speed_sp=-450, time_sp=120)

while (count_dispensed < numberPills):
    # reverse direction every 200 iterations
    if (direction_count > 200):
        if (forward):
           motor.run_timed(speed_sp=450, time_sp=120)
        else:
           motor.run_timed(speed_sp=-450, time_sp=120)
        forward = not forward
        direction_count = 0

    if (not dispensing and stopfor == 0):
        # if sensor value changes by +-2 then we have started pill dispensing
        # sensor behaviour after initial change is dependent on pill position
        # so cases of value increase and decrease must be seperated
        if (cl.value() <= (initial-2)):
           dispensing = True
           less = True
        elif (cl.value() >= (initial+2)):
           less = False
           dispensing = True

    elif (stopfor == 0):
        if (less and cl.value() > (initial-2)):
            # if sensor value originally decreased, and value has now increased
            # then dispense is complete
            dispensing = False
            count_dispensed = count_dispensed + 1
            print(str(count_dispensed) + ' pills dispensed')
        elif (not less and cl.value() <= (initial+1) and cl.value() >= (initial-1)):
            # if sensor value originally increased, it may decrease below normal
            # before returning to normal, so stop monitoring sensor value for 10 iterations
            dispensing = False
            count_dispensed = count_dispensed + 1
            print(str(count_dispensed) + ' pills dispensed')
            stopfor = 10

    direction_count = direction_count + 1
    if (stopfor != 0):
        stopfor = stopfor - 1
    time.sleep(0.0005) # increase length of iteration