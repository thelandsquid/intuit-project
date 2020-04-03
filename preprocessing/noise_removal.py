import sys
import cv2 as cv
import numpy as np
import time
import os
from matplotlib import pyplot as plt

def main(image_path):
    startTime = int(round(time.time() * 1000))
    # Open the image file in greyscale (0)
    tempImage = cv.imread(image_path)

    # Do the preprocessing stuff here
    tempImage = cv.fastNlMeansDenoisingColored(tempImage, None, 10, 10, 7, 21)

    cv.imwrite("temp.jpg", tempImage)

    return int(round(time.time() * 1000)) - startTime

if __name__ == "__main__":
    main(sys.argv[1])