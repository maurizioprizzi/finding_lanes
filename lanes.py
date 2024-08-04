# importando a biblioteca OpenCV
import cv2
import numpy as np

# return the image as a multidimensional numpy array
image = cv2.imread('test_image.jpg')

# make a copy of the image
lane_image = np.copy(image)
# make a copy of the gray scale image
gray = cv2.cvtColor(lane_image, cv2.COLOR_BGR2GRAY)
# apply GaussianBlur filter to the image to reduce noise
blur = cv2.GaussianBlur(gray, (5, 5), 0) # 5*5 kernel, deviation of 0

cv2.imshow('result', blur)
cv2.waitKey(0)