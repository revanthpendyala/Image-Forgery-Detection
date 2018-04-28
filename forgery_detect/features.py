import numpy as np
import cv2
import pywt
from matplotlib import pyplot as plt
from scipy import fftpack
from copy import deepcopy
from collections import OrderedDict
from operator import itemgetter

def convert_array(arr):
	for i, x in enumerate(arr):
		arr[i] = np.array(list(x))

# Returns the k_l blocks matrix
def sliding_window(data, window):
	# Tune these latter
	stride = 1
	padding = 0
	H, W, HH, WW = data.shape[0], data.shape[1], window.shape[0], window.shape[1]
	H_prime = 1 + (H + 2 * padding - HH) / stride
	W_prime = 1 + (W + 2 * padding - WW) / stride
	out = np.zeros((H_prime * W_prime, window.size))

	x_pad = data

	ind_l = 0
	for k in xrange(0,x_pad.shape[0]-HH+1,stride):
	    for l in xrange(0,x_pad.shape[1]-WW+1,stride):
	    	temp = x_pad[k:k+HH,l:l+WW] * window
	    	out[ind_l,:] = np.reshape(temp, [-1, temp.size], order='F')
	    	ind_l += 1

	out = np.ceil(np.round_(out.tolist(), decimals=3))
	return out, W_prime


def set_window():
	# Can be tuned as well
	# Sliding window size
	n = 2
	window = np.ones((n, n))

	return window


# Calculates the lowest frequency sub-band of the image using Haar j-level DWT
def low_subband(image, j):
	# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = image
		
	for i in xrange(j):
		coeffs = pywt.dwt2(gray, 'haar')
		cA, (cH, cV, cD) = coeffs
		gray = cA

	return gray


def dct_qcd(x):
	length = int(np.sqrt(x.shape[1]))

	y = fftpack.dct(x, axis=1)
	np.sort(y, axis=1)
	z = y[0:length,:]
	return z


# [[  2.   2.   2.   2.]
#  [  2.   2.   8.  13.]
#  [  8.  13.  19.  10.]
#  [ 19.  10.   8.   8.]
#  [  2.  11.   2.   9.]
#  [  2.   9.  13.   2.]
#  [ 13.   2.  10.   2.]
#  [ 10.   2.   8.  16.]
#  [ 11.  12.   9.  10.]
#  [  9.  10.   2.   2.]
#  [  2.   2.   2.   2.]
#  [  2.   2.  16.   4.]]


def lex_order(matrix):
	mat = deepcopy(matrix)
	k = mat.shape[0]
	mat_data = {}
	for i in xrange(1,k+1):
		mat_data[i] = list(mat[i-1])

	orig_data = mat_data
	mat_data = OrderedDict(sorted(mat_data.items(), key=itemgetter(1)))

	return orig_data, mat_data


def calc_shift_vec(data, W_prime):
	key_list = [key for key in data]
	shift_vec = {}
	k = len(data)
	for i in xrange(1,k):
		key = key_list[i-1]
		x1 = key / W_prime + 1
		y1 = key % W_prime
		if not y1:
			x1 -= 1
			y1 = W_prime
		
		key = key_list[i]
		x2 = key / W_prime + 1
		y2 = key % W_prime
		if not y2:
			x2 -= 1
			y2 = W_prime
		
		shift_vec[i] = (x1-x2, y1-y2)

	return shift_vec

def main():
	# img = cv2.imread('horse_blur.jpg')
	# plt.imshow(gray),plt.show()
	img = np.array([[1, 1, 1, 1, 3, 6, 10, 4, 3],
				[1, 1, 1, 1, 4, 2, 12, 11, 5],
				[1, 1, 1, 1, 9, 4, 1, 9, 2],
				[1, 1, 1, 1, 5, 8, 2, 7, 6],
				[6, 4, 5, 6, 1, 1, 1, 1, 9],
				[2, 10, 3, 4, 1, 1, 1, 1, 7],
				[3, 5, 4, 1, 1, 1, 1, 1, 1],
				[7, 9, 7, 8, 1, 1, 1, 1, 3]])

	subband_matrix = low_subband(img, 1)
	window = set_window()
	block_matrix, W_prime = sliding_window(subband_matrix, window)

	reduced_matrix = dct_qcd(block_matrix)
	block_data, sorted_data = lex_order(block_matrix)

	# for key in sorted_data:
	# 	print sorted_data[key], key

	shift_vec = calc_shift_vec(sorted_data, W_prime)

	print shift_vec

if __name__ == "__main__":
	main()


