'''
Created on 11-11-2015

@author: tomek
'''
import numpy as np
import cv2
from cv2 import *
from random import randint
from Xlib import display
import math

def calculatemodel(s):
    x = []
    y = []
    for i in range(len(s)):
        xtmp, ytmp = s[i]
        x.append(xtmp)
        y.append(ytmp)

    sumx = 0
    sumy = 0
    for i in range(len(x)):
        sumx += x[i]
        sumy += y[i]
    meanx = sumx/len(x)
    meany = sumy/len(y)
    centerX = int(meanx)
    centerY = int(meany)
    srodek = (centerX, centerY)
    
    sumdists = 0
    for i in range(len(s)):
        sumdists += calculatedistance(srodek, s[i])  
    meandist = sumdists/len(s)
    r = int(meandist)
    return ((centerX, centerY), r)

def calculatedistance(a, b):
    x1, y1 = a
    x2, y2 = b
    dx = x1-x2
    dy = y1-y2
    return math.sqrt(dx*dx+dy*dy)

def calculateerror(model, data):
    srodek, radius = model
    distance = calculatedistance(srodek, data)
    return math.fabs(radius - distance)
 
def ranzac(points):
    #D: x, y = thresh.shape[0/1], r =4-15, n=100
    if len(points) == 0:
        return ((0,0), 0)
    maxerror = 3
    maxR = 4
    minR = 1
    maxiterations = 10
    n = 10
    bestmodel = ((0,0),0)
    bestscore = 0
    for i in range(100):
        model = ((0,0),0)
        iterations = 0
        radius = maxR+100
        while (iterations < maxiterations) & ((model == ((0,0),0)) | (radius>maxR) | (radius<minR)):
            iterations += 1
            s = []
            for r in range(n):
                rand = randint(0, len(points)-1)
                s.append(points[rand])  
            #rozszerzyc calculatemodel na wiecej punktow, zwiekszyc n
            model = calculatemodel(s)   
            _, radius = model
        score = 0
        for d in range(len(points)):
            error = calculateerror(model, points[d])
            if error < maxerror:
                score += 1
        if score > bestscore:
            bestscore = score
            bestmodel = model
    return bestmodel    
            
        

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

d = display.Display()              
def setCursorPosition(x, y):  
    s = d.screen()
    root = s.root
    root.warp_pointer(x,y)
    d.sync()

def capture():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("original")
    cv2.namedWindow('oko_gray')
    cv2.namedWindow('oko_punkty')
    cv2.namedWindow('oko_thresh')
    cv2.namedWindow('oko_kolko')
    
    
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
        frame = cv2.flip(frame, 1)
        cv2.imshow("original", frame)
        cv2.moveWindow("original", 10, 20)
    
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        oko_color = frame[y-h/2:y+h/2, x-w/2:x+w/2]
        oko_gray = cv2.cvtColor(oko_color, cv2.COLOR_BGR2GRAY)
        value = (35, 35)
        blurred = cv2.GaussianBlur(oko_gray, value, 2)
        _, oko_thresh = cv2.threshold(blurred, 55, 255, cv2.ADAPTIVE_THRESH_MEAN_C)
        points = getBorderPoints(oko_thresh)
        oko_punkty = oko_color.copy()
        drawPoints(oko_punkty, points)
        
        
        srodek, rCircle = ranzac(points)
        xCircle, yCircle = srodek
        oko_kolko = oko_color.copy() 
        cv2.circle(oko_kolko,(xCircle,yCircle),rCircle,(255,0,0),1)
        
        skokKursoraPoziomy, skokKursoraPionowy = (10, 10)
        setCursorPosition(round(xCircle*skokKursoraPoziomy), round(yCircle*skokKursoraPionowy))


        # Display the resulting frame
        cv2.moveWindow('oko_gray',650, 20)
        cv2.imshow('oko_gray',oko_gray)
        cv2.moveWindow('oko_punkty',750, 20)
        cv2.imshow('oko_punkty',oko_punkty)
        cv2.moveWindow('oko_thresh',750, 200)
        cv2.imshow('oko_thresh',oko_thresh)
        cv2.moveWindow('oko_kolko',750, 100)
        cv2.imshow('oko_kolko',oko_kolko)
        #cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture()