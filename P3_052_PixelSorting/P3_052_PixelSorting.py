import matplotlib.pyplot as plt
import numpy as np

im = plt.imread("Image.jpeg")
im = plt.imread("Image.png")
plt.subplot(1, 2, 1)
plt.imshow(im)

height, width, channels = np.shape(im)
im = im.flatten().reshape(height * width, channels)

filtered_im = np.asarray(sorted(im, key=lambda triplet: sum(triplet)/3)).reshape(height, width, channels)

print(np.shape(filtered_im))
plt.subplot(1, 2, 2)
plt.imshow(filtered_im, cmap="binary")
plt.show()