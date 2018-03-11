from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
import paho.mqtt.client as mqtt
import cv2
import linedetect
import qrscanner
import time
import datetime
import numpy as np


# Set up MQTT
client = mqtt.Client()
client.connect("localhost", 1883, 60)

# Prepare camera and performance statistics
vs = PiVideoStream(resolution=(640, 480)).start()
time.sleep(1)
fps = FPS().start()
vs.camera.shutter_speed = 10000

data = []
npdata = []
found = 0
total = 0

# Loop until we find a QR
print('SCANNING')
while True:
    frame = vs.read()
    line_frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
    line_contours, clean = linedetect.detect_line(line_frame, 15)
    total += 1
    if (len(line_contours) > 0):
        found += 1
        direction = linedetect.extract_direction_max(line_contours, np.shape(line_frame))
        direction = (0.7 * direction + 0.3 * linedetect.extract_direction_average(clean, np.shape(line_frame)))
        print(direction)
        max_speed = 300
        if direction > 0:
            left = max_speed
            right = max_speed - (max_speed * direction)
        else:
            right = max_speed
            left = max_speed + (max_speed * direction)
        client.publish("topic/test", "start," + str(left) + "," + str(right))
        data.append((datetime.time() ,direction, left, right))
        npdata.append(line_contours)
    qr_contours = qrscanner.detect_qr(frame)
    if qr_contours != None:
        client.publish("topic/test", "stop")
        print('QR FOUND')
        qr_data = qrscanner.read_qr(frame, qr_contours)
        if len(qr_data) > 0:
            print(qr_data)
            break
        time.sleep(0.2)

    # update the FPS counter
    fps.update()

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
print("[INFO] Found lines in {:.2f}".format(found/float(total)))

f = open("data.txt", "w")
for d in data:
    f.write(str(d) + "\n")
f.close()

np.save("data.npy", np.array(npdata))

# do a bit of cleanup
vs.stop()