import numpy as np
import cv2
from pyzbar import pyzbar
from time import sleep
from collections import Counter
from sys import stderr

def zbar_rect_correction(x,y,w,h):
    return ((x, y), (x + w, y + h))

window = "Take a picture"
cv2.namedWindow(window)
camera = cv2.VideoCapture(0)

if camera.isOpened():
    rval, frame = camera.read()
else:
    rval = False

found_codes = []
counter = []
while rval:
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        barcode_information = (barcode.type, barcode.data.decode("utf-8"))
        counter.append(barcode_information[1])
        if barcode_information not in found_codes:
            found_codes.append(barcode_information)
            print("Found {} barcode: {}".format(*found_codes[-1]))
        poly = barcode.polygon
        poly = np.asarray([(point.x, point.y) for point in poly])
        poly = poly.reshape((-1,1,2))
        cv2.polylines(frame, [poly] ,True, (0,255,0), 2)
        cv2.rectangle(frame, *zbar_rect_correction(*barcode.rect), (122, 122, 0), 2)
        x, y = barcode.rect[:2]
        cv2.putText(frame, "{}({})".format(*barcode_information), (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
    cv2.imshow(window, frame)
    if barcodes:
        pass
       # sleep(5)
    rval, frame = camera.read()
    key = cv2.waitKey(1)
    if key == 27:
        stderr.write("Aborted")
        break
    if counter:
        code = Counter(counter).most_common(1)[0]
        if code[1] > 20:
            print(code[0])
            break
camera.release()
cv2.destroyWindow(window)