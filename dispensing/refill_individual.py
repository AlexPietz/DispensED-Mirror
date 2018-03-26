#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time

def refill_indi:

    motor_A = ev3.MediumMotor('outB')
    motor_B = ev3.MediumMotor('outD')

    ev3.Sound.speak("Entered individual dispenser refill mode, please wait").wait()

    motor_A.run_timed(speed_sp=250, time_sp=190)
    motor_B.run_timed(speed_sp=250, time_sp=190)

    ev3.Sound.speak("Pills can now be added to the pill storage containers").wait()

    return "1"
