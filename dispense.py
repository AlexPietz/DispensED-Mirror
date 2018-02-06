#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time

cl = ev3.ColorSensor(ev3.INPUT_2)
motor=ev3.Motor('outA')

cl.mode='COL-REFLECT'

numberPills = int(sys.argv[1])
count_dispensed = 0
forward = True
direction_count = 0
dispensing = False
initial = cl.value()
less = False
stopfor = 0

motor.run_timed(speed_sp=-450, time_sp=120)

while (count_dispensed < numberPills):
#    print(cl.value())
    if (direction_count > 200):
        if (forward):
           motor.run_timed(speed_sp=450, time_sp=120)
           forward = False
           direction_count = 0
        else:
           motor.run_timed(speed_sp=-450, time_sp=120)
           forward = True
           direction_count = 0
    
    if (not dispensing and stopfor == 0):
        if (cl.value() <= (initial-2)):
           #print('downdowndowndowndowndowndowndown')
           dispensing = True
           less = True
        #   count_dispensed = count_dispensed + 1
         #  print(str(count_dispensed) + ' pills dispensed')
        elif (cl.value() >= (initial+2)):
           #print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
           less = False
           dispensing = True
        #   count_dispensed = count_dispensed + 1
         #  print(count_dispensed)
       #    initial = cl.value()

    elif (stopfor == 0):
        if (less and cl.value() > (initial-2)):
            dispensing = False
            count_dispensed = count_dispensed + 1
            print(str(count_dispensed) + ' pills dispensed')
        elif (not less and cl.value() <= (initial+1) and cl.value() >= (initial-1)):
            dispensing = False
            count_dispensed = count_dispensed + 1
            print(str(count_dispensed) + ' pills dispensed')
            stopfor = 10                
           
    direction_count = direction_count + 1
    if (stopfor != 0):
        stopfor = stopfor - 1
    time.sleep(0.0005)
