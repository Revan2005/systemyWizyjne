'''
Created on 11-11-2015

@author: tomek
'''
import numpy as np
import cv2
from cv2 import *

def starburst(img, (x, y)):
    thresh = 100
    delta = 0
    while delta<thresh:
        delta = img[x][y] -img[x+1][y] 
        x+=1
    cv2.circle(img, (x, y), 1, (0,0,0))
    return img

def capture():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('modified')
    cv2.namedWindow("original")
    
    eye_cascade = cv2.CascadeClassifier('/home/tomek/workspace/systemyWizyjne/xmle/haarcascade_eye.xml')
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray)
    x,y,w,h = eyes[0] 
    x=x+w/2
    y=y+h/2
    #teraz x i y sa srodkiem prostokata wycietego jako oko przez detektor oczu

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        cv2.imshow("original", frame)
        cv2.moveWindow("original", 10, 20)
        
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        wyciete_oko = frame[y-h/2:y+h/2, x-w/2:x+w/2]
        oko_gray = cv2.cvtColor(wyciete_oko, cv2.COLOR_BGR2GRAY)
        
        oko_gray = starburst(oko_gray, (h/2, w/2))

        # Display the resulting frame
        cv2.moveWindow('modified',650, 20)
        cv2.imshow('modified',oko_gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture()