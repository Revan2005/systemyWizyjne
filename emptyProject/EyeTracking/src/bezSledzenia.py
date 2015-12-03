'''
Created on 16-03-2015

@author: tomek
'''

import numpy as np
import cv2
import video

def black_field(a, b, img):
    #print a, b
    cropped_img = img[b-5:b+5, a-5:a+5]
    cv2.imshow('kropd', cropped_img)
    #print 255-cv2.mean(cropped_img)[0]
    return 255-cv2.mean(cropped_img)[0]

def pupil_position(img):
    #ustawiam polozenie poczatkowe posrodku
    height, width = np.shape(img)
    a, b = width/2, height/2
    #if x<6 | y<6:
    #    pass
    obecnie = black_field(a, b, img)
    prawo=black_field(a+1, b, img)
    lewo=black_field(a-1, b, img)
    gora=black_field(a, b-1, img)
    dol=black_field(a, b+1, img)
    
    while obecnie < max([prawo, lewo, gora, dol]): 
        if prawo > obecnie:
            a+=1
        elif lewo > obecnie:
            a-=1
        elif gora > obecnie:
            b-=1
        elif dol > obecnie:
            b+=1
        obecnie = black_field(a, b, img)
        prawo = black_field(a+1, b, img)
        lewo = black_field(a-1, b, img)
        gora = black_field(a, b-1, img)
        dol = black_field(a, b+1, img)
    return (a, b)
    #cv2.imshow("thresholded_ze_sledzeniem", img)
    #cv2.rectangle(img,(a,b),(a+10,b+10),(255,0,0),2)
                
   

if __name__ == '__main__':

    eye_cascade = cv2.CascadeClassifier('/home/tomek/workspace/systemyWizyjne/xmle/haarcascade_eye.xml')

    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
      
    cv2.namedWindow('image')
    def nothing(*arg):
        print threshold_value
    cv2.createTrackbar('threshold_value', 'image', 70, 255, nothing)
      
    cap = video.create_capture(video_src)
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray)
    x,y,w,h = eyes[0]
    #powiekszam ramke do analizy zeby w funkcji 
    #pupil_position moc sprawdzic caly zaznaczony przez x,y,w,h obszar
    #jako ze licze srednie zaczernienie w kwadracie 10*10 to zeby nie wyjechac
    #za obrazek (co mialoby wplyw na srednia chyba) poszerzam troche ramke
    #do obliczen
    #wyciete_oko_img = img[y-11:y+h+22, x-11:x+w+22] 
    x-=44
    y-=44
    w+=88
    h+=88
    #x,y,w,h = (x-11, y-11, w+22, h+22)

    wyciete_oko_img = img[y:y+h, x:x+w]
    #print h
    oko_gray = cv2.cvtColor(wyciete_oko_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred = cv2.GaussianBlur(oko_gray, value, 2)
    blurred = cv2.flip(blurred,1)
    #cv2.imshow("gaus", blurred)
    #cv2.moveWindow("gaus", 800, 100)
    _, thresh1 = cv2.threshold(blurred, 70, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C)#+cv2.THRESH_OTSU)
    #thresh1 = cv2.flip(thresh1, 1)
    #cv2.imshow('thresh',thresh1)
    #cv2.moveWindow("thresh", 800,0)
    
    '''
    #sledzenie
    # setup initial location of window
    x2,y2,w2,h2 = 0,0,50,50  # simply hardcoded the values
    track_window = (x2,y2,w2,h2)
    
    # set up the ROI for tracking
    roi = img[y2:y2+h2, x2:x2+w2]
    hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
    roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
    cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
 
    # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
    term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
    #sledzenie
    '''
    
    
    
    while True:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        '''
        #sledzenie
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x2,y2,w2,h2 = track_window
        img2 = cv2.rectangle(img, (x2,y2), (x2+w2,y2+h2), 255,2)
        #cv2.imshow('img2',img2)
        #sledzenie
        '''
        wyciete_oko_img = img[y:y+h, x:x+w] 
        oko_gray = cv2.cvtColor(wyciete_oko_img, cv2.COLOR_BGR2GRAY)
        value = (35, 35)
        blurred = cv2.GaussianBlur(oko_gray, value, 2)
        blurred = cv2.flip(blurred,1)
        cv2.imshow("gaus", blurred)
        cv2.moveWindow("gaus", 800, 100)
        
        threshold_value = cv2.getTrackbarPos('threshold_value', 'image')
        _, thresh1 = cv2.threshold(blurred, threshold_value, 255,
                               cv2.ADAPTIVE_THRESH_MEAN_C)
        #_, contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
        #    cv2.CHAIN_APPROX_NONE)
        #cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
        #thresh1 = cv2.flip(thresh1, 1)
        cv2.imshow('thresh',thresh1)
        #moja funkcja
        a,b = pupil_position(thresh1)
        
        cv2.rectangle(img,(x+w-a,y+b),(x+w-a-1,y+b+1),(255,0,0),2)#plus w, minus przy a :bo robie flip = obrot prawo lewo = lustrzane odbicie
        
        cv2.moveWindow("thresh", 800,0)
        if eyes.size<2:
            eyes = eye_cascade.detectMultiScale(gray)
        if eyes.size>1:
            eyes = eyes[:1]
        x,y,w,h = eyes[0]
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        #powiekszam ramke do analizy zeby w funkcji 
        #pupil_position moc sprawdzic caly zaznaczony przez x,y,w,h obszar
        #jako ze licze srednie zaczernienie w kwadracie 10*10 to zeby nie wyjechac
        #za obrazek (co mialoby wplyw na srednia chyba) poszerzam troche ramke
        #do obliczen
        #wyciete_oko_img = img[y-11:y+h+22, x-11:x+w+22] 
        x-=44
        y-=44
        w+=88
        h+=88
        #for (x,y,w,h) in eyes:
        #    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        #print eyes.__class__
        #print eyes[0][0]
                
        vis = img.copy()
        vis = cv2.flip(vis, 1)
        #print 'petla'
        cv2.imshow('image',vis)
        if 0xFF & cv2.waitKey(5) == 27:
            break
 
    cv2.destroyAllWindows()