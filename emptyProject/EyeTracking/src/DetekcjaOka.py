'''
Created on 16-03-2015

@author: tomek
'''

import numpy as np
import cv2
import video

if __name__ == '__main__':

    #face_cascade = cv2.CascadeClassifier("/home/tomek/WORKSPACES!!/Systemy wizyjne/EyeTracking/src/xmle/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier('/home/tomek/workspace/systemyWizyjne/xmle/haarcascade_eye.xml')

    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    #cv2.namedWindow("siemanko")
    cap = video.create_capture(video_src)
    #licznik = 0
    
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray)
    
    # setup initial location of window
    c,r,w,h = eyes[0]  # simply hardcoded the values
    #track_window = (c,r,w,h)
    track_window = (c,r,w,h)

    # set up the ROI for tracking
    roi = img[r:r+h, c:c+w]
    hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
    roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
    cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

    # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
    term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

    
    while True:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print img.size

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x,y,w,h = track_window
        img2 = cv2.rectangle(img, (x,y), (x+w,y+h), 255,2)
        #cv2.imshow('img2',img2)

        wyciete_oko_img = img[y:y+h, x:x+w]
        grey = cv2.cvtColor(wyciete_oko_img, cv2.COLOR_BGR2GRAY)
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV)#+cv2.THRESH_OTSU)

        cv2.imshow('thresh1',thresh1)
        #if eyes.size<2:
        #    eyes = eye_cascade.detectMultiScale(gray)
        #if eyes.size>1:
        #    eyes = eyes[:1]
        #for (ex,ey,ew,eh) in eyes:
        #    cv2.rectangle(img2,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        #print eyes.__class__
        #print eyes[0][0]
                
        vis = img2.copy()
        #print 'petla'
        cv2.imshow('image',vis)
        if 0xFF & cv2.waitKey(5) == 27:
            break
 
    cv2.destroyAllWindows()