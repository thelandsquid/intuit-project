# Alter this file to choose what preprocessing functions to use
import time
import sys
from .binarization_adaptive_thresh import main as bat
from .noise_removal import main as noise_rem

def main(image_path):
    startTime = int(round(time.time() * 1000))
    # Place preprocessing steps in between comments
    noise_rem(image_path)
    ###
    return int(round(time.time() * 1000)) - startTime

if __name__ == "__main__":
    main(sys.argv[1])