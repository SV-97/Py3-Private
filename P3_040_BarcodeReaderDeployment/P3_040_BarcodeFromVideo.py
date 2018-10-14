
from argparse import ArgumentParser
from collections import Counter
from time import sleep
from sys import stderr

import cv2
import numpy as np
from pyzbar import pyzbar

parser = ArgumentParser(description="Get barcode from video feed")
parser.add_argument("-c", "--camera_id", dest="camera_id", default=0, type=int, help="ID for the video feed (default: use standart camera)")
parser.add_argument("-da", "--disable_abort", dest="disable_abort", default=False, type=bool, help="Disable closing the videofeed with esc or lmb (WARNING: Has to be killed if no code is found) (default: don't abort it)")
args = parser.parse_args()
camera_id = args.camera_id
disable_abort = args.disable_abort
print(camera_id)
print(disable_abort)
def zbar_rect_correction(x,y,w,h):
    return ((x, y), (x + w, y + h))

class Camera():
    """Context Manager for video streams
    """
    def __init__(self, camera_id):
        self.camera_id = camera_id
    def __enter__(self):
        self.camera = cv2.VideoCapture(self.camera_id)
        return self.camera
    def __exit__(self, exc_type, exc_value, traceback):
        self.camera.release()

run = True
def abort(event ,x ,y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            global run
            stderr.write("Aborted")
            run = False
window = "SV Barcode Reader"
cv2.namedWindow(window)
if not disable_abort:
    cv2.setMouseCallback(window, abort)
with Camera(camera_id) as camera:
    if camera.isOpened():
        rval, frame = camera.read()
    else:
        rval = False

    found_codes = []
    counter = []
    while rval & run:
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            barcode_information = (barcode.type, barcode.data.decode("utf-8"))
            counter.append(barcode_information[1])
            if barcode_information not in found_codes:
                found_codes.append(barcode_information)
                # print("Found {} barcode: {}".format(*found_codes[-1]))
            poly = barcode.polygon
            poly = np.asarray([(point.x, point.y) for point in poly])
            poly = poly.reshape((-1,1,2))
            cv2.polylines(frame, [poly] ,True, (0,255,0), 2)
            cv2.rectangle(frame, *zbar_rect_correction(*barcode.rect), (255, 0, 0), 2)
            x, y = barcode.rect[:2]
            cv2.putText(frame, "{}({})".format(*barcode_information), (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        cv2.imshow(window, frame)
        """
        if barcodes:
            sleep(5)
        """
        rval, frame = camera.read()
        key = cv2.waitKey(1)
        if not disable_abort:
            if key == 27:
                stderr.write("Aborted")
                break
        if counter:
            code = Counter(counter).most_common(1)[0]
            if code[1] > 20:
                print(code[0])
                break
cv2.destroyWindow(window)