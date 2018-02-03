import cv2
import numpy as np


def detect_line(img, hue):
    """
    Tries to threshold based on hue.
    :param img: The (COLOUR!) image to threshold
    :param hue: The hue value to Threshold on
    :return: A binary (thresholded) image
    """
    hue_lower = hue - 10
    hue_upper = hue + 10
    print(str(hue_upper) + str(hue_lower))

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if hue_lower < 0:
        hue_lower_1 = 179 + hue_lower
        thresholded_1 = cv2.inRange(hsv_img, np.array([hue_lower_1, 100, 100]), np.array([179, 255, 255]))
        thresholded_2 = cv2.inRange(hsv_img, np.array([0, 100, 100]), np.array([hue_upper, 255, 255]))
        thresholded = cv2.bitwise_or(thresholded_1, thresholded_2)
    elif hue_upper > 179:
        hue_upper_1 = hue_upper - 179
        thresholded_1 = cv2.inRange(hsv_img, np.array([hue_lower, 100, 100]), np.array([179, 255, 255]))
        thresholded_2 = cv2.inRange(hsv_img, np.array([0, 100, 100]), np.array([hue_upper_1, 255, 255]))
        thresholded = cv2.bitwise_or(thresholded_1, thresholded_2)
    else:
        thresholded = cv2.inRange(hsv_img, np.array([hue_lower, 100, 100]), np.array([hue_upper, 255, 255]))

    return thresholded


