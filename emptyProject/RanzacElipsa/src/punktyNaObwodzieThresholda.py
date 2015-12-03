'''
Created on 11-11-2015

@author: tomek
'''
import numpy as np
import cv2
from cv2 import *

def getBorderPoints(thresh):
    points = []
    for x in xrange(thresh.shape[0]-1):
        for y in xrange(thresh.shape[1]-1):
            if thresh[x][y] != thresh[x+1][y+1]:
                points.append((y,x))
    return points

def drawPoints(img, points):
    for (a, b) in points:
        cv2.circle(img,(a,b),1,(255,0,255),1)

def capture():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("original")
    cv2.namedWindow('oko_gray')
    cv2.namedWindow('oko_color')
    cv2.namedWindow('oko_thresh')
    
    
    eye_cascade = cv2.CascadeClassifier('/home/tomek/workspace/systemyWizyjne/xmle/haarcascade_eye.xml')
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray)
    x,y,w,h = eyes[0] 
    x=x+w/2
    y=y+h/2
    #teraz x i y sa srodkiem prostokata wycietego jako oko przez detektor oczu

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        cv2.imshow("original", frame)
        cv2.moveWindow("original", 10, 20)
    
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        oko_color = frame[y-h/2:y+h/2, x-w/2:x+w/2]
        oko_gray = cv2.cvtColor(oko_color, cv2.COLOR_BGR2GRAY)
        value = (35, 35)
        blurred = cv2.GaussianBlur(oko_gray, value, 2)
        _, oko_thresh = cv2.threshold(blurred, 100, 255, cv2.ADAPTIVE_THRESH_MEAN_C)
        points = getBorderPoints(oko_thresh)
        drawPoints(oko_color, points)
    


        # Display the resulting frame
        cv2.moveWindow('oko_gray',650, 20)
        cv2.imshow('oko_gray',oko_gray)
        cv2.moveWindow('oko_color',750, 20)
        cv2.imshow('oko_color',oko_color)
        cv2.moveWindow('oko_thresh',750, 200)
        cv2.imshow('oko_thresh',oko_thresh)
        #cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture()