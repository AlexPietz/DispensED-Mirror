import cv2


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

    if hue_lower < 0:
        hue_lower_1 = 255 - hue_lower
        thresholded_1 = cv2.inRange(hsv_img, [hue_lower_1, 100, 100], [255, 100, 100])
        thresholded_2 = cv2.inRange(hsv_img, [0, 100, 100], [hue_upper, 100, 100])
        thresholded = cv2.bitwise_or(thresholded_1, thresholded_2)
    elif hue_upper > 255:
        hue_upper_1 = hue_upper - 255
        thresholded_1 = cv2.inRange(hsv_img, [hue_lower, 100, 100], [255, 100, 100])
        thresholded_2 = cv2.inRange(hsv_img, [0, 100, 100], [hue_upper_1, 100, 100])
        thresholded = cv2.bitwise_or(thresholded_1, thresholded_2)
    else:
        thresholded = cv2.inRange(hsv_img, [hue_lower, 100, 100], [hue_upper, 255, 255])

    return thresholded


