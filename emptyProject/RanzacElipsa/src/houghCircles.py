'''
Created on 11-11-2015

@author: tomek
'''
import numpy as np
import cv2
from cv2 import *

def capture():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('modified')
    cv2.namedWindow("original")
    first =10
    second =10
    third =10
    fourth =10
    def nothing(*arg):
            pass
    cv2.createTrackbar('first', 'modified', first, 255, nothing)
    cv2.setTrackbarPos('first', 'modified', first)
    cv2.createTrackbar('second', 'modified', second, 255, nothing)
    cv2.setTrackbarPos('second', 'modified', second)
    cv2.createTrackbar('third', 'modified', third, 255, nothing)
    cv2.setTrackbarPos('third', 'modified', third)
    cv2.createTrackbar('fourth', 'modified', fourth, 255, nothing)
    cv2.setTrackbarPos('fourth', 'modified', fourth)
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        cv2.imshow("original", frame)
        cv2.moveWindow("original", 10, 20)
        
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh1 = cv2.threshold(gray, 150, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
       
        
        first = cv2.getTrackbarPos('first', 'modified')
        second = cv2.getTrackbarPos('second', 'modified')
        third = cv2.getTrackbarPos('third', 'modified')
        fourth = cv2.getTrackbarPos('fourth', 'modified')
        circles = cv2.HoughCircles(gray,cv.CV_HOUGH_GRADIENT, first,second, param1=third,param2=fourth,minRadius=2,maxRadius=15)
        for c in circles[0,:]:
            # draw the outer circle
            cv2.circle(gray,(c[0],c[1]),c[2],(255,0,0),1)
            # draw the center of the circle
            cv2.circle(gray,(c[0],c[1]),2,(0,0,255),1)
            
        

        # Display the resulting frame
        
        cv2.moveWindow('modified',650, 20)
        cv2.imshow('modified',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture()