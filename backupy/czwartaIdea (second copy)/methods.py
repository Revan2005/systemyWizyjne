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
#from menu import *
from numpy import sqrt, real, math, double
from cmath import atan, cos, sin
from math import atan2
from EyeTracking import *

ramkaWidth = 20
ramkaHeight = 14

def black_field(thresh, (pupilX, pupilY)):
    rozmiar = 10
    cropped_thresh = thresh[pupilY-rozmiar/2:pupilY+rozmiar/2, pupilX-rozmiar/2:pupilX+rozmiar/2]
    cv2.imshow('kropd', cropped_thresh)
    return 255-cv2.mean(cropped_thresh)[0]












 
'''





POPRAWIC!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
zle licze te odleglosci wyhylenia, zastnow sie nad tym jeszcze



ROZGRZEBANE POPRAWIC OMYSLEC ramka grubosc dx itp (przed paroma linijkami zmian dzialalo w miare spoko)







!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''    
def korektaPupil(thresh, (x0,y0), (pupilX, pupilY)):
    #screenHeight, screenWidth = np.shape(thresh)
    margines = 5 #kazdy piksel to inny 'bieg'
    dXmax = ramkaWidth/2.0
    dYmax = ramkaHeight/2.0
    dXmin = dXmax - margines
    dYmin = dYmax - margines
    #jezeli zrenica jest w "obramowaniu" okienka to czytam to jako polecenie ruchu kursorem
    speed = 0
    speedPosX = 0
    speedNegX = 0
    speedPosY = 0
    speedNegY = 0
    dX = pupilX-x0
    dY = pupilY-y0
    
    if abs(dX)>dXmin:
        if dX>0:
            speedPosX = 2
            print 'predkosc 1'
            if dX>dXmin+1:
                speedPosX = 2
                print "predkosc 2"
            if dX>dXmin+2:
                speedPosX = 5
                print "predkosc 4"
            if dX>dXmin+3:
                speedPosX = 5
                print "predkosc 10"
            if dX>dXmin+4:
                speedPosX = 10
                print "predkosc 20"
            if dX>dXmin+5:
                speedPosX = 20
                print "predkosc 50"
            if dX>dXmin+6:
                speedPosX = 20
                print 'predkosc 100'
            if dX>dXmin+7:
                speedPosX = 35
                print 'predkosc 100'
        else:
            speedNegX = 2
            if dX<-dXmin-1:
                speedNegX = 2
            if dX<-dXmin-2:
                speedNegX = 5
            if dX<-dXmin-3:
                speedNegX = 5
            if dX<-dXmin-4:
                speedNegX = 10
            if dX<-dXmin-5:
                speedNegX = 20
            if dX<-dXmin-6:
                speedNegX = 20
            if dX<-dXmin-7:
                speedNegX = 35
    if abs(dY)>dYmin:
        if dY>0:
            speedPosY = 2
            if dY>dYmin+1:
                speedPosY = 2
            if dY>dYmin+2:
                speedPosY = 5
            if dY>dYmin+3:
                speedPosY = 5
            if dY>dYmin+4:
                speedPosY = 10
            if dY>dYmin+5:
                speedPosY = 20
            if dY>dYmin+6:
                speedPosY = 20
            if dY>dYmin+7:
                speedPosY = 35
        else:
            speedNegY = 2
            if dY<-dYmin-1:
                speedNegY = 2
            if dY<-dYmin-2:
                speedNegY = 5
            if dY<-dYmin-3:
                speedNegY = 5
            if dY<-dYmin-4:
                speedNegY = 10
            if dY<-dYmin-5:
                speedNegY = 20
            if dY<-dYmin-6:
                speedNegY = 20
            if dY<-dYmin-7:
                speedNegY = 35
                  
    kierunek = 0 #kierunek 0 brak, 1-gora 2-prawo 3-dol, 4-lewo              
    maxSpeed = max([speedPosX, speedNegX, speedPosY, speedNegY])
    #print speedPosX, speedPosY, speedNegX, speedNegY, maxSpeed
    
    if speedPosX == maxSpeed:
        kierunek = 2
    elif speedNegX == maxSpeed:
        kierunek = 4
    elif speedPosY == maxSpeed:
        kierunek = 3
    elif speedNegY == maxSpeed:
        kierunek = 1
    speed = maxSpeed
    print 'speed na koncu = ', speed

    return (pupilX, pupilY, x0, y0, kierunek, speed)

def obliczPozycjeRamki(thresh, (x0,y0), (pupilX, pupilY)):
    dXmax = ramkaWidth/2.0
    dYmax = ramkaHeight/2.0
    #'uciekam okienkiem'
    if abs(pupilX-x0)>dXmax:
        if (pupilX-x0)>0:
            x0 += (pupilX-x0 - (dXmax))
        else:
            x0 += (pupilX-x0 + (dXmax))
    if abs(pupilY-y0)>dYmax:
        if (pupilY-y0)>0:
            y0 += (pupilY-y0 - (dYmax))
        else:
            y0 += (pupilY-y0 + (dYmax))
    return (x0,y0)

def pupil_position(thresh, (x0, y0), (pupilX, pupilY)):
    obecnie = black_field(thresh, (pupilX, pupilY))
    prawo = black_field(thresh, (pupilX+1, pupilY))
    lewo = black_field(thresh, (pupilX-1, pupilY))
    gora = black_field(thresh, (pupilX, pupilY-1))
    dol = black_field(thresh, (pupilX, pupilY+1))
    kierunek = 0
    
    while (obecnie < max([prawo, lewo, gora, dol])): 
        if prawo > obecnie:
            pupilX+=1
        elif lewo > obecnie:
            pupilX-=1
        elif gora > obecnie:
            pupilY-=1
        elif dol > obecnie:
            pupilY+=1   
        x0, y0 = obliczPozycjeRamki(thresh, (x0, y0), (pupilX, pupilY))
        obecnie = black_field(thresh, (pupilX, pupilY))
        prawo = black_field(thresh, (pupilX+1, pupilY))
        lewo = black_field(thresh, (pupilX-1, pupilY))
        gora = black_field(thresh, (pupilX, pupilY-1))
        dol = black_field(thresh, (pupilX, pupilY+1)) 
    
    pupilX, pupilY , x0, y0, kierunek, speed = korektaPupil(thresh, (x0,y0), (pupilX, pupilY))    
    return (pupilX, pupilY, x0, y0, kierunek, speed)
  
def removeEyeBrow(oko_thresh):
    for x in xrange(oko_thresh.shape[0]):
        for y in xrange(oko_thresh.shape[1]):
            pass
        