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
ramkaHeight = 20

def black_field(thresh, (pupilX, pupilY)):
    rozmiar = 10
    cropped_thresh = thresh[pupilY-rozmiar/2:pupilY+rozmiar/2, pupilX-rozmiar/2:pupilX+rozmiar/2]
    cv2.imshow('kropd', cropped_thresh)
    return 255-cv2.mean(cropped_thresh)[0]












 
'''
tu powinno byc tak ze zwracam kierunek i predkosc tego kierunku w ktorym bylo wieksze wyhylenie!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!





POPRAWIC!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!











!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''    
def korektaPupil(thresh, (x0,y0), (pupilX, pupilY)):
    #screenHeight, screenWidth = np.shape(thresh)
    margines = 5 #kazdy piksel to inny 'bieg'
    dXmax = (ramkaWidth-margines)/2.0
    dYmax = (ramkaHeight-margines)/2.0
    #jezeli zrenica jest w "obramowaniu" okienka to czytam to jako polecenie ruchu kursorem
    speed = 0
    speedPosX = 0
    speedNegX = 0
    speedPosY = 0
    speedNegY = 0
    if abs(pupilX-x0)>(dXmax-margines):
        if (pupilX-x0)>0:
            speedPosX = 1
            if (pupilX-x0)>4:
                speedPosX = 2
            if (pupilX-x0)>5:
                speedPosX = 5
            if (pupilX-x0)>6:
                speedPosX = 10
            if (pupilX-x0)>7:
                speedPosX = 20
        else:
            speedNegX = 1
            if (pupilX-x0)<-4:
                speedNegX = 2
            if (pupilX-x0)<-5:
                speedNegX = 5
            if (pupilX-x0)<-6:
                speedNegX = 10
            if (pupilX-x0)<-7:
                speedNegX = 20
    if abs(pupilY-y0)>(dYmax-margines):
        if (pupilY-y0)>0:
            speedPosY = 1
            if (pupilY-y0)>4:
                speedPosY = 2
            if (pupilY-y0)>5:
                speedPosY = 5
            if (pupilY-y0)>6:
                speedPosY = 10
            if (pupilY-y0)>7:
                speedPosY = 20
        else:
            speedNegY = 1
            if (pupilY-y0)<-4:
                speedNegY = 2
            if (pupilY-y0)<-5:
                speedNegY = 5
            if (pupilY-y0)<-6:
                speedNegY = 10
            if (pupilY-y0)<-7:
                speedNegY = 20
                  
    kierunek = 0 #kierunek 0 brak, 1-gora 2-prawo 3-dol, 4-lewo              
    maxSpeed = max([speedPosX, speedNegX, speedPosY, speedNegY])

    if speedPosX == maxSpeed:
        kierunek = 2
    elif speedNegX == maxSpeed:
        kierunek = 4
    elif speedPosY == maxSpeed:
        kierunek = 3
    elif speedNegY == maxSpeed:
        kierunek = 1
    speed = maxSpeed

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
  
    