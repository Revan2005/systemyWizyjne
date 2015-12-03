'''
Created on 04-11-2015

@author: tomek
'''
import numpy as np
import cv2
import video
from methods import *
import Tkinter as tk
from Xlib import display
from menu import *
from numpy import sqrt, real, math, double
from cmath import atan, cos, sin
from math import atan2
from EyeTracking import *


poleSterowaniaWidth = 30
poleSterowaniaHeight = 30
poleSterowaniaResolution = (poleSterowaniaWidth, poleSterowaniaHeight)

def odleglosc((x1,y1),(x2,y2)):
    dxKw = pow((x1-x2), 2)
    dyKw = pow((y1-y2), 2)
    return sqrt( dxKw + dyKw )

def ustalAlfa((x0,y0), (a,b)):
    dy = -(b-y0)
    dx = (a-x0)
    if dx == 0:
        if b > y0:
            alfa = 270
        else:
            alfa = 90
    else:
        alfa = math.atan( float(dy) / dx )
        if a < x0:
            alfa += math.pi
    if alfa<0:
        alfa += 2*math.pi
            
    '''
    if(dx!=0):
        print 'dy',dy,'dx',dx, 'dy/dx', float(dy)/dx
    alfa /= math.pi
    alfa *= 180
    print 'alfa=',alfa
    '''
    
    return alfa
        

def ustawNaObwodzie(alfa, (x0,y0), r):      
    newa = x0 + real(cos(alfa)*r)
    newb = y0 - real(sin(alfa)*r)
    return (int(round(newa)), int(round(newb)))

def black_field(a, b, img):
    #print a, b
    #print b-5, b+5, a-5, b+5
    cropped_img = img[b-5:b+5, a-5:a+5]
    cv2.imshow('kropd', cropped_img)
    #print 255-cv2.mean(cropped_img)[0]
    return 255-cv2.mean(cropped_img)[0]
 
    

def pupil_position(img, (a,b), radius):
    #a,b wspolrzedne zrenicy, (x,y)wspolrzedne centrum kolka
    height, width = np.shape(img)
    maxOdchyleniePrawoLewo, maxOdchylenieGoraDol = poleSterowaniaResolution#(width-12, height-12) #12 to bufor zeby nie wychodzilo za zakres jak wywoluje blac field (tam dodaje odejmuje 5 pikseli wiec na wszelki wypadek dalem 6 bufor /ramke wokol) 
    x0, y0 = width/2, height/2
    px, py = (a, b)
   
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
            
        alfa = ustalAlfa((x0,y0), (a,b))
        #print 'alfa = ', alfa, "00=", (x0, y0), "ab=", (a,b)
        #print 'atan 20/8', atan(20/8)*180/math.pi
        
        if( odleglosc((a,b),(x0,y0))>radius ):
            #oblicz kat i umiesc na obwodzie , x y to srodek moje 0,0 ukladu
            px, py = ustawNaObwodzie(alfa, (x0,y0), radius)
        else:
            px, py = (a, b)
            
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
    return (a, b, px, py)
  
    