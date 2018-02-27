from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
import paho.mqtt.client as mqtt
import cv2
import linedetect
import qrscanner
import time


# Set up MQTT
client = mqtt.Client()
client.connect("localhost", 1883, 60)

# Prepare camera and performance statistics
vs = PiVideoStream(resolution=(640, 480)).start()
time.sleep(1)
fps = FPS().start()
vs.camera.shutter_speed = 10000

# Loop until we find a QR
print('SCANNING')
while True:
    frame = vs.read()
    linedetect.detect_line(cv2.resize(frame, (0, 0), fx=0.3, fy=0.3), 15)
    qr_contours = qrscanner.detect_qr(frame)
    if qr_contours != None:
        client.publish("topic/test", "stop")
        print('QR FOUND')
        qr_data = qrscanner.read_qr(frame, qr_contours)
        if len(qr_data) > 0:
            print(qr_data)
            break

    # update the FPS counter
    fps.update()

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
vs.stop()
