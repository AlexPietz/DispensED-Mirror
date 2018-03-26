#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time
def refill_indi:
    motor_A = ev3.MediumMotor('outB')
    motor_B = ev3.MediumMotor('outD')

    motor_A.run_timed(speed_sp=250, time_sp=190)
    motor_B.run_timed(speed_sp=250, time_sp=190)

    return "1"
