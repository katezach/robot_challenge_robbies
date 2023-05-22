import time
import imutils
import cv2
import numpy as np
import picar_4wd as fc
from picamera2 import Picamera2
import sys
import matplotlib.pyplot as plt



# KNOWN_WIDTH = 7.0
KNOWN_WIDTH = 10.0
def find_object(image):
    # convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (9,9), 0) #itan cv2.GaussianBlur(gray, (9, 9), 0)

    edged = cv2.Canny(gray, 110, 150) 

    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)
    

    if np.all(gray == 0) or np.all(edged == 0) or np.all(cnts == 0):
        print("All elements are zeros")
        rect=400
        image0=400
        return rect,image0
        
    c = max(cnts, key = cv2.contourArea)
    M = cv2.moments(c)
    rect= cv2.minAreaRect(c)
    
    if M["m00"]==0: #itan TIPOTA
        print("division element is zeros")
        rect=400
        image0=400
        print('AKIROO')
        return rect,image0
    
    # compute the bounding box of the note region and return it
    return rect, [int(M["m10"] / M["m00"]),int(M["m01"] / M["m00"])]


def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth


def main():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1280, 720)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    total_dist = 200
    
    array = picam2.capture_array()
    image = array[:, array.shape[1]//2-250: array.shape[1]//2+250]
    obj, centre = find_object(image)
    focalLength = 478 * 1.66  #equals to 793.48

    dist = distance_to_camera(KNOWN_WIDTH, focalLength, obj[1][0]) 
    print(dist)
    
    
    while dist > 150:
        dist = distance_to_camera(KNOWN_WIDTH, focalLength, obj[1][0]) 
        if dist<=150:
            break
        sleep_duration = 5/30 
        fc.forward(20) 
        dist=dist-5
        time.sleep(sleep_duration)
        fc.stop()
        time.sleep(1)
        
        array = picam2.capture_array()
        image = array[:, array.shape[1]//2-250: array.shape[1]//2+250]
        obj, centre = find_object(image)
        dist = distance_to_camera(KNOWN_WIDTH, focalLength, obj[1][0])
        
        
        print(dist)
    
    total_dist -= dist
    print(dist)
    sleep_duration = (dist-15)/ 30 

    fc.forward(20)
    time.sleep(sleep_duration)

    # turn right
    fc.turn_right(10)
    time.sleep(0.9)
    
    
    # go straight 30 cm
    fc.forward(20)
    time.sleep(30/30)
    

    # rutn left
    fc.turn_left(10)
    time.sleep(1.1)
    
    # go straight 55 cm
    fc.forward(20)
    time.sleep(55/30)
    total_dist-=55
    
    # run left
    fc.turn_left(10)
    time.sleep(1)
    
    # go straight 30 cm
    fc.forward(20)
    time.sleep(30/30)
    
    # turn right
    fc.turn_right(10)
    time.sleep(1)
    	
    # go straight remaining distance
    fc.forward(20)
    time.sleep((total_dist+15)/30)

    fc.stop()
    

if __name__== '__main__':
    main()
