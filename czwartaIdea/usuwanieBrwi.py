import numpy as np
import matplotlib.pyplot as plt
import cv2

#cap = cv2.VideoCapture(0)

def removeRows(a,b,oko_thresh):
    if  (a==0) & (b >= oko_thresh.shape[0]-2):
        wyciete = oko_thresh[:, :]
        ones = np.ones_like(wyciete)
        biale = np.multiply(ones, [255])
        oko_thresh[:, :] = biale
    elif a == 0:
        wyciete = oko_thresh[a:b+1, :]
        ones = np.ones_like(wyciete)
        biale = np.multiply(ones, [255])
        oko_thresh[a:b+1, :] = biale
    elif b >= oko_thresh.shape[0]-2:
        wyciete = oko_thresh[a-1:b, :]
        ones = np.ones_like(wyciete)
        biale = np.multiply(ones, [255])
        oko_thresh[a-1:b, :] = biale
    else:
        wyciete = oko_thresh[a-1:b+2, :]
        ones = np.ones_like(wyciete)
        biale = np.multiply(ones, [255])
        oko_thresh[a-1:b+2, :] = biale
    return oko_thresh

def removeCols(a,b,oko_thresh):
    wyciete = oko_thresh[:, a:b+1]
    ones = np.ones_like(wyciete)
    biale = np.multiply(ones, [255])
    oko_thresh[:, a:b+1] = biale
    return oko_thresh

def usunBrew(thresh):
    #histshape0 - histogram "rzucony" na os pionowa OY, -histshape1 na pozioma OX
    histShape0 = [0 for i in range(thresh.shape[0])] 
    for y in xrange(thresh.shape[0]):
        for x in xrange(thresh.shape[1]):
            if thresh[y][x] == 0:
                #czarny piksel
                histShape0[y] += 1
    #podluzny ksztalt prezentuje sie jako pik na histogramie, zrenica ma wysokosc podobna do szerokosci podstawy na histogramie
    #zrenica ma okolo 15x15 pikseli
    granice = []
    prog = 5
    for i in range(len(histShape0)-1):
        if (histShape0[i]<=prog) & (histShape0[i+1]>prog) | ((i==0) & (histShape0[0]>prog)):
            resztaHistogramu = histShape0[i+1:]
            for j in range(len(resztaHistogramu)):
                if (resztaHistogramu[j]<=prog) | (j == len(resztaHistogramu)-1):
                    granice.append((i, i+j))
                    break
    #teraz szukam maximow w tych granicach one mi powiedza o rozciaglosci obiektu w osi OX, dla zrenicy stosunek powinien byc bliski 1
    progPodluznosci = 2.0
    for g in granice:
        a, b = g
        przedzial = histShape0[a:b] 
        if a>=b:
            podluznosc = 0
        else:  
            podluznosc = max(przedzial)/((b-a)*1.0)
        print podluznosc
        if podluznosc > progPodluznosci:
            thresh = removeRows(a,b,thresh)
            print 'usunieto wiersze'
    histShape0 = np.zeros_like(histShape0)    
    for y in xrange(thresh.shape[0]):
        for x in xrange(thresh.shape[1]):
            if thresh[y][x] == 0:
                #czarny piksel
                histShape0[y] += 1
    return thresh , histShape0, granice

'''
def usunPionowe(thresh):
    #histshape0 - histogram "rzucony" na os pionowa OY, -histshape1 na pozioma OX
    histShape1 = [0 for i in range(thresh.shape[1])] 
    for y in xrange(thresh.shape[0]):
        for x in xrange(thresh.shape[1]):
            if thresh[y][x] == 0:
                #czarny piksel
                histShape1[x] += 1
    #podluzny ksztalt prezentuje sie jako pik na histogramie, zrenica ma wysokosc podobna do szerokosci podstawy na histogramie
    #zrenica ma okolo 15x15 pikseli
    granice = []
    prog = 0
    for i in range(len(histShape0)-1):
        if (histShape1[i]<=prog) & (histShape1[i+1]>prog) | ((i == 0) & (histShape1[0]>prog)):
            resztaHistogramu = histShape1[i+1:]
            for j in range(len(resztaHistogramu)):
                if (resztaHistogramu[j]<=prog) | (j == len(resztaHistogramu)-1):
                    granice.append((i, i+j))
                    break
    #teraz szukam maximow w tych granicach one mi powiedza o rozciaglosci obiektu w osi OX, dla zrenicy stosunek powinien byc bliski 1
    progPodluznosci = 2.0
    for g in granice:
        a, b = g
        przedzial = histShape1[a:b]  
        if a >= b:
            podluznosc = 0
        else:
            podluznosc = max(przedzial)/((b-a)*1.0)
        print podluznosc
        if podluznosc > progPodluznosci:
            thresh = removeCols(a,b,thresh)
            print 'usunieto kolumny'
    histShape1 = np.zeros_like(histShape1)    
    for y in xrange(thresh.shape[0]):
        for x in xrange(thresh.shape[1]):
            if thresh[y][x] == 0:
                #czarny piksel
                histShape1[y] += 1
    return thresh , histShape1
'''
'''
if __name__ == '__main__':
    cv2.namedWindow("przed zabiegami")
    cv2.namedWindow("po zabiegach")
    cv2.moveWindow("przed zabiegami", 100, 100)
    cv2.moveWindow("po zabiegach", 400, 100)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        value = (35,35)
        blurred = cv2.GaussianBlur(gray, value, 2)
        blurred = blurred[300:350, 300:400]
        _, thresh = cv2.threshold(blurred, 75, 255, cv2.ADAPTIVE_THRESH_MEAN_C)
           
        cv2.imshow('przed zabiegami',thresh)   
        thresh, histShape0, granice = usunPoziome(thresh)
        #thresh, histShape1 = usunPionowe(thresh)
        cv2.imshow('po zabiegach',thresh)     
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            for g in granice:
                print g
            cv2.imwrite("obrazek.jpg", thresh)
            plt.plot(histShape0)
            plt.ylabel('liczba czarnych pikseli w wierszu')
            plt.show()
            
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
'''