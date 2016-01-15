import os
from Tkinter import  *
import tkMessageBox

if __name__ == "__main__":
    top = Tk()
    
    widthTrackbar = Scale(top, from_ = 5, to = 200, orient = HORIZONTAL, label = "Szerokosc ramki [pix]")
    widthTrackbar.set(21)
    widthTrackbar.pack()
    heightTrackbar = Scale(top, from_ = 5, to = 200, orient = HORIZONTAL, label = "Wysokosc ramki [pix]")
    heightTrackbar.set(12)
    heightTrackbar.pack()
    accelerationTrackbar = Scale(top, from_ = 1, to = 100, orient = HORIZONTAL, label = "Przyspieszenie [pix/s^2]")
    accelerationTrackbar.set(8)
    accelerationTrackbar.pack()
    clickTrackbar = Scale(top, from_ = 1, to = 10, orient = HORIZONTAL, label = "Czas bezruchu potrzebny do klikniecia [s]")
    clickTrackbar.set(1)
    clickTrackbar.pack()
    
    def start():
        ramkaWidth = widthTrackbar.get()
        ramkaHeight = heightTrackbar.get()
        PRZYSPIESZENIE = accelerationTrackbar.get()
        CZAS_POMIEDZY_KLIKNIECIAMI = clickTrackbar.get()
        top.destroy()
        os.system("python EyeTracking.py " + str(ramkaWidth) + " " + str(ramkaHeight) + 
                  " " + str(PRZYSPIESZENIE) + " " + str(CZAS_POMIEDZY_KLIKNIECIAMI))
        
    B = Button(top, text ="Uruchom", command = start)
    B.pack()
    top.mainloop()



