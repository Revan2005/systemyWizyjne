'''
Created on 04-11-2015

@author: tomek
'''
import numpy as np
import cv2
#import video
from methods import *
import Tkinter as tk
from Xlib import display
#from menu import *
from numpy import sqrt, real, math, double
from cmath import atan, cos, sin
from math import atan2
from EyeTracking import *


root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()



ramkaWidth = 24
ramkaHeight = 19

def czyMoznaWPrawo(px, py, capWidth, capHeight):
    if px < capWidth-ramkaWidth / 2 - 5:
        return True
    return False

def czyMoznaWLewo(px, py, capWidth, capHeight):
    if px > ramkaWidth / 2 + 5:
        return True
    return False

def czyMoznaWGore(px, py, capWidth, capHeight):
    if py > ramkaHeight / 2 + 5:
        return True
    return False

def czyMoznaWDol(px, py, capWidth, capHeight):
    if py < capHeight - ramkaHeight / 2 - 5:
        return True
    return False


def black_field(thresh, (pupilX, pupilY)):
    rozmiar = 10
    cropped_thresh = thresh[pupilY-rozmiar/2:pupilY+rozmiar/2, pupilX-rozmiar/2:pupilX+rozmiar/2]
    cv2.imshow('kropd', cropped_thresh)
    return 255-cv2.mean(cropped_thresh)[0]

  
def korektaPupil(thresh, (x0,y0), (pupilX, pupilY)):
    #screenHeight, screenWidth = np.shape(thresh)
    margines = 8 #kazdy piksel to inny 'bieg'
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
                speedPosX = 35
                print 'predkosc 100'
            if dX>dXmin+7:
                speedPosX = 50
                print 'predkosc 100'
            if dX>dXmin+8:
                speedPosX = 100
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
                speedNegX = 35
            if dX<-dXmin-7:
                speedNegX = 50
            if dX<-dXmin-8:
                speedNegX = 100
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
                speedPosY = 35
            if dY>dYmin+7:
                speedPosY = 50
            if dY>dYmin+8:
                speedPosY = 100
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
                speedNegY = 35
            if dY<-dYmin-7:
                speedNegY = 50
            if dY<-dYmin-8:
                speedNegY = 100
                  
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

def pupil_position_meanshift(thresh, (x0, y0), (pupilX, pupilY), (capWidth, capHeight)):
    obecnie = black_field(thresh, (pupilX, pupilY))
    prawo = black_field(thresh, (pupilX+1, pupilY))
    lewo = black_field(thresh, (pupilX-1, pupilY))
    gora = black_field(thresh, (pupilX, pupilY-1))
    dol = black_field(thresh, (pupilX, pupilY+1))
    kierunek = 0
    
    while (obecnie < max([prawo, lewo, gora, dol])): 
        if prawo > obecnie:
            if not czyMoznaWPrawo(pupilX, pupilY, capWidth, capHeight):
                break
            pupilX+=1
        elif lewo > obecnie:
            if not czyMoznaWLewo(pupilX, pupilY, capWidth, capHeight):
                break
            pupilX-=1
        elif gora > obecnie:
            if not czyMoznaWGore(pupilX, pupilY, capWidth, capHeight):
                break
            pupilY-=1
        elif dol > obecnie:
            if not czyMoznaWDol(pupilX, pupilY, capWidth, capHeight):
                break
            pupilY+=1   
        x0, y0 = obliczPozycjeRamki(thresh, (x0, y0), (pupilX, pupilY))
        obecnie = black_field(thresh, (pupilX, pupilY))
        prawo = black_field(thresh, (pupilX+1, pupilY))
        lewo = black_field(thresh, (pupilX-1, pupilY))
        gora = black_field(thresh, (pupilX, pupilY-1))
        dol = black_field(thresh, (pupilX, pupilY+1)) 
        #if pozaEkranem(pupilX, pupilY, capWidth, capHeight):
        #    break
    
    pupilX, pupilY , x0, y0, kierunek, speed = korektaPupil(thresh, (x0,y0), (pupilX, pupilY))    
    return (pupilX, pupilY, x0, y0, kierunek, speed)




