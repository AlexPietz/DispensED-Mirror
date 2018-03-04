import cv2
import linedetect
import qrscanner
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('filename', metavar='F', type=str, help='Filename for the video')
ap.add_argument("hue", type=int, help="The value of the hue to threshold on")
args = vars(ap.parse_args())

if __name__ == "__main__":
    cap = cv2.VideoCapture(args["filename"])

    qr_no = 0
    qr_fail = 0
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        orig_frame = frame.copy()
        qr_contours = qrscanner.detect_qr(frame)
        frame = cv2.drawContours(frame, qr_contours, -1, (0, 255, 0), 3)
        line_contour = linedetect.detect_line(frame, args["hue"])
        print(linedetect.extract_direction(line_contour, np.shape(frame)))
        # if not (line_contour == None):
        frame = cv2.drawContours(frame, [line_contour], -1, (0, 0, 255), 3)

        if qr_contours != None:
            results = qrscanner.read_qr(orig_frame, qr_contours)
            print(results)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break