import cv2
import os
from ParallelASM import Shape, PASM, Point
from FaceDraw import FaceDraw
from matplotlib import pyplot as plt
import numpy as np


DIR = 'C:\\Users\\Valerie\\Desktop\\MicroExpress\\facePoints\\session_1\\'
file = '000_1_1.pts'
img = cv2.imread( 'C:\\Users\\Valerie\\Downloads\\000_1_1.ppm')
img_g = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )

pasm = PASM( [36,31], 10 )

with open( os.path.join( DIR, file), "r" ) as infile:
    ptList = [ ]
    allLines = infile.readlines()
    pointLine = False
    cleanLines = [ x.strip() for x in allLines]
    for line in cleanLines:
        if line is '{':
            pointLine = True
                
        elif line is '}':
            pointLine = False
            pass
        elif pointLine:
            ptList.append( map( float, line.split(' ') ) )
        else:
            pass
ptList
s1 = Shape( ptList )
plt.imshow( img_g, cmap = 'gray' )
FaceDraw( s1, plt).drawBold()
plt.show()


plt.imshow(cv2.filter2D( img_g, cv2.CV_8U, np.array([ -1, 0, 1]) ))
FaceDraw( s1, plt).drawBold()
plt.show()
plt.imshow(cv2.filter2D( img_g, cv2.CV_8U, np.array([[ -1], [0],[ 1]]) ))
FaceDraw( s1, plt).drawBold()
plt.show()


