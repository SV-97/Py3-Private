import numpy as np
import cv2
from pyzbar import pyzbar
from collections import Counter
from sys import stderr
import threading

def zbar_rect_correction(x,y,w,h):
    return ((x, y), (x + w, y + h))

class Camera():
    """Context Manager for video streams
    """
    def __init__(self, camera_id):
        self.camera_id = camera_id
    def __enter__(self):
        self.camera = cv2.VideoCapture(self.camera_id)
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.camera.release()



class ReadCode(threading.Thread):
    """Read a barcode
    Args:
        image (list): THIS WILL BE MUTATED serves as In/Out of image between threads
        camera_id (int): ID of the camera to use
        lock (threading.Lock): Lock for critical sections with image
    """
    def __init__(self, image, lock, camera_id=0):
        super().__init__()
        self.lock = lock
        self.image = image
        self.camera_id = camera_id
        self.camera = cv2.VideoCapture(self.camera_id)

    def run(self):  
        with Camera(self.camera_id):
            if self.camera.isOpened():
                rval, frame = self.camera.read()
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
                    poly = barcode.polygon
                    poly = np.asarray([(point.x, point.y) for point in poly])
                    poly = poly.reshape((-1,1,2))
                    cv2.polylines(frame, [poly] ,True, (0,255,0), 2)
                    cv2.rectangle(frame, *zbar_rect_correction(*barcode.rect), (122, 122, 0), 2)
                    x, y = barcode.rect[:2]
                    cv2.putText(frame, "{}({})".format(*barcode_information), (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
                with self.lock:
                    self.image[0] = frame
                rval, frame = self.camera.read()
                key = cv2.waitKey(1)
                if key == 27:
                    stderr.write("Aborted")
                    break
                if counter:
                    code = Counter(counter).most_common(1)[0]
                    if code[1] > 20:
                        print(code[0])
                        break
        