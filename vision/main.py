import cv2
import linedetect
import qrscanner


if __name__ == "__main__":
    cap = cv2.VideoCapture("test_orange.mp4")

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0,0), fx=0.7, fy=0.7)
        qr_contours = qrscanner.detect_qr(frame)
        frame = cv2.drawContours(frame, qr_contours, -1, (0, 255, 0), 3)
        line_contour = linedetect.detect_line(frame, 15)
        # if not (line_contour == None):
        frame = cv2.drawContours(frame, [line_contour], -1, (0, 0, 255), 3)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break