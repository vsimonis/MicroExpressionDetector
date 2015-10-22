import cv2
import os
import pandas as pd
import math
import numpy as np
from matplotlib import pyplot as plt
import re
  
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
    # resize to 28ish * 23ish
    img = cv2.resize( img, dsize= (0,0), fx = .1, fy = 0.1, interpolation = cv2.INTER_NEAREST )
    return img


def readInVideo( vidPath ):
        CASCADE='C:\\OpenCV\\data\\haarcascades\\haarcascade_frontalface_default.xml'


def displayGabor( imgs ):
    for im in imgs:
        plt.imshow( im, cmap = 'gray' )
        plt.show()
    

DATA = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\Cropped\Cropped"
DATA1 = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\CASME2_RAW\CASME2-RAW"
DIR = "C:\Users\Valerie\Desktop\MicroExpress\CASME2"


excelFile = os.path.join( DIR, "CASME2-coding-20140508.xlsx")
table = pd.ExcelFile( excelFile )
t = table.parse( )

labelInfo  = {}
frameInfo = {}
featureInfo = []


tf = 0
s = 0
for sub in os.listdir( DATA ): 
    v = 0
    for vid in os.listdir( os.path.join( DATA, sub ) ):
        intLabelInfo, labelParams = getLabelInfo( sub, vid, t, [s, v] )
        f = 0
        for frame in os.listdir( os.path.join( DATA, sub, vid ) ):
            # Label Information
            # merge intLabelInfo and frameParams and assign frame number as key to avoid wiping out in update
            frameInfo = getFrameParams( intLabelInfo, labelParams, f, frame )
            frameInfo.update( intLabelInfo )
            labelInfo.update( { tf :  frameInfo } )
           
            featureInfo.append( process( readInImg( os.path.join( DATA, sub, vid, frame)  ), generateGabor( 9, 8 ) ) )
            f += 1
            tf += 1
        v += 1
    s += 1


labels = pd.DataFrame.from_dict( labelInfo, orient = 'index' )

labels[ (labels['video'] == 0) & (labels['subject'] == 0) ]


        