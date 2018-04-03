from imutils.video.pivideostream import PiVideoStream
import paho.mqtt.client as mqtt
import cv2
import linedetect
import qrscanner
import time
import numpy as np
import requests

dispensing_return = 0
line_colour = 0
server_hostname = "http://34.245.208.59:5000"
patients = []

def on_connect(client, userdata, flags, rc):
    print("Connected with code: " + str(rc))
    client.subscribe("dispensing/out")
    client.subscribe("movement/out")
    client.subscribe("refilling/out")


def on_message(client, userdata, msg):
    string = msg.payload.decode()
    if msg.topic == "dispensing/out":
        global dispensing_return
        if string == "1":
            dispensing_return = 1
        else:
            dispensing_return = 2

    if msg.topic == "refilling/out":
        if string == "refill_start":
            requests.put(server_hostname + "/updatestatus", data={'status': 'refilling', 'details': ''})
            while True:
                r = requests.get().json()
                if r['set']:
                    refillstring = ''
                    if r['singles']:
                        refillstring += '1'
                    else:
                        refillstring += '0'
                    for package in r['packages']:
                        refillstring += ',' + package
                    break

        if string == "0":
            requests.put(server_hostname + "/updatestatus", data={'status': 'error', 'details': 'Refilling failed'})
        if string == "1":
            requests.put(server_hostname + "/updatestatus", data={'status': 'idle', 'details': ''})


def handle_qr(data):
    global line_colour
    global server_hostname
    global patients
    string = data[0].data.decode('ascii')

    # We wait at the start until we get a list of patients
    if string.startswith("start"):
        while True:
            r = requests.get(server_hostname + "/dbread").json()
            if len(r) > 0:
                requests.put(server_hostname + "/updatestatus", data={'status': 'dispensing', 'details': ''})
                line_colour = int(string.split(',')[1])
                patients = r

    # Return to base
    if string.startswith("return"):
        r = requests.put(server_hostname + "/updatestatus", data={'status': 'dispensing', 'details': 'Returning to base'})
        line_colour = int(string.split(',')[1])

    # Send necessary details to dispenser
    if string.startswith("patient"):
        drug_a = 0
        time_a = ""
        drug_b = 0
        time_b = ""
        drug_package = "None"
        for patient in patients:
            if patient['qr_code'] == string.split(',')[1]:
                for drug in patient['drugs']:
                    if drug['drug_id'] == 1:
                        drug_a = drug['qty']
                        time_a = drug['time']
                    if drug['drug_id'] == 2:
                        drug_b = drug['qty']
                        time_b = drug['time']
                if not patient['drug_package'] == '0':
                    drug_package = patient['drug_package']
                identification = patient['patient_auth_colour']
                id = patient['patient_id']
                dispense(identification + ',' + str(drug_a) + ',' + str(drug_b) + ',' + drug_package, id, time_a, time_b)



def dispense(string, id, time_a, time_b):
    client.publish("dispensing", string)
    global dispensing_return
    while(True):
        if dispensing_return == 1:
            dispensing_return = 0
            if len(time_a > 0):
                requests.put(server_hostname + "/dispensed", data={'patient_id': id, 'drug_id': 1, 'time': time_a})
            if len(time_b > 0):
                requests.put(server_hostname + "/dispensed", data={'patient_id': id, 'drug_id': 2, 'time': time_b})
            break
        if dispensing_return == 2:
            dispensing_return = 0
            r = requests.put(server_hostname + "/updatestatus", data={'status': 'error', 'details': 'patient has not picked up medication'})
            break


# Set up MQTT
client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.on_connect = on_connect
client.on_message = on_message

client.loop_start()

# Prepare camera and performance statistics
vs = PiVideoStream(resolution=(640, 480)).start()
time.sleep(1)
vs.camera.shutter_speed = 5000
while True:

    if requests.get(server_hostname + "/go").text == "True":
        line_panic = 0

        # Find the first QR
        while True:
            frame = vs.read()

            qr_data = qrscanner.read_qr_whole(frame)
            if len(qr_data) > 0:
                handle_qr(qr_data)
                break
            else:
                client.publish("movement", "start,-200,-200")
                time.sleep(0.2)
                client.publish("movement", "stop")
                line_panic += 1
                if line_panic > 10:
                    # Failed to find the initial QR - stop

                    r = requests.put(server_hostname + "/updatestatus", data={'status': 'error', 'details': 'cannot find first QR'})
                    break


        qr_delay = 0
        line_panic = 0

        # Loop until we find a QR
        print('SCANNING')
        while True:
            frame = vs.read()

            # We only want to read a QR code if we've not just seen one
            if qr_delay >= 40:
                qr_data = qrscanner.read_qr_whole(frame)
                if len(qr_data) > 0:
                    client.publish("movement", "stop")
                    print('QR FOUND')
                    print(qr_data)
                    handle_qr(qr_data)
                    qr_delay = 0
                    time.sleep(0.2)

            qr_delay += 1

            line_frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
            line_contours, clean = linedetect.detect_line(line_frame, line_colour)
            if (len(line_contours) > 0):
                direction = linedetect.extract_direction_max(line_contours, np.shape(line_frame))
                direction = (0.5 * direction + 0.5 * linedetect.extract_direction_average(clean, np.shape(line_frame)))
                print(direction)
                direction = direction
                max_speed = 400
                if direction > 0:
                    left = max_speed
                    right = max_speed - (max_speed * direction)
                else:
                    right = max_speed
                    left = max_speed + (max_speed * (direction))
                client.publish("movement", "start," + str(-left) + "," + str(-right))

                line_panic = 0
            else:
                # No line found
                if line_panic > 30:
                    # if we don't find a line for a long time - stop and notify server
                    client.publish("movement", "stop")
                    time.sleep(0.2)
                    client.publish("movement", "stop")
                    break
                    r = requests.put(server_hostname + "/updatestatus", data={'status': 'error', 'details': 'lost line'})
                line_panic += 1

    else:
        time.sleep(5)


# do a bit of cleanup
vs.stop()