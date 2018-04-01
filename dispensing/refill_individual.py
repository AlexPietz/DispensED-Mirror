#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time

def enter(state):
    global pressed
    pressed = True
    return "1"

def refill_indi():
    global pressed
    pressed = False

    motor_A = ev3.MediumMotor('outB')
    motor_B = ev3.MediumMotor('outD')

    ev3.Sound.speak("Entered individual dispenser refill mode, please wait").wait()
    time.sleep(2)

    motor_A.run_timed(speed_sp=-250, time_sp=190)
    motor_B.run_timed(speed_sp=-250, time_sp=190)

    ev3.Sound.speak("Pills can now be added to the pill storage containers").wait()
    time.sleep(2)

    btn = ev3.Button()
    btn.on_enter = enter # on enter button pressed

    start_time = time.time()

    while time.time() < start_time + 60:
        result = btn.process()
        if pressed:
            return "1"

    return "0"
