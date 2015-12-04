import os
import cv2

dir = "C:\Users\Valerie\Pictures\Camera Roll"
vid = "WIN_20151017_12_26_36_Pro.mp4"

i = 0
cap = cv2.VideoCapture( os.path.join( dir, vid ))
while( True ):
    ret, frame = cap.read()
    gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY )
    cv2.imwrite(os.path.join( dir, "%d.jpg" % i  ), gray )
    i += 1
    