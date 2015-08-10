import numpy as np
import cv2
from ParallelASM import Point, PASM
import math

fx = np.matrix( [-1, 0, 1] )
fy = np.transpose( fx )

img = cv2.imread( 'C:\\Users\\Valerie\\Desktop\\MicroExpress\\CASME2\\Cropped\\Cropped\\sub02\\EP01_11f\\reg_img46.jpg' )
imgg = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )

ptList = [ Point(1,1), Point(20,50), Point(5, 15) ]

def getRegion( img, pt ):
    return img[ pt.y - 1 : pt.y + 2, pt.x - 1 : pt.x + 2 ] 

a = map( lambda x : getRegion( imgg, x ) , ptList )

def getGradient( pt, img ):
    img = np.array([])
    dx = img
    delF = [ (img[ pt.y, pt.x + 1] - img[pt.y, pt.x - 1 ] )/2,
            (img[ pt.y + 1 , pt.x] - img[pt.y - 1, pt.x ] )/2 ] 
    print delF
    mag = math.sqrt( delF[0] ** 2 + delF[1] ** 2 )
    dir = PASM.angleV( delF, [ 0, 0] )
    return mag, dir

def applyFilter( mat, filter ):
    return cv2.filter2D( mat, cv2.CV_8U, filter )

map( lambda x : getGradient( x, imgg ),  ptList)
    