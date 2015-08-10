from DeformableASM import DASM, PASM
from ParallelASM import Point, Shape
from FaceDraw import FaceDraw

from matplotlib import pyplot as plt

import numpy as np
import os
import math
import cv2
import time
from PIL import Image
import copy

def showImg( imgIn ):
    img = Image.fromarray(imgIn)
    img.show()

def readInAlign( ):
    allLines = None
    with open( "outfile-ASM-100iters-500tr.txt", "r") as infile:
        allLines = infile.readlines()
        cleanLines = map( lambda x : x.strip().split(), allLines )
    
    asm = PASM( [36,31],10 )
    s = []

    for tuple in cleanLines:
        if tuple[0] == '!!!':
            if s != []:
                asm.meanShape = Shape( s )
                s = []
            else: 
                pass
        elif tuple[0] == '@@@':
            if s != [] :
                asm.addShape( Shape(s) )
                s = []
            else: 
                pass
        else:
            s.append( Point( float(tuple[0]), float(tuple[1]) ) )
                
    return asm

def readInImage( ):

    img = cv2.imread( 'C:\\Users\\Valerie\\Desktop\\MicroExpress\\CASME2\\Cropped\\Cropped\\sub02\\EP01_11f\\reg_img46.jpg' )
    img = cv2.imread( 'C:\\Users\\Valerie\Desktop\\MicroExpress\\CASME2\\CASME2_RAW\\CASME2-RAW\\sub01\\EP02_01f\\img1.jpg')
    
    img = cv2.imread( 'C:\\Users\\Valerie\\Downloads\\000_1_1.ppm')
    img_gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY ) 
    #faces = face_cascade.detectMultiScale( gray, 1.3, 5)
    #for (x,y,w,h) in faces:
    #    cv2.rectangle( img, (x,y), (x+w,y+h), (255,0,0),2)
    #    roi_gray = gray[y:y+h, x:x+w]
    #    roi_color = img[y:y+h, x:x+w]

    return img_gray
def areaRect( tup ):
    return tup[2] * tup[3]


def findEyes( img_gray ):
    eye_cascade = cv2.CascadeClassifier('C:\\OpenCV\\data\\haarcascades\\haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(img_gray)
    im_toshow = copy.deepcopy(img_gray)
    eyeArr = []
    for (ex,ey,ew,eh) in eyes:

        cv2.rectangle(im_toshow,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        eyeArr.append( ( ex, ey, ew, eh ) )

    # filter by area
    eyeAreas = map( areaRect, eyeArr )
    ix = np.argmax( eyeAreas )
    eye1 = eyeArr[ix]
    
    eyeAreas.pop( ix )
    eyeArr.pop(ix )

    ix = np.argmax( eyeAreas )
    eye2 = eyeArr[ix]

    ex1, ey1, ew1, eh1 = eye1
    eye1loc = Point( ex1 + ew1/2,ey1+ eh1/2)

    ex2, ey2, ew2, eh2 = eye2
    eye2loc = Point( ex2 + ew2/2,ey2+ eh2/2)

    cv2.circle( im_toshow, ( int(eye1loc.x), int(eye1loc.y) ), 1, (255,255,255) )
    cv2.circle( im_toshow, ( int(eye2loc.x), int(eye2loc.y) ), 1, (255,255,255) )
    #showImg( im_toshow ) 
    return eye1loc, eye2loc

def calcShift( point, img_gray ):
    ## get point p (ix 48)
    p = point

    # Get gradient ( unitV already )
    f, m = dasm.getGradient( p, img_gray )
#    print "x %f, y %f" % ( p.x, p.y )
    cX = p.x
    cY = p.y
    #print f, m
    maxM = 1
    cnt = 0
    while cX < np.shape( img_gray )[1] and cY < np.shape( img_gray )[0]:

        if cnt > 30:
            return pt.x + f[0] * float(m)/float(maxM), pt.y + f[1]* float(m)/float(maxM)
        cnt+= 1
        cX = cX + f[0]
        cY = cY + f[1]
        if cX < np.shape( img_gray )[1] and cY < np.shape( img_gray)[0]:
            _, cM = dasm.getGradient( Point( cX, cY ), img_gray )
            if cM > maxM:
                maxM = cM
    #            print "cX %f cY %f" % (cX, cY) 
    return pt.x + f[0] * float(m)/float(maxM), pt.y + f[1]* float(m)/float(maxM)

def drawFaces( dasm ):
    # Test model and appModel structures
    FaceDraw( dasm.model, plt).drawBold()
    FaceDraw( dasm.appModel, plt).drawBold()

####  MAIN ###########
asm = readInAlign()
dasm = DASM( asm )

drawFaces( dasm )

## Read in image
img_gray = readInImage()

## Align model to image face
eye1, eye2 = findEyes( img_gray )
dasm.alignEyes( eye1, eye2, img_gray )

plt.imshow( img_gray, cmap = 'gray' )
drawFaces( dasm )







dmodel = copy.deepcopy( dasm.model )
i = 0
while i < 100:
#    print i
    allpt = []
    pts = []

    for pt in dmodel.shapePoints:
       dx, dy = calcShift( pt, img_gray )
       allpt.append( dx )
       allpt.append( dy )
       pts.append( [dx, dy] )
       #print pts
    
    dmodel = Shape( pts )
    FaceDraw( dasm.model, plt ).drawBold()
    FaceDraw( dmodel, plt ).drawContrast()
    plt.imshow( img_gray )

    ### 

    i+= 1

plt.show()

FaceDraw( dasm.model, plt ).drawBold()
FaceDraw( dmodel, plt ).drawContrast()
plt.imshow( img_gray )
plt.show()
