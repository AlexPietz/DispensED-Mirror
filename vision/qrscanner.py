import cv2


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

        print(abs((area_1 / area_2) - (49 / 25)))
        print(abs((area_2 / area_3) - (25 / 9)) )

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
        return markers
    else:
        return None
