import math
import cv2
import numpy as np
from matplotlib import pyplot as plt

class PreProcessing(object):
    def __init__( self ):
        return 

    @staticmethod
    def readInImg( imgPath ):
        img = cv2.imread( imgPath )
        img = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
        if np.shape( img )[0] > 400:
            img = crop( img, 2.5, 2)
        # resize to 28ish * 23ish
    
        return img

    @staticmethod
    def imgRes( img, scale ):
        dims = np.shape( img )
        nh, nw = map( lambda m: int(math.floor( m * scale)), dims )
        return nh, nw
    
    @staticmethod
    def downsample( img, nh, nw ):
        #img = cv2.resize( img, dsize= (dim,dim), fx = .1, fy = 0.1, interpolation = cv2.INTER_NEAREST )
        img = cv2.resize( img, dsize= (nh, nw), interpolation = cv2.INTER_NEAREST )
        return img

    @staticmethod
    def faceDetection( img ):
        face_cascade = cv2.CascadeClassifier('C:\\OpenCV\\data\\haarcascades\\haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale( img, 1.3, 5)
        x,y,w,h = faces[0]
        roi_gray = img[y:y+h, x:x+w]   
        return roi_gray

    @staticmethod    
    def eyeDetection( img ):
        eye_cascade = cv2.CascadeClassifier('C:\\OpenCV\\data\\haarcascades\\haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale( img )
        eye1, eye2 = filterFoundEyes( eyes, img )
        return eye1, eye2


    #    print d    #    print newH, newW

    @staticmethod
    def crop( img, fh, fw ):       ## In terms of x, y not h, w !!!   # or the other way>>>

        # Using eyes
        eye1, eye2 = eyeDetection( img )
        d = Point.dist( eye1, eye2 )

        newH = int(fh * d)  #set more firmly for other types of images for consistent size
        newW = int(fw * d)
    
        y0, x0 = newEyeLoc( eye1, eye2, newH, newW, d )

        return img[ y0 : y0 + newH, x0 : x0  + newW ]

    
    @staticmethod
    def newEyeLoc( eye1, eye2, newH, newW, d):
        if eye1.x < eye2.x:
            y0 = eye1.y - ( newH ) / 3
            x0 = eye1.x - ( newW - d )/2
        else:
            y0 = eye2.y - ( newH ) / 3
            x0 = eye2.x - ( newW - d )/2
        return y0, x0

    @staticmethod
    def showEyes( img, eye1, eye2 ):
        im_toshow = copy.deepcopy( img )
        cv2.circle( im_toshow, eye1, 10, (1,0,0) )
        cv2.circle( im_toshow, eye2, 10, (0,1,0) )
        plt.imshow( im_toshow, cmap = "gray" )
        plt.show()
   
    @staticmethod
    def areaRect( tup ):
        return tup[2] * tup[3]

    @staticmethod
    def filterFoundEyes( eyes, img ):
        if len( eyes ) > 1:  ## if multiple eyes are returned, get biggest one
            eyeArr = []
            for (ex,ey,ew,eh) in eyes:
                #cv2.rectangle(im_toshow,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
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
            ex2, ey2, ew2, eh2 = eye2

        else:   ## just one eye, estimate the other
            ex, ey, ew, eh = eyes[0] 
            w0 = np.shape( img )[1]
            if ex < w0 / 2:
                ex1, ey1, ew1, eh1 = [  ex, ey, ew, eh  ]
                ex2, ey2, ew2, eh2 = [ ex + w0/5, ey, ew, eh ]
            else: 
                ex1, ey1, ew1, eh1 = [  ex - w0/5, ey, ew, eh  ]
                ex2, ey2, ew2, eh2 = [ ex, ey, ew, eh ]
            
 

        eye1loc = Point( ex1 + ew1/2, ey1+ eh1/2 )
        eye2loc = Point( ex2 + ew2/2, ey2+ eh2/2)


        return eye1loc, eye2loc         



