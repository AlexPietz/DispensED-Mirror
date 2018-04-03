#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time

def dispense_number(number_pills):

    cl_A = ev3.ColorSensor(ev3.INPUT_1)
    cl_A.mode = 'COL-REFLECT'
    cl_B = ev3.ColorSensor(ev3.INPUT_3)
    cl_B.mode = 'COL-REFLECT'
    motor_A = ev3.MediumMotor('outB')
    motor_B = ev3.MediumMotor('outD')

    if number_pills[0:2] == [0,0]:
        return True

    if not dispense(motor_A, int(number_pills[0])):
        return False
    if not dispense(motor_B, int(number_pills[1])):
        return False

    ev3.Sound.speak("Pills are now ready for collection").wait()
    time.sleep(0.5)
    initial = cl_B.value()
    start_time = time.time()

    while True:
        value = cl_B.value()
        if value <= (initial - 4) or value >= (initial + 4):
            print('Pills taken')
            #time.sleep(10)
            return True
        if time.time() > start_time + 30:
            return False


def dispense(motor, no_to_dispense):
    cl_A = ev3.ColorSensor(ev3.INPUT_1)
    cl_A.mode = 'COL-REFLECT'
    cl_B = ev3.ColorSensor(ev3.INPUT_3)
    cl_B.mode = 'COL-REFLECT'
    motor_A = ev3.MediumMotor('outB')
    motor_B = ev3.MediumMotor('outD')

    if no_to_dispense == 0:
        return True

    forward = True  # direction of motor
    direction_count = 0  # number of iterations since direction change
    dispensing = False  # whether dispenser is curently in the process of dispensing
    initial = cl_A.value()  # initial value of colour sensor
    less = False  # represents whether cl.value() decreases (or increases) at start of dispensing
    stopfor = 0  # if cl value increases, then we stop checking colour sensor for 10 iterations
    dispense_attempts = 0
    count_dispensed = 0  # number of pills that have been dispensed so far

    motor.run_timed(speed_sp=-250, time_sp=190)
    while count_dispensed < no_to_dispense:
        if dispense_attempts >= 10:
            print('Error: dispenser time-out! - pill not dispensed')
            motor.stop()
            return False

        # reverse direction every 200 iterations
        if direction_count > 100:
            if forward:
                motor.run_timed(speed_sp=250, time_sp=190)
            else:
                motor.run_timed(speed_sp=-250, time_sp=190)
                dispense_attempts += 1
            forward = not forward
            direction_count = 0

        if not dispensing and stopfor == 0:
            # if sensor value changes by +-2 then we have started pill dispensing
            # sensor behaviour after initial change is dependent on pill position
            # so cases of value increase and decrease must be seperated
            if cl_A.value() <= (initial - 2):
                dispensing = True
                less = True
            elif cl_A.value() >= (initial + 2):
                less = False
                dispensing = True

        elif stopfor == 0:
            if less and cl_A.value() >= (initial - 2):
                # if sensor value originally decreased, and value has now increased
                # then dispense is complete
                dispensing = False
                count_dispensed += 1
                dispense_attempts = 0
                print(str(count_dispensed) + ' pills dispensed')
                stopfor = 20
            elif not less and (initial + 1) >= cl_A.value() >= (initial - 1):
                # if sensor value originally increased, it may decrease below normal
                # before returning to normal, so stop monitoring sensor value for 10 iterations
                dispensing = False
                count_dispensed += 1
                dispense_attempts = 0
                print(str(count_dispensed) + ' pills dispensed')
                stopfor = 20

        direction_count += 1
        if stopfor != 0:
            stopfor -= 1
        time.sleep(0.0005)  # increase length of iteration
    motor.stop()
    time.sleep(1)
    return True
