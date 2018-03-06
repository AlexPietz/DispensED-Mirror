import cv2
import numpy as np


def detect_line(img, hue):
    """
    Tries to threshold based on hue.
    :param img: The (COLOUR!) image to threshold
    :param hue: The hue value to Threshold on
    :return: A binary (thresholded) image
    """
    hue_lower = hue - 15
    hue_upper = hue + 15

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # inRange doesn't neatly wrap Hue values (0-179), so we have to do two thresholds in some cases
    # (which can then be OR'd)
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

    # Remove noise, we can be fairly aggressive with the kernel as the line should be thick
    clean = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, np.ones((8, 8), np.uint8))
    clean = cv2.dilate(clean, np.ones((5,5), np.uint8))
    contours = cv2.findContours(clean, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[1]
    if len(contours) == 0:
        return []

    # Find the largest contour, which we assume is the line
    contour = max(contours, key=cv2.contourArea)

    return contour


def extract_direction(contour, size):
    # Get the highest point (CV images count y top to bottom, so we want the min y value)
    def get_y(pair): return pair[0][1]
    highest_point = min(contour, key=get_y)
    filtered = list(filter(lambda x: x[0][1] == highest_point[0][1], contour))
    highest_point = np.mean(filtered, 0)

    dx = highest_point[0][0] - size[1] / 2
    dy = size[0] - highest_point[0][1]

    print((dx,dy))

    return np.arctan(dx/dy)
