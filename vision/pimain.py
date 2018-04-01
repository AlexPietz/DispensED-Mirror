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
server_hostname = ""

def on_connect(client, userdata, flags, rc):
    print("Connected with code: " + str(rc))
    client.subscribe("dispensing/out")
    client.subscribe("movement/out")


def on_message(client, userdata, msg):
    string = msg.payload.decode()
    if msg.topic == "dispensing/out":
        global dispensing_return
        if string == "1":
            dispensing_return = 1
        else:
            dispensing_return = 2


def handle_qr(data):
    global line_colour
    global server_hostname
    string = data.data
    if string.startswith("start"):
        # TODO: check if anything needs delivering
        line_colour = int(string.split(',')[1])
    if string.startswith("end"):
        # r = requests.put(server_hostname, data={'status': 'returning'})
        # TODO: notify server we're on our way back
        line_colour = int(string.split(',')[1])
    if string.startswith("patient"):
        dispense(string)



def dispense(string):
    client.publish("dispensing", string)
    global dispensing_return
    while(True):
        #client.loop()
        if dispensing_return == 1:
            dispensing_return = 0
            # TODO: notify server of success
            break
        if dispensing_return == 2:
            dispensing_return = 0
            # r = requests.put(server_hostname, data={'status': 'FAILED TO DISPENSE'})
            # TODO: notify server of failure
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

qr_delay = 11
line_panic = 0

# Loop until we find a QR
print('SCANNING')
while True:
    frame = vs.read()

    line_frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
    line_contours, clean = linedetect.detect_line(line_frame, line_colour)
    if (len(line_contours) > 0):
        direction = linedetect.extract_direction_max(line_contours, np.shape(line_frame))
        #direction = linedetect.extract_direction_average(clean, np.shape(line_frame))
        direction = (0.7 * direction + 0.3 * linedetect.extract_direction_average(clean, np.shape(line_frame)))
        print(direction)
        direction = direction*1.3
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
        if line_panic > 30:
            client.publish("movement", "stop")
            #break
            # r = requests.put(server_hostname, data={'status': 'STUCK'})
        line_panic += 1

    if qr_delay >= 40:
#        qr_contours = qrscanner.detect_qr(frame)
        qr_data = qrscanner.read_qr_whole(frame)
        #if qr_contours != None:
        if len(qr_data) > 0:
            client.publish("movement", "stop")
            print('QR FOUND')
#            qr_data = qrscanner.read_qr(frame, qr_contours)
            #qr_data=qrscanner.read_qr_whole(frame)
            if len(qr_data) > 0:
                print(qr_data)
                #handle_qr(qr_data)
                #dispense("red,0,0,red")
                qr_delay = 0
            time.sleep(0.2)

    qr_delay += 1


# do a bit of cleanup
vs.stop()