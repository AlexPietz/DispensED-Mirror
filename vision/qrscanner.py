import cv2


def detect_qr(img):
    """
    Scans an image for QR codes. If it finds one, it returns True, else False. Should be fast enough to use
    in real-time applications, might have to add robustness for situations where QR is not on the ground
    :param img: CV image to scan
    :return: True if QR code is found, otherwise False
    """
    edges = cv2.Canny(img, 100, 200)
    (_, contours, hierarchy) = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    mark = 0

    for i in range(0, len(contours)):
        k = i
        c = 0

        while hierarchy[0][k][2] != -1:
            k = hierarchy[0][k][2]
            c += 1

        if hierarchy[0][k][2] != -1:
            c += 1

        if c >= 5:
            mark += 1

    if mark >= 3:
        return True
    else:
        return False