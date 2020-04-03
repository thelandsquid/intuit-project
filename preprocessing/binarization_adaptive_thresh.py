# preprocessMethod.py
# Runs a preprocessing method against the intermediate dataset and outputs them
# into the "preprocessed" folder

# Binarization - Adaptive Thresholding
# Adaptive thresholding is used instead of Simple thresholding because the image may have different lighting conditions
# in different areas.
# https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html

import sys
import cv2 as cv
import numpy as np
import time
import os
from matplotlib import pyplot as plt

def main(image_path):
    startTime = int(round(time.time() * 1000))
    # Open the image file in greyscale (0)
    tempImage = cv.imread(image_path, 0)
    # Blurring (averaging)/Smoothing the image to reduce noise
    # Maybe not use this??
    tempImage = cv.medianBlur(tempImage, 5)
    # Do the preprocessing stuff here
    # Apply Adaptive thresholding method - Guassian threshold
    tempImage = cv.adaptiveThreshold(tempImage, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

    cv.imwrite("temp.jpg", tempImage)

    return int(round(time.time() * 1000)) - startTime

if __name__ == "__main__":
    main(sys.argv[1])