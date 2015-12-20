import os


ramkaWidth = 250
ramkaHeight = 150
gruboscObszaruSterowaniaKursorem = 2;

#dlugoscObszaruKlikania = ramkaWidth - 2*gruboscObszaruSterowaniaKursorem
#wysokoscObszaruKlikania = ramkaHeight - 2*gruboscObszaruSterowaniaKursorem



LICZBA_KLATEK_POTRZEBNA_DO_AKTYWACJI = 150


lICZBA_KLATEK_DO_PRZYSPIESZENIA = 3
maxSpeed = 100


os.system("python EyeTracking.py " + str(ramkaWidth) + " " + str(ramkaHeight) + 
          " " + str(lICZBA_KLATEK_DO_PRZYSPIESZENIA) + " " + str(LICZBA_KLATEK_POTRZEBNA_DO_AKTYWACJI))