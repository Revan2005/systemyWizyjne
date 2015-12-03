'''
Created on 16-03-2015

@author: tomek
'''
import numpy as np
import cv2
import video
import Tkinter as tk
from Xlib import display
from menu import *
from removeEyebrow import *


root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
poleSterowaniaWidth = 80
poleSterowaniaHeight = 45
skokKursoraPoziomy = round(screen_width/poleSterowaniaWidth)
skokKursoraPionowy = round(screen_height/poleSterowaniaHeight)


poleSterowaniaResolution = (poleSterowaniaWidth, poleSterowaniaHeight)
poleWycinane = (poleSterowaniaWidth+12, poleSterowaniaHeight+12) # dookola ramki w ktorej oceniam pomozenie mam bufor na granicy zeby jak zrenica wyjdzie poza
#pole nie wywalalo bledu (ponizej widac ze potrzeba z 5 kratek zapasu)
threshold_value = 70

def black_field(a, b, img):
    #print a, b
    #print b-5, b+5, a-5, b+5
    cropped_img = img[b-5:b+5, a-5:a+5]
    cv2.imshow('kropd', cropped_img)
    #print 255-cv2.mean(cropped_img)[0]
    return 255-cv2.mean(cropped_img)[0]


def pupil_position(img,(a,b)):
    height, width = np.shape(img)
    maxOdchyleniePrawoLewo, maxOdchylenieGoraDol = poleSterowaniaResolution#(width-12, height-12) #12 to bufor zeby nie wychodzilo za zakres jak wywoluje blac field (tam dodaje odejmuje 5 pikseli wiec na wszelki wypadek dalem 6 bufor /ramke wokol) 
   
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
        '''
        if abs(a-width/2)>maxOdchyleniePrawoLewo/2: 
            a, b = width/2, height/2
            print 'pozazakresem'
        if abs(b-height/2)>maxOdchylenieGoraDol/2:  
            a, b = width/2, height/2
            print 'pozazakresem'
        '''
        #rogi
        #print "a-width/2:", a-width/2, "maxOdchyleniePrawoLewo/2:", maxOdchyleniePrawoLewo/2, "b-height/2:", b-height/2, "maxOdchylenieGoraDol/2", maxOdchylenieGoraDol/2
        #print abs(a-width/2)>=maxOdchyleniePrawoLewo/2, abs(b-height/2)>=maxOdchylenieGoraDol/2
        #print (abs(a-width/2)>=maxOdchyleniePrawoLewo/2) & (abs(b-height/2)>=maxOdchylenieGoraDol/2)
        if (abs(a-width/2)>=maxOdchyleniePrawoLewo/2) & (abs(b-height/2)>=maxOdchylenieGoraDol/2):
            #print "sprawdzam rogi"
            if (a-width/2>0) & (b-height/2<0):
                print 'prawy gorny rog'
                prawo = -10
                gora = -10
                a-=1
                b+=1
                obecnie = black_field(a, b, img)
                #prawo = black_field(a+1, b, img)
                lewo = black_field(a-1, b, img)
                #gora = black_field(a, b-1, img)
                dol = black_field(a, b+1, img)
            
            if (a-width/2<0) & (b-height/2<0):
                print "lewy gorny rog"
                lewo = -10
                gora = -10
                a+=1
                b+=1
                obecnie = black_field(a, b, img)
                prawo = black_field(a+1, b, img)
                #lewo = black_field(a-1, b, img)
                #gora = black_field(a, b-1, img)
                dol = black_field(a, b+1, img)
            
            if (a-width/2>0) & (b-height/2>0):
                print "prawy dolny rog"
                prawo = -10
                dol = -10
                a-=1
                b-=1
                obecnie = black_field(a, b, img)
                #prawo = black_field(a+1, b, img)
                lewo = black_field(a-1, b, img)
                gora = black_field(a, b-1, img)
                #dol = black_field(a, b+1, img)
            
            if (a-width/2<0) & (b-height/2>0):
                print "lewy dolny rog"
                lewo = -10
                dol = -10
                a+=1
                b-=1
                obecnie = black_field(a, b, img)
                prawo = black_field(a+1, b, img)
                #lewo = black_field(a-1, b, img)
                gora = black_field(a, b-1, img)
                #dol = black_field(a, b+1, img)
        #krawedzie
        elif abs(a-width/2)>maxOdchyleniePrawoLewo/2:# & abs(b-height/2)<=maxOdchylenieGoraDol/2: 
            #a, b = width/2, height/2
            #print 'pozazakresem prawo lewo'
            if a-width/2>0:
                #print "poza zakresem w prawo",
                #a=width/2+maxOdchyleniePrawoLewo/2-10
                prawo = -10
                a-=1
                obecnie = black_field(a, b, img)
                #prawo = black_field(a+1, b, img)
                lewo = black_field(a-1, b, img)
                gora = black_field(a, b-1, img)
                dol = black_field(a, b+1, img)
                #print a
            if a-width/2<0:
                #print "poza zakresem w lewo",
                #a=width/2+maxOdchyleniePrawoLewo/2-10
                lewo = -10
                a+=1
                obecnie = black_field(a, b, img)
                prawo = black_field(a+1, b, img)
                #lewo = black_field(a-1, b, img)
                gora = black_field(a, b-1, img)
                dol = black_field(a, b+1, img)
                #print a
        elif abs(b-height/2)>maxOdchylenieGoraDol/2:# & abs(b-height/2)<=maxOdchylenieGoraDol/2: 
        #print 'pozazakresem gora dol'
            if b-height/2>0:
                #print "poza zakresem w dol, h: ",
                #a=width/2+maxOdchyleniePrawoLewo/2-10
                dol = -10
                b-=1
                obecnie = black_field(a, b, img)
                prawo = black_field(a+1, b, img)
                lewo = black_field(a-1, b, img)
                gora = black_field(a, b-1, img)
                #dol = black_field(a, b+1, img)
                #print b
            if b-height/2<0:
                #print "poza zakresem w gore, h: ",
                #a=width/2+maxOdchyleniePrawoLewo/2-10
                gora = -10
                b+=1
                obecnie = black_field(a, b, img)
                prawo = black_field(a+1, b, img)
                lewo = black_field(a-1, b, img)
                #gora = black_field(a, b-1, img)
                dol = black_field(a, b+1, img)
                #print b
         
        else:    
            obecnie = black_field(a, b, img)
            prawo = black_field(a+1, b, img)
            lewo = black_field(a-1, b, img)
            gora = black_field(a, b-1, img)
            dol = black_field(a, b+1, img)
    return (a, b)
  
    
  
d = display.Display()              
def setCursorPosition(x, y):  
    s = d.screen()
    root = s.root
    root.warp_pointer(x,y)
    d.sync()
      

if __name__ == '__main__':
    #showMenu()
    #face_cascade = cv2.CascadeClassifier("/home/tomek/WORKSPACES!!/Systemy wizyjne/EyeTracking/src/xmle/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier('/home/tomek/workspace/systemyWizyjne/xmle/haarcascade_eye.xml')
    
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
      
      
    cv2.namedWindow('image')
    def nothing(*arg):
        pass
        #print threshold_value
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
    #print h
    oko_gray = cv2.cvtColor(wyciete_oko_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred = cv2.GaussianBlur(oko_gray, value, 2)
    blurred = cv2.flip(blurred,1)

    _, thresh1 = cv2.threshold(blurred, threshold_value, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C)#+cv2.THRESH_OTSU)
    #potrzebne do normalizacji jasnosci
    _, first_img = cap.read()
    srednia_jasnosc = first_img.mean()
    
    
    '''
       
    wyciete_oko_img = img[y-h/2:y+h/2, x-w/2:x+w/2] 
    oko_gray = cv2.cvtColor(wyciete_oko_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred = cv2.GaussianBlur(oko_gray, value, 2)
    blurred = cv2.flip(blurred,1)
    new_a, new_b = a, b 
    first_okolicaOkaBlurred = blurred[new_b-5:new_b+5, new_a-5:new_a+5]
    
    '''
    
    
    
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
        
        #threshold_value = cv2.getTrackbarPos('threshold_value', 'image')
        #print "thresholdValue ktore wchodzi " , threshold_value
        cv2.setTrackbarPos('threshold_value', 'image', threshold_value)
        _, thresh1 = cv2.threshold(blurred, threshold_value, 255,
                               cv2.ADAPTIVE_THRESH_MEAN_C)
     
        cv2.imshow('thresh',thresh1)
        
        #moja funkcja
        #new_a,new_b = pupil_position(thresh1,(a,b))
        new_a, new_b = a, b
        
        #dopisuje
        #print "threshold na wejsciu: ", threshold_value,
        global threshold_value
        okolicaOkaBlurred = blurred[new_b-5:new_b+5, new_a-5:new_a+5]
        '''
        #normalizuje jasnosc
        roznica_jasnosci = first_okolicaOkaBlurred.mean() - okolicaOkaBlurred.mean()
        jedynki = np.ones_like(okolicaOkaBlurred) #tablica jedynek
        deltki = cv2.multiply(jedynki,np.array([roznica_jasnosci])) # tablica o wymiarach obrazka wypelniona wartosciami  = roznica_jasnosci
        img = cv2.add(okolicaOkaBlurred, deltki) 
        #koniec normalizacji jasnosci
        '''
        #okolicaOkaBlurred = blurred
        _, okolicaOkaOdswiezona = cv2.threshold(okolicaOkaBlurred, threshold_value, 255,
                               cv2.ADAPTIVE_THRESH_MEAN_C)
        #sredniaJasnosc, _, __, ___ = cv2.mean(okolicaOkaBlurred)
        sredniaJasnosc, _, __, ___ = cv2.mean(okolicaOkaOdswiezona)
        #print 'drugi threshold', threshold_value 
        tmp_threshold_value = threshold_value
        if sredniaJasnosc<100:
            while sredniaJasnosc<120:
                #print sredniaJasnosc, sredniaJasnosc<220
                #print 1, cv2.mean(okolicaOkaOdswiezona), threshold_value
                if tmp_threshold_value >= 0:
                    tmp_threshold_value-=1
                #print threshold_value
                _, okolicaOkaOdswiezona = cv2.threshold(okolicaOkaBlurred, tmp_threshold_value, 255,
                               cv2.ADAPTIVE_THRESH_MEAN_C)
                cv2.imshow("okolicaokaodswiezona", okolicaOkaOdswiezona)
                sredniaJasnosc, _, __, ___ = cv2.mean(okolicaOkaOdswiezona)
                #print "nowa", sredniaJasnosc
            #print "wychodze"
        if sredniaJasnosc>245:
            while sredniaJasnosc>120:
                #sredniaJasnosc, _, __, ___ = cv2.mean(okolicaOka)
                #print 2, cv2.mean(okolicaOkaOdswiezona), threshold_value
                if tmp_threshold_value <= 255:
                    tmp_threshold_value+=1
                #print threshold_value
                _, okolicaOkaOdswiezona = cv2.threshold(okolicaOkaBlurred, tmp_threshold_value, 255,
                               cv2.ADAPTIVE_THRESH_MEAN_C)
                sredniaJasnosc, _, __, ___ = cv2.mean(okolicaOkaOdswiezona)
                #print "nowa", sredniaJasnosc
        #print "threshold na wyjsciu: ", threshold_value, "sredniajasnosc na wyjsciu", sredniaJasnosc
        threshold_value = tmp_threshold_value
    #koniec dopisanego
        
        
        # a moze nie trzeba dubla?? dubel po znormalizowaniu jasnosci wczesniej to samo bylo po to zeby okreslic dla jakiego obszaru jasnosc normalizowac
        new_a,new_b = pupil_position(thresh1,(a,b))
        cv2.rectangle(img,(x+w/2-new_a,y-h/2+new_b),(x+w/2-new_a-1,y-h/2+new_b+1),(255,0,0),2)#plus w, minus przy a :bo robie flip = obrot prawo lewo = lustrzane odbicie
        a, b = (new_a, new_b) #a, b to polozenie wzgledem ramki wycietej
        #print a, b
        
        #if menu.isModeOn():
        setCursorPosition(round((a-6)*skokKursoraPoziomy), round((b-6)*skokKursoraPionowy))
        
        cv2.moveWindow("thresh", 800,0)
        cv2.rectangle(img,(x-w/2,y-h/2),(x+w/2,y+h/2),(0,255,0),2)
        #ramka po ktorej moge sie poruszac
        wPolaSterowania, hPolaSterowania = poleSterowaniaResolution
        cv2.rectangle(img, (x-wPolaSterowania/2,y-hPolaSterowania/2), (x+wPolaSterowania/2,y+hPolaSterowania/2), (255,0,0),2)
        
        vis = img.copy()
        vis = cv2.flip(vis, 1)
        cv2.imshow('image',vis)
        if 0xFF & cv2.waitKey(5) == 27:
            break
    
    cv2.destroyAllWindows()