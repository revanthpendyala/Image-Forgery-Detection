import numpy as np
import cv2
import pywt
from matplotlib import pyplot as plt

def sliding_window(image, stepSize):
	windowSize = image.shape
	# slide a window across the image
	for y in xrange(0, image.shape[0], stepSize):
		for x in xrange(0, image.shape[1], stepSize):
			# yield the current window
			yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


img = cv2.imread('horse_blur.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# plt.imshow(gray),plt.show()

coeffs = pywt.dwt2(gray, 'haar')
cA, (cH, cV, cD) = coeffs
size = cA.shape
cA = np.reshape(cA, [size[0]*2, size[1]/2])


# plt.imshow(cA),plt.show()




