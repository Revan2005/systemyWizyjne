'''
Created on 09-10-2015

@author: tomek
'''
import Tkinter as tk
from Xlib import display
from time import sleep

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print screen_height, screen_width,

d = display.Display()
def move_mouse(x,y):#Moves the mouse to (x,y). x and y are ints
    s = d.screen()
    root = s.root
    root.warp_pointer(x,y)
    d.sync()
  
if __name__ == '__main__':
    move_mouse(10, 10)
    sleep(5)
    move_mouse(screen_width-10, screen_height-10)
  #  dt.rawinput.click(100,100)