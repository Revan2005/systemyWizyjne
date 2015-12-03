'''
Created on 14-10-2015

@author: tomek
'''
from Tkinter import *
#import Tkinter as tk


mode = False 
def showMenu():     
    button = Button(text='Stop', width=10, height=10, command=setModeOff)
    button.pack()

    button2 = Button(text='Start', width=10, height=10, command=setModeOn)
    button2.pack()

    mainloop()

def isModeOn():
    return mode

def setModeOn():
    mode = True
    
def setModeOff():
    mode = False




