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


def extract_direction(img, center):
    clean = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((8, 8), np.uint8))
    contours = cv2.findContours(clean, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[1]
    if len(contours) == 0:
        return None

    contour = max(contours, key=cv2.contourArea)

    def get_y(pair): return pair[0][1]
    highest_point = min(contour, key=get_y)

    dx = highest_point[0][0] - center[0]
    dy = center[1] - highest_point[0][1]

    return np.sin(dx/dy)
