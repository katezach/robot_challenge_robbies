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
    gray = cv2.GaussianBlur(gray, (9,9), 0)
    edged = cv2.Canny(gray, 110, 150) 
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if np.all(gray == 0) or np.all(edged == 0) or np.all(cnts == 0):
        print("All elements are zeros (no object detected) continue your task")
        rect=400
        image0=400
        return rect,image0
    else: 
        print('OK continue')
    c = max(cnts, key = cv2.contourArea)
    M = cv2.moments(c)
        
    rect= cv2.minAreaRect(c)
    
    #if no object detected return 0
    #for not having error if the denominator M["m00"] is zero:
    if M["m00"]==0: 
        return rect, [int(0),int(0)]
    
    # compute the bounding box of the note region and return it
    return rect, [int(M["m10"] / M["m00"]),int(M["m01"] / M["m00"])]

def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth


def part1():
    global picam2
    array = picam2.capture_array()
    image = array[:, array.shape[1]//2-250: array.shape[1]//2+250]
    obj, centre = find_object(image)
    if obj==400 or centre==400:
        return 400
    focalLength = 478 * 1.66 #equals to 793.48
    dist = distance_to_camera(KNOWN_WIDTH, focalLength, obj[1][0])
    print('part1',dist)
    
    return dist

            
def part2():
    global picam2
    indz=0
    while True:
        array = picam2.capture_array()
        image = array[:, array.shape[1]//2-250: array.shape[1]//2+250]
        obj, centre = find_object(image)
        focalLength = 478 * 1.66  #equals to 793.48
        dist = distance_to_camera(KNOWN_WIDTH, focalLength, obj[1][0]) 
        if dist-2!=0:
            dist = dist - 2 
        print('part2',dist)
        if dist > 90 and dist<150 : #to take photo and check again for more accuracy
            sleep_duration = 10 /30 
            fc.forward(20) #itan 20
            time.sleep(sleep_duration)
            fc.stop()
            time.sleep(1)
        elif dist <= 90: #go to the object
             
            sleep_duration = (dist-10)/ 30
            
            fc.forward(20) #itan 20
            time.sleep(sleep_duration)
            fc.stop()
            break
        
        #because when the object is more than 150 cm away it is detected from
        #bigger distance so the car needs to turn a little left and then go straight to reach it
        elif dist >=150 : #go to the object
            
            fc.turn_left(20)
            time.sleep(5/30)
            
            sleep_duration = dist/30 
            fc.forward(20) 
            time.sleep(sleep_duration)
            
            
            fc.stop()
            time.sleep(1)
            break
        


picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()



cm_restr=250 #250x250 box
distance=0
a=0
object_found=False
while object_found==False:
    if a==0: #for checking only one time the front line
        a=1
        distance = part1()
        if distance<=cm_restr:
            object_found=True
            part2() #if robot finds an object it goes to it
            break
    #turn right 90 degrees
    fc.turn_right(10)
    time.sleep(0.9)
    #stop
    fc.stop()
    time.sleep(1)
    #calculate distance on the right line
    distance = part1()
    if distance<=cm_restr:
        object_found=True
        part2()
        break
    #if the object is not found:
   
    
    fc.turn_left(10)  #turn 90 degrees to the left
    time.sleep(0.9) 
    
    fc.forward(5) #go straight around 7 cms and do again the same loop
    time.sleep(1) 
    #stop
    fc.stop()
fc.stop()
time.sleep(5)
