from imutils.video.pivideostream import PiVideoStream
import paho.mqtt.client as mqtt
import cv2
import linedetect
import qrscanner
import time
import numpy as np

dispensing_return = 0

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
    string = data.data #TODO: check
    # run different functions


def dispense(string):
    client.publish("dispensing", string)
    global dispensing_return
    while(True):
        client.loop()
        if dispensing_return == 1:
            dispensing_return = 0
            # TODO: notify server of success
            break
        if dispensing_return == 2:
            dispensing_return = 0
            # TODO: notify server of failure
            break


# Set up MQTT
client = mqtt.Client()
client.connect("localhost", 1883, 60)

# Prepare camera and performance statistics
vs = PiVideoStream(resolution=(640, 480)).start()
time.sleep(1)
vs.camera.shutter_speed = 5000

# Loop until we find a QR
print('SCANNING')
while True:
    frame = vs.read()
    line_frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
    line_contours, clean = linedetect.detect_line(line_frame, 95)
    if (len(line_contours) > 0):
        direction = linedetect.extract_direction_max(line_contours, np.shape(line_frame))
        #direction = linedetect.extract_direction_average(clean, np.shape(line_frame))
        direction = (0.7 * direction + 0.3 * linedetect.extract_direction_average(clean, np.shape(line_frame)))
        print(direction)
        max_speed = 300
        if direction > 0:
            left = max_speed
            right = max_speed - (max_speed * direction)
        else:
            right = max_speed
            left = max_speed + (max_speed * direction)
        client.publish("movement", "start," + str(left) + "," + str(right))
    qr_contours = qrscanner.detect_qr(frame)
    if qr_contours != None:
        client.publish("movement", "stop")
        print('QR FOUND')
        qr_data = qrscanner.read_qr(frame, qr_contours)
        if len(qr_data) > 0:
            print(qr_data)
            client.publish("dispensing", "go")
            break
        time.sleep(0.2)

# do a bit of cleanup
vs.stop()