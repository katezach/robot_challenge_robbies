
import time
import imutils
import cv2
import numpy as np
import picar_4wd as fc
from picamera2 import Picamera2
import sys
import matplotlib.pyplot as plt

KNOWN_WIDTH = 10.0
#KNOWN_WIDTH = 12.0
def find_object(image):
    # convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.GaussianBlur(gray, (9, 9), 0)
    edged = cv2.Canny(gray, 110, 150) #itan 150,150
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key = cv2.contourArea)
    M = cv2.moments(c)
    rect= cv2.minAreaRect(c)
    # compute the bounding box of the note region and return iT
    return cv2.minAreaRect(c), [int(M["m10"] / M["m00"]),int(M["m01"] / M["m00"])]

def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth


def part1():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1280, 720)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    array = picam2.capture_array()
    image = array[:, array.shape[1]//2-250: array.shape[1]//2+250]
    #cv2.imwrite('test_task1.png', image)
    obj, centre = find_object(image)
    
        
    focalLength = 478 * 1.66  #equal to 793.48
    dist = distance_to_camera(KNOWN_WIDTH, focalLength, obj[1][0]) 
    print(dist)
    
    
def part2():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1280, 720)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    
    while True:
        array = picam2.capture_array()
        image = array[:, array.shape[1]//2-250: array.shape[1]//2+250]
        obj, centre = find_object(image)
        focalLength = 478 * 1.66 
        dist = distance_to_camera(KNOWN_WIDTH, focalLength, obj[1][0])
        if dist-2!=0:
            dist = dist - 2 

        if dist > 80 : 
            #part 1
            
    
            box = cv2.cv.BoxPoints(obj) if imutils.is_cv2() else cv2.boxPoints(obj)
            box = np.int0(box)
            
            sleep_duration = 10 /30 

            fc.forward(20) #itan 20
            time.sleep(sleep_duration)
            fc.stop()
            time.sleep(1)

            
        elif dist <= 80: 

            box = cv2.cv.BoxPoints(obj) if imutils.is_cv2() else cv2.boxPoints(obj)
            box = np.int0(box)

            sleep_duration = (dist- 10) / 30
            
            fc.forward(20)
            time.sleep(sleep_duration)
            fc.stop()
            break


def main():
    
    if sys.argv[1] == '1':
        part1()
    elif sys.argv[1] == '2':
        part2()
    else:
        print("Not valid arguments")
        exit(1)

        
if __name__ == '__main__':
    main()
