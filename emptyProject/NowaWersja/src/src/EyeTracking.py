'''
Created on 03-11-2015

@author: tomek
'''
import numpy as np
import cv2
import video
from methods import *
import Tkinter as tk
from Xlib import display
from menu import *
from numpy import sqrt, real, math, double, sinc
from cmath import atan, cos, sin, cosh
from math import atan2


root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
poleSterowaniaWidth = 30
poleSterowaniaHeight = 30
skokKursoraPoziomy = round(screen_width/poleSterowaniaWidth)
skokKursoraPionowy = round(screen_height/poleSterowaniaHeight)


poleSterowaniaResolution = (poleSterowaniaWidth, poleSterowaniaHeight)
poleWycinane = (poleSterowaniaWidth+12, poleSterowaniaHeight+12) # dookola ramki w ktorej oceniam pomozenie mam bufor na granicy zeby jak zrenica wyjdzie poza
#pole nie wywalalo bledu (ponizej widac ze potrzeba z 5 kratek zapasu)
threshold_value = 70

  
d = display.Display()              
def setCursorPosition(x, y):  
    s = d.screen()
    root = s.root
    root.warp_pointer(x,y)
    d.sync()
      
def moveCursor(alfa):
    speed = 10
    d = display.Display().screen().root.query_pointer()._data
    obecnyx = d["root_x"]
    obecnyy = d["root_y"]
    ruchx = round(real(cos(alfa))*speed)
    ruchy = -round(real(sin(alfa))*speed)
    setCursorPosition(obecnyx+ruchx, obecnyy+ruchy)
    

if __name__ == '__main__':
    #showMenu()

    eye_cascade = cv2.CascadeClassifier('/home/tomek/WORKSPACES!!/Systemy wizyjne/EyeTracking/src/xmle/haarcascade_eye.xml')
    
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
      
      
    cv2.namedWindow('image')
    def nothing(*arg):
        pass
    cv2.createTrackbar('threshold_value', 'image', threshold_value, 255, nothing)
      
    cap = video.create_capture(video_src)
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray)
    x,y,w,h = eyes[0] 
    x=x+w/2
    y=y+h/2
    #teraz x i y sa srodkiem prostokata wycietego jako oko przez detektor oczu
    w, h = poleWycinane
    a = w/2
    b = h/2
    wyciete_oko_img = img[y-h/2:y+h/2, x-w/2:x+w/2]
    oko_gray = cv2.cvtColor(wyciete_oko_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred = cv2.GaussianBlur(oko_gray, value, 2)
    blurred = cv2.flip(blurred,1)

    _, thresh1 = cv2.threshold(blurred, threshold_value, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C)#+cv2.THRESH_OTSU)
    _, contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
        cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
    #potrzebne do normalizacji jasnosci
    _, first_img = cap.read()
    srednia_jasnosc = first_img.mean()
    
    
    
    while True:
        _, img = cap.read()
        #normalizuje jasnosc
        roznica_jasnosci = first_img.mean() - img.mean()
        jedynki = np.ones_like(img) #tablica jedynek
        deltki = cv2.multiply(jedynki,np.array([roznica_jasnosci])) # tablica o wymiarach obrazka wypelniona wartosciami  = roznica_jasnosci
        img = cv2.add(img, deltki) 
        #koniec normalizacji jasnosci
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       
        wyciete_oko_img = img[y-h/2:y+h/2, x-w/2:x+w/2] 

        oko_gray = cv2.cvtColor(wyciete_oko_img, cv2.COLOR_BGR2GRAY)
        value = (35, 35)
        blurred = cv2.GaussianBlur(oko_gray, value, 2)
        blurred = cv2.flip(blurred,1)
        cv2.imshow("gaus", blurred)
        cv2.moveWindow("gaus", 800, 100)
        
        cv2.setTrackbarPos('threshold_value', 'image', threshold_value)
        _, thresh1 = cv2.threshold(blurred, threshold_value, 255,
                               cv2.ADAPTIVE_THRESH_MEAN_C)
     
        cv2.imshow('thresh',thresh1)

        new_a, new_b = a, b

        global threshold_value
        okolicaOkaBlurred = blurred[new_b-5:new_b+5, new_a-5:new_a+5]

        _, okolicaOkaOdswiezona = cv2.threshold(okolicaOkaBlurred, threshold_value, 255,
                               cv2.ADAPTIVE_THRESH_MEAN_C)
        sredniaJasnosc, _, __, ___ = cv2.mean(okolicaOkaOdswiezona)
        tmp_threshold_value = threshold_value
        if sredniaJasnosc<100:
            while sredniaJasnosc<120:
                if tmp_threshold_value >= 0:
                    tmp_threshold_value-=1
                _, okolicaOkaOdswiezona = cv2.threshold(okolicaOkaBlurred, tmp_threshold_value, 255,
                               cv2.ADAPTIVE_THRESH_MEAN_C)
                cv2.imshow("okolicaokaodswiezona", okolicaOkaOdswiezona)
                sredniaJasnosc, _, __, ___ = cv2.mean(okolicaOkaOdswiezona)
        if sredniaJasnosc>245:
            while sredniaJasnosc>120:
                if tmp_threshold_value <= 255:
                    tmp_threshold_value+=1
                _, okolicaOkaOdswiezona = cv2.threshold(okolicaOkaBlurred, tmp_threshold_value, 255,
                               cv2.ADAPTIVE_THRESH_MEAN_C)
                sredniaJasnosc, _, __, ___ = cv2.mean(okolicaOkaOdswiezona)
        threshold_value = tmp_threshold_value       
        
        radius = 7
        new_a,new_b, px, py = pupil_position(thresh1,(a,b), radius)
        #rysuje niebieska kropke z pozycja zrenicy
        cv2.rectangle(img,(x+w/2-new_a,y-h/2+new_b),(x+w/2-new_a-1,y-h/2+new_b+1),(255,0,0),2)#plus w, minus przy a :bo robie flip = obrot prawo lewo = lustrzane odbicie
        #rysuje biala kropke wewnatrz kolka
        cv2.rectangle(img,(x+w/2-px,y-h/2+py),(x+w/2-px-1,y-h/2+py+1),(255,255,255),2)#plus w, minus przy a :bo robie flip = obrot prawo lewo = lustrzane odbicie

        a, b = (new_a, new_b) #a, b to polozenie wzgledem ramki wycietej
        if odleglosc((w/2, h/2), (a, b)) > radius:
            #print "x, y =",(w/2,h/2),' a,b=',(a,b)
            alfa = ustalAlfa((w/2,h/2), (a, b))
            if (alfa<math.pi/4) | (alfa>=(2*math.pi-math.pi/4)):
                alfa = 0
            if (alfa>=math.pi/4) & (alfa<(math.pi-math.pi/4)):
                alfa = math.pi/2
            if (alfa>=(math.pi-math.pi/4)) & (alfa<(math.pi+math.pi/4)):
                alfa = math.pi
            if (alfa>=(math.pi+math.pi/4)) & (alfa<(2*math.pi-math.pi/4)):
                alfa = math.pi+math.pi/2
            moveCursor(alfa)
        #if menu.isModeOn():
       
        
        cv2.moveWindow("thresh", 800,0)
        cv2.rectangle(img,(x-w/2,y-h/2),(x+w/2,y+h/2),(0,255,0),2)
        #ramka po ktorej moge sie poruszac
        wPolaSterowania, hPolaSterowania = poleSterowaniaResolution
        cv2.rectangle(img, (x-wPolaSterowania/2,y-hPolaSterowania/2), (x+wPolaSterowania/2,y+hPolaSterowania/2), (255,0,0),2)
        #koleczko
        cv2.circle(img, (x, y), radius, (0,0,255))
        
        vis = img.copy()
        vis = cv2.flip(vis, 1)
        cv2.imshow('image',vis)
        if 0xFF & cv2.waitKey(5) == 27:
            break
    
    cv2.destroyAllWindows()