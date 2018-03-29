#! /usr/bin/env python3
import sys
import ev3dev.ev3 as ev3
import time
import paho.mqtt.client as mqtt


dispensers = {}
dispensers['A'] = (ev3.MediumMotor('outA'), ev3.ColorSensor(ev3.INPUT_1))
dispensers['B'] = (ev3.MediumMotor('outB'), ev3.ColorSensor(ev3.INPUT_2))

def on_connect(client, userdata, flags, rc):
    print("Connected with code: " + str(rc))
    client.subscribe("dispensing")

def dispense_pills(client, userdata, msg):
    msg = msg.payload.decode()
    cl = dispensers[msg[0]][1]
    cl.mode='COL-REFLECT'
    motor=dispensers[msg[0]][0]

    numberPills = int(msg[2]) # number of pills to be dispensed
    count_dispensed = 0 # number of pills that have been dispensed so far
    forward = True # direction of motor
    direction_count = 0 # number of iterations since direction change
    dispensing = False # whether dispenser is curently in the process of dispensing
    initial = cl.value() # initial value of colour sensor
    less = False # represents whether cl.value() decreases (or increases) at start of dispensing
    stopfor = 0 # if cl value increases, then we stop checking colour sensor for 10 iterations
    dispense_attempts = 0

    motor.run_timed(speed_sp=-250, time_sp=190)

    while (count_dispensed < numberPills):
        print(cl.value())
        if (dispense_attempts >= 10):
            print('Error: dispenser time-out! - pill not dispensed')
            client.publish("dispensing", "0")
            motor.stop()
            break

        # reverse direction every 200 iterations
        if (direction_count > 200):
            if (forward):
                motor.run_timed(speed_sp=250, time_sp=190)
            else:
                motor.run_timed(speed_sp=-250, time_sp=190)
                dispense_attempts += 1
            forward = not forward
            direction_count = 0

        if (not dispensing and stopfor == 0):
            # if sensor value changes by +-2 then we have started pill dispensing
            # sensor behaviour after initial change is dependent on pill position
            # so cases of value increase and decrease must be seperated
            if (cl.value() <= (initial - 2)):
                dispensing = True
                less = True
            elif (cl.value() >= (initial + 2)):
                less = False
                dispensing = True

        elif (stopfor == 0):
            if (less and cl.value() >= (initial - 2)):
                # if sensor value originally decreased, and value has now increased
                # then dispense is complete
                dispensing = False
                count_dispensed += 1
                dispense_attempts = 0
                print(str(count_dispensed) + ' pills dispensed')
                stopfor = 20
            elif (not less and cl.value() <= (initial + 1) and cl.value() >= (initial - 1)):
                # if sensor value originally increased, it may decrease below normal
                # before returning to normal, so stop monitoring sensor value for 10 iterations
                dispensing = False
                count_dispensed += 1
                dispense_attempts = 0
                print(str(count_dispensed) + ' pills dispensed')
                stopfor = 20

        direction_count += 1
        if (stopfor != 0):
            stopfor -= 1
        time.sleep(0.0005)  # increase length of iteration
    motor.stop()
    if count_dispensed > numberPills:
        client.publish("dispensing", "0")
    else:
        client.publish("dispensing", "1")

client = mqtt.Client()
client.connect("192.168.17.130", 1883, 60)

client.on_connect = on_connect
client.on_message = dispense_pills

client.loop_forever()