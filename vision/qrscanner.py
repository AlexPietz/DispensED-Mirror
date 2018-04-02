import cv2
import numpy as np
from imutils import perspective
import zbar

def detect_qr(img):
    """
    Scans an image for QR codes. If it finds one, it returns True, else False. Should be fast enough to use
    in real-time applications.
    :param img: CV image to scan
    :return: Contours for the markers found, otherwise None
    """
    # Checks if nested contours are indeed markers
    def is_marker(contours):
        if len(contours) != 6:
            return False

        area_1 = cv2.contourArea(contours[1])
        area_2 = cv2.contourArea(contours[3])
        area_3 = cv2.contourArea(contours[5])

        if abs((area_1 / area_2) - (49 / 25)) > 0.5:
            return False
        if abs((area_2 / area_3) - (25 / 9)) > 1:
            return False

        return True

    # Find edges and contours
    edges = cv2.Canny(img, 200, 300)
    (_, contours, hierarchy) = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    markers = []

    # Go over all of the contours and check how many  children they have
    for i in range(0, len(contours)):
        check_next = i
        contour_list = [contours[check_next]]

        while hierarchy[0][check_next][2] != -1:
            check_next = hierarchy[0][check_next][2]
            contour_list.append(contours[check_next])

        if hierarchy[0][check_next][2] != -1:
            contour_list.append(contours[check_next])

        # Check if the contour + its children make for a marker
        if is_marker(contour_list):
            markers.append(contour_list[0])

    # If we have three (or more - will need fixing) markers, we've got a QR
    if len(markers) >= 3:
        clean_markers = []
        for marker in markers:
            clean_markers.append(cv2.approxPolyDP(marker, 0.1*cv2.arcLength(marker, True), True))
        return clean_markers
    else:
        return None

def read_qr(img, contours):
    """
    Reads the QR code spotted in the image
    :param img: image to inspect
    :return: the parsed QR code
    """
    # clean up opencv's weird contours layout
    pts_list = []
    for contour in contours:
        pts_list.append(np.array([ points.flatten() for points in contour ], dtype="float32"))

    # sort the points in each of the markers (top-left, top-right, bottom-left, bottom-right)
    markers = [perspective.order_points(marker) for marker in pts_list]
    for marker in markers:
        tmp = np.array(marker[3], dtype="float32")
        marker[3] = marker[2]
        marker[2] = tmp

    # Sort the markers (top-left, top-right, bottom-left)
    def sum_point(marker):
        return marker[0][0] + marker[0][1]
    markers = sorted(markers, key=sum_point)
    if markers[1][0][0] < markers[2][0][0]:
        tmp = markers[2]
        markers[2] = markers[1]
        markers[1] = tmp

    ratio = 33/7.0 #ratio between marker and the entire qr

    # Define the source QR
    src = [markers[0][0] - 5,
           markers[1][1] + [5, -5],
           markers[2][2] + [-5, 5]]
    # Find the fourth corner (which doesn't have a marker)
    src.append(markers[1][1] + ratio * (markers[1][3] - markers[1][1]) + 5)
    src[3] = (src[3] + markers[2][2] + ratio * (markers[2][3] - markers[2][2]) + 5) / 2
    src[3] = (src[3] + markers[0][0] + ratio * (markers[0][3] - markers[0][0]) + 5) / 2

    # Define a target to map to
    qr_size = 100
    matrix = cv2.getPerspectiveTransform(np.array(src, dtype="float32"), np.array([
        [0,0],
        [qr_size - 1, 0],
        [0, qr_size - 1],
        [qr_size - 1, qr_size - 1]], dtype="float32"))

    # Do the perspective warp
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    qr_img = cv2.warpPerspective(img, matrix, (qr_size, qr_size))
    _, qr_img = cv2.threshold(qr_img, 0, 255, cv2.THRESH_OTSU)

    # Scan and return results
    scanner = zbar.Scanner()
    results = scanner.scan(qr_img)
    return results


def read_qr_whole(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    scanner = zbar.Scanner()
    results = scanner.scan(img)
    return results