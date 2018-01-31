import os
import zxing
import cv2


def scan_qrcode(img):
    """
    Tries to find a QR code the supplied image (which can be cropped).
    This uses the zxing QR decoder, written in Java unfortunately. (Way) Too slow for real-time reading
    :param img: An opencv image (potentially) containing a QR code
    :return: A list of data in QR codes found, None if none are found.
    """
    # Create folder for opencv to write a temp image to
    temp_path = "./temp"
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    cv2.imwrite("temp/qr.jpg", img)

    # Have zxing decode the qr
    reader = zxing.BarCodeReader()
    barcode = reader.decode("temp/qr.jpg", "QR_CODE")
    if barcode == None:
        return None
    else:
        return barcode.parsed