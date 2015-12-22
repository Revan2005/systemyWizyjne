import os
from Tkinter import  *
import tkMessageBox

if __name__ == "__main__":
    top = Tk()
    
    widthTrackbar = Scale(top, from_ = 5, to = 200, orient = HORIZONTAL, label = "Szerokosc ramki")
    widthTrackbar.set(25)
    widthTrackbar.pack()
    heightTrackbar = Scale(top, from_ = 5, to = 200, orient = HORIZONTAL, label = "Wysokosc ramki")
    heightTrackbar.set(15)
    heightTrackbar.pack()
    accelerationTrackbar = Scale(top, from_ = 1, to = 100, orient = HORIZONTAL, label = "Przyspieszenie")
    accelerationTrackbar.set(10)
    accelerationTrackbar.pack()
    clickTrackbar = Scale(top, from_ = 1, to = 100, orient = HORIZONTAL, label = "Szybkosc klikania do -1")
    clickTrackbar.set(150)
    clickTrackbar.pack()
    
    def start():
        ramkaWidth = widthTrackbar.get()
        ramkaHeight = heightTrackbar.get()
        PRZYSPIESZENIE = accelerationTrackbar.get()
        LICZBA_KLATEK_POTRZEBNA_DO_AKTYWACJI = clickTrackbar.get()
        top.destroy()
        os.system("python EyeTracking.py " + str(ramkaWidth) + " " + str(ramkaHeight) + 
                  " " + str(PRZYSPIESZENIE) + " " + str(LICZBA_KLATEK_POTRZEBNA_DO_AKTYWACJI))
        
    B = Button(top, text ="Uruchom", command = start)
    B.pack()
    top.mainloop()



