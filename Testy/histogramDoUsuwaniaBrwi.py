import numpy as np
import matplotlib.pyplot as plt
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    value = (35,35)
    blurred = cv2.GaussianBlur(gray, value, 2)
    blurred = blurred[300:350, 300:400]
    _, thresh = cv2.threshold(blurred, 65, 255, cv2.ADAPTIVE_THRESH_MEAN_C)
    
    histShape0 = [0 for i in range(thresh.shape[0])]
    histShape1 = [0 for i in range(thresh.shape[1])]
         
    for y in xrange(thresh.shape[0]):
        for x in xrange(thresh.shape[1]):
            if thresh[y][x] == 0:
                #czarny piksel
                histShape0[y] += 1
    
       
            
            
    # Display the resulting frame
    cv2.imshow('frame',thresh)
    
      
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        plt.plot(histShape0)
        plt.ylabel('some numbers')
        plt.show()  
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()