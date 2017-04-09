# -*- coding:utf-8 -*-
import numpy as np   
import cv2 

redLower = np.array([150,100,100])  
redUpper = np.array([180,255,255]) 

camera = cv2.VideoCapture(0)  

def center(): 
    (ret, f) = camera.read()  

    if not ret:  
        print 'No Camera'  
        
    center = (0,0)
    
    frame = cv2.flip(f,1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  

    mask = cv2.inRange(hsv, redLower, redUpper)  

    mask = cv2.erode(mask, None, iterations=2)  

    mask = cv2.dilate(mask, None, iterations=2)  

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  

    if len(cnts) > 0:  

        c = max(cnts, key = cv2.contourArea)  

        M = cv2.moments(c)  

        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))   
    
    return int(center[0] * 2.4), int(center[1] * 1.8)