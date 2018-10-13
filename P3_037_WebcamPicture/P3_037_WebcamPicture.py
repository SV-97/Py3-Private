import numpy
import cv2

window = "Take a picture"
cv2.namedWindow(window)
camera = cv2.VideoCapture(0)

if camera.isOpened():
    rval, frame = camera.read()
else:
    rval = False

while rval:
    cv2.imshow(window, frame)
    rval, frame = camera.read()
    key = cv2.waitKey(10)
    if key == 27:
        break
    key2 = cv2.waitKey(10)
    if key == 32:
        cv2.imwrite("CapturedPicture.png", frame)
        break
camera.release()
cv2.destroyWindow(window)