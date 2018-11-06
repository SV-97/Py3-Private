import cv2
import numpy as np

def approximate_pi(k):
    def term(k):
        return (np.math.factorial(4*k)*(1103+26390*k))/(np.math.factorial(k)**4*396**(4*k))
    a = 2*np.sqrt(2)/9801*np.sum([term(k) for k in range(k)])
    return 1/a

def pad_image(im, color=255):
    """Pad an image with bars in specified color
    Args:
        im (np.ndarray): Image array in shape y, x
        color (int): value from 0-255 to specify color of padding
    """
    height, width = np.shape(im)[:2]
    length = max(height, width)
    length += 1 if length%2 else 0
    pad_total_y = length - height
    pad_top = pad_total_y//2
    pad_bottom = pad_total_y - pad_top
    pad_total_x = length - width
    pad_left = pad_total_x//2
    pad_right = pad_total_x - pad_left
    return cv2.copyMakeBorder(im, pad_top , pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=color)

def pattern_from_image(im, n_x, n_y):
    """Seperate an image into cubes
    Args:
        im (np.ndarray): Image array in shape y, x
        n_x (int): number of cubes x-wise
        n_y (int): number of cubes y-wise
    """
    height, width = np.shape(im)[:2]
    factor_x = n_x/width
    factor_y = n_y/height
    pattern = cv2.resize(im, (0, 0), fx=factor_x, fy=factor_y, interpolation=cv2.INTER_LANCZOS4)
    return pattern

def textify(im, file, pattern, n, color, fontsize):
    """Write text to image if corresponding value in pattern is True
    Args:
        im (np.ndarray): Image array in shape y, x
        file (string): Path to file with text that's to be used
        pattern (np.ndarray of bool): see pattern_from_image
        n (int): how many pixels are grouped for one letter
        color (int): value from 0-255 to specify color of text
        fontsize (int): fontsize of text
    """
    with open(file, "r") as f:
        im = np.ones((length, length))
        for y in range(len(pattern)):
            Y = pattern[y]
            for x in range(len(Y)):
                if Y[x]:
                    char = f.read(1)
                    cv2.putText(im, char, (x*n, y*n), cv2.FONT_HERSHEY_PLAIN, fontsize, color, 1)
    return im

boolify = np.vectorize(lambda x: True if x <= 127 else False)


# print(approximate_pi(500))
im = cv2.imread("Pi.png")[:,:,0]
im = pad_image(im)
length = np.shape(im)[0]
# cv2.imwrite("padded.png", im)
pattern = pattern_from_image(im, 150, 150)
# cv2.imwrite("pattern.png", pattern)
pattern = boolify(pattern)
im = textify(im, "Pi", pattern, 10, 255, 1)

cv2.imwrite("result.png", im)