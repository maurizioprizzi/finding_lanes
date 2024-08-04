# importando a biblioteca OpenCV
import cv2
import numpy as np

# return the image as a multidimensional numpy array
image = cv2.imread('test_image.jpg')

# make a copy of the image
lane_image = np.copy(image)

gray = cv2.cvtColor(lane_image, cv2.COLOR_BGR2GRAY)

cv2.imshow('result', gray)
cv2.waitKey(0)

# 