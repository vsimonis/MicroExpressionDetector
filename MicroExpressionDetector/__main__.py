import cv2
import os
import pandas as pd
import math
import numpy as np
from matplotlib import pyplot as plt
import re
import copy
from shapes.Point import Point

  
def getLabelInfo( sub, vid, df, videoKey ):
   
    # Query master table given subject and video
    instance = df.query( 'Subject == %d & Filename == "%s"' % ( int(sub.replace( "sub", "" )), vid) )
    
    # Get important stuff from there
    onset = int( instance.OnsetFrame.values[0] )
    apex =  instance.ApexFrame.values[0] 
    offset = int( instance.OffsetFrame.values[0] )

    s,v = videoKey ## unpack (subject, video, frame)
    

    ## double check boundaries of onset/apex/offset
    accum = {
        "subject" : s,
        "video" : v,
        }
    params = { 
        "emotion" : instance['Estimated Emotion'].values[0], # replace string with num
        "onset" : onset,
        "apex" : hasApex( apex ),
        "offset" : offset
        }

    return accum, params
 
def hasApex( a ):
    if a == '/' :
        return None
    else:
        return int( a )


def isOnset( f, onset, apex ):
    return f in range( onset, apex )

def isApex( f, apex ):
    return f == apex

def isOffset( f, apex, offset ):
    return f in range( apex + 1, offset + 1 )

def getEmotion( vidEmotion, frameInfo  ):
    # Translation between string and integer reps of emotions
    emoji = { 'happiness' : 0,
            'disgust' : 1,
            'repression' : 2,
            'fear': 3,
            'sadness' : 4,
            'others' : 5,
            'surprise' : 6,
            'neutral' : 7
            }
    
    if frameInfo['isOnset'] or frameInfo['isApex'] or frameInfo['isOffset']:
        return emoji[ vidEmotion ]
    else:
        return emoji['neutral']
    



def getFrameParams( labelInfo, labelParams, f, frame ):
    if labelParams['apex'] is None:  #estimate halfway as apex
        apex =  int( math.floor( (labelParams['offset'] - labelParams['onset']) / 2 ) )
    else:
        apex = labelParams['apex']
    orgFrame =  map( int, re.findall( r'\d+', frame ))[0]                              
    accum = {
        "frame" : f,
        "isOnset" : isOnset( orgFrame, labelParams['onset'], apex ),
        "isApex" : isApex( orgFrame, labelParams['apex'] ),
        "isOffset" :  isOffset( orgFrame, apex, labelParams['offset'] )
        }

    accum.update( { "emotion" : getEmotion( labelParams[ 'emotion' ], accum) } )
    return accum


    

def generateGabor( nScales, nOrientations):
    ## get features
    ksize = 30
    ## 9 scales
    frequencies = [ ( math.pi / 2 ) / ( math.pow( math.sqrt( 2 ), u ) ) for u in range(nScales) ]
    ## 8 orientations
    thetas = [v * math.pi / 8 for v in range(nOrientations) ]
    sigma = 1 #average of sigmas shown in Shen2006MutualBoost
    # possibility of using ellipse formulation of sigma with major and minor axis components
    filters = []
    for f in frequencies :
        for th in thetas :
            filters.append (cv2.getGaborKernel( (ksize,ksize), sigma, th, 1 / f, 1 ) )
    return filters

### https://cvtuts.wordpress.com/2014/04/27/gabor-filters-a-practical-overview/

def process(img, filters):   ## apply all filters to one image
     accum = np.zeros_like(img)
     imgs = []
     for kern in filters:
         fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
         np.maximum(accum, fimg, accum)
         imgs.append( accum )     #instead of fimg
     return np.ravel( imgs ) 


def readInImg( imgPath ):
    img = cv2.imread( imgPath )
    img = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    if np.shape( img )[0] > 400:
        img = crop( img, 2.5, 2)
    # resize to 28ish * 23ish
    
    return img


def downsample( img, dim1, dim2 ):
    #img = cv2.resize( img, dsize= (dim,dim), fx = .1, fy = 0.1, interpolation = cv2.INTER_NEAREST )
    img = cv2.resize( img, dsize= (dim1,dim2), interpolation = cv2.INTER_NEAREST )
    return img

def crop( img, fh, fw ):       ## In terms of x, y not h, w !!!   # or the other way>>>
    ## USING FACES
    #face_cascade = cv2.CascadeClassifier('C:\\OpenCV\\data\\haarcascades\\haarcascade_frontalface_default.xml')
    #faces = face_cascade.detectMultiScale( img, 1.3, 5)
    #x,y,w,h = faces[0]
    #roi_gray = img[y:y+h, x:x+w]   
    
    ## USING EYES
    eye_cascade = cv2.CascadeClassifier('C:\\OpenCV\\data\\haarcascades\\haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale( img )

    eye1, eye2 = filterFoundEyes( eyes, img )
    d = Point.dist( eye1, eye2 )
#    print d
    newH = int(fh * d)  #set more firmly for other types of images for consistent size
    newW = int(fw * d)
    
    y0, x0 = newEyeLoc( eye1, eye2, newH, newW, d )
#    print newH, newW
    return img[ y0 : y0 + newH, x0 : x0  + newW ]

def newEyeLoc( eye1, eye2, newH, newW, d):
    if eye1.x < eye2.x:
        y0 = eye1.y - ( newH ) / 3
        x0 = eye1.x - ( newW - d )/2
    else:
        y0 = eye2.y - ( newH ) / 3
        x0 = eye2.x - ( newW - d )/2
    return y0, x0
        
    
    
    
    



#    im_toshow = copy.deepcopy( img )
#    cv2.circle( im_toshow, eye1, 10, (1,0,0) )
#    cv2.circle( im_toshow, eye2, 10, (0,1,0) )
#    plt.imshow( im_toshow, cmap = "gray" )
#    plt.show()
   
def areaRect( tup ):
    return tup[2] * tup[3]

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

    # cv2.circle( self.img, ( int(eye1loc.x), int(eye1loc.y) ), 1, (255,0,0) )
    # cv2.circle( self.img, ( int(eye2loc.x), int(eye2loc.y) ), 1, (255,0,0) )
    #showImg( im_toshow ) 
    return eye1loc, eye2loc         


                                                                           
def displayGabor( imgs ):
    for im in imgs:
        plt.imshow( im, cmap = 'gray' )
        plt.show()
    

DATA = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\Cropped\Cropped"
DATA1 = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\CASME2_RAW\CASME2-RAW"
DIR = "C:\Users\Valerie\Desktop\MicroExpress\CASME2"

NSCALES = 5
NORIENT =  8
D1 = 14
D2 = 11

excelFile = os.path.join( DIR, "CASME2-coding-20140508.xlsx")
table = pd.ExcelFile( excelFile )
t = table.parse( )

labelInfo  = {}
frameInfo = {}
featureInfo = np.array([ ] ).reshape( 0, NSCALES * NORIENT * D1 * D2 )


tf = 0
s = 0
for sub in os.listdir( DATA ): 
    v = 0
    for vid in os.listdir( os.path.join( DATA, sub ) ):
        if vid.endswith( "avi" ):
            break
        print vid   


        intLabelInfo, labelParams = getLabelInfo( sub, vid, t, [s, v] )
        f = 0
        for frame in os.listdir( os.path.join( DATA, sub, vid ) ):
            ## Skip avi's

            # Label Information
            # merge intLabelInfo and frameParams and assign frame number as key to avoid wiping out in update
            frameInfo = getFrameParams( intLabelInfo, labelParams, f, frame )
            frameInfo.update( intLabelInfo )
            labelInfo.update( { tf :  frameInfo } )
            img = downsample( readInImg( os.path.join( DATA, sub, vid, frame ) ), D1, D2 ) 
            featureInfo = np.vstack( [ featureInfo, process( img, generateGabor( NSCALES, NORIENT ) ) ])
            f += 1
            tf += 1
        v += 1
    s += 1


labels = pd.DataFrame.from_dict( labelInfo, orient = 'index' )

#labels[ (labels['video'] == 0) & (labels['subject'] == 0) ]


 
### AdaBoost
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import math
import pickle
 
clf = AdaBoostClassifier( 
    base_estimator = DecisionTreeClassifier( min_samples_leaf = 25, min_samples_split = 25),
    n_estimators = 50,
    algorithm='SAMME' )
X = featureInfo
Y = labels['emotion']
clf.fit( X, Y ) 


             