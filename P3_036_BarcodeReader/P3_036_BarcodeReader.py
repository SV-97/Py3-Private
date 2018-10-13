import numpy
import cv2
from pyzbar import pyzbar
"""Extract code from image
"""
paths = ["BottleBar.jpg", "QR.png"]

for path in paths:
    image = cv2.imread(path)
    height, width = image.shape[:2]
    resolution = width/height
    target_height = 640
    target_width = resolution*target_height
    height_factor = target_height/height
    width_factor = target_width/width
    image = cv2.resize(image, (0,0), fx=width_factor, fy=height_factor) 
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
    
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 0, 255), 2)
    
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

    name = "Barcode{}".format(paths.index(path))
    cv2.namedWindow(name)
    cv2.moveWindow(name, 0, 0)
    cv2.imshow(name, image)
cv2.waitKey(0)