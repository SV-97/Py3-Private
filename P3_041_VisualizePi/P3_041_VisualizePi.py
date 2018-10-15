import cv2
import numpy as np

def approximate_pi(k):
    def term(k):
        return (np.math.factorial(4*k)*(1103+26390*k))/(np.math.factorial(k)**4*396**(4*k))
    a = 2*np.sqrt(2)/9801*np.sum([term(k) for k in range(k)])
    return 1/a

window = "Pi"
cv2.namedWindow(window)

print(approximate_pi(500))
im = cv2.imread("Pi.png")[:,:,0]
height, width = np.shape(im)[:2]
length = height if height > width else width
length += 1 if length%2 else 0
new = np.full((length, length), 0)
height_offset_1 = (length - height)//2
height_offset_2 = length - height - height_offset_1
width_offset_1 = (length - width)//2
width_offset_2 = length - width - width_offset_1
new[height_offset_1:length-height_offset_2, width_offset_1:length-width_offset_2] += im
im = new
cv2.imwrite("new.png", im)
n = 20
a = []
for line in im:
    b = [(np.sum(line[i:i+n])) for i in range(0, length, n)]
    a.append(b)
a = np.asarray(a)
a = [sum(np.dstack(a[i:i+n])) for i in range(0, length, n)]
a = np.asarray(a)
a = [[True if sum(x)/n <= 127 else False for x in b] for b in a]
pattern = np.asarray(a)

with open("Pi", "r") as f:
    im = np.ones((length, length))
    for y in range(len(pattern)):
        Y = pattern[y]
        for x in range(len(Y)):
            if Y[x]:
                char = f.read(1)
                cv2.putText(im, char, (x*n, y*n), cv2.FONT_HERSHEY_PLAIN, 2, 0, 1)

cv2.imwrite("SCHOKOLADE.png", im)
im = cv2.resize(im, (0,0), fx=0.5, fy=0.5)
cv2.imshow(window, im)
cv2.waitKey(0)