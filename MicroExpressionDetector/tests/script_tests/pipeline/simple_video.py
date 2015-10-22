import numpy as np               
import cv2

VID = "C:\Users\Valerie\Documents\Research\MicroExpress\CASME2_Compressed video\CASME2_compressed\sub01\EP02_01f.avi"

cap = cv2.VideoCapture(VID)

while(cap.isOpened()):
    face_cascade = cv2.CascadeClassifier('C:\\OpenCV\\data\\haarcascades\\haarcascade_frontalface_default.xml')
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    
    #faces = face_cascade.detectMultiScale( gray, 1.3, 4)
    #print faces
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
