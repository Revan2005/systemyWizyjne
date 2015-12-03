'''
Created on 16-03-2015

@author: tomek
'''

import numpy as np
import cv2
import video

if __name__ == '__main__':

    #face_cascade = cv2.CascadeClassifier("/home/tomek/WORKSPACES!!/Systemy wizyjne/EyeTracking/src/xmle/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier('/home/tomek/WORKSPACES!!/Systemy wizyjne/EyeTracking/src/xmle/haarcascade_eye.xml')

    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    #cv2.namedWindow("siemanko")
    cap = video.create_capture(video_src)
    licznik = 0
    
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray)
    while True:
        #licznik+=1
        #licznik%=10
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        #for (x,y,w,h) in faces:
        #    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        #    roi_gray = gray[y:y+h, x:x+w]
        #    roi_color = img[y:y+h, x:x+w]

        if eyes.size<2:
            eyes = eye_cascade.detectMultiScale(gray)
        if eyes.size>2:
            eyes = eyes[:2]
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        #print eyes.__class__
        print eyes[0][0]
                
        vis = img.copy()
        #print 'petla'
        cv2.imshow('image',vis)
        if 0xFF & cv2.waitKey(5) == 27:
            break
 
    cv2.destroyAllWindows()