from active_shape_models.ActiveShapeModel import ActiveShapeModel
from active_shape_models.ShapeAligner import ShapeAligner
from active_shape_models.ApplyASM import ApplyASM

from helpers.WriteUpHelper import WriteUp
from helpers.FileHelper import FileHelper
from helpers.DrawFace import DrawFace

from shapes.ActiveShape import ActiveShape

import logging
from matplotlib import pyplot as plt
import numpy as np
import os
import cv2
from collections import OrderedDict


""" 
Folder structure: 

> ASM: iters, training imgs, filtering
--> Deformation
--> PCA
--> SSD
-----> 7
-----> 5
-----> 3
--> Grad
-----> 5
-----> 10
-----> 15
"""

def trainingRun( ):
    train = True
    for filterPoints in [ True, False ]:
        for filterImages in [ True, False ] :
            process( filterPoints, filterImages, train, "",0,0 )

def applyRun( ):
    train = False
    for filterPoints in [ True, False ]:
        for filterImages in [ True, False ] :
            for method in [ "grad", "SSD", "nCorr" ] :
                if method == "grad":
                    for maxPx in [5,10,15,30,50]:
                        process( filterPoints, filterImages, train, method, maxPx, 0 )
                else :
                    for filter in [ 3,5,7 ]:
                        process( filterPoints, filterImages, train, method, 0, filter )

            
    

def getMethodSubFolder( params, output ):
    paramStr = ""
    paramStr += "%s-" % ( params["method"] )
    if params["method"] == 'grad':
        paramStr += "%s-%d" % ("maxPx", params["maxPx"]) 
    else: 
        paramStr += "%s-%d" % ("fSize", params["fSize"]) 
    sub = os.path.join( output, paramStr )
    if not params["trainASM"]:
        if not os.path.exists( sub ):
            os.mkdir( sub )
    return sub

                                                                   
def getASMfolder( params ):
    paramStr = ""
    for k,v in params.iteritems():
        if v and k in ["filterPts", "filterImgs"]:
            paramStr += "%s-" % k
    
    i = 0
    output = "C:\\Users\\Valerie\\Desktop\\output\\"
    study = "i-%d-t-%d-%ss-%d" % (  params["nIters"], params["nTrain"], paramStr, i )


    while os.path.exists( os.path.join( output, study )):
        study = "i-%d-t-%d-%ss-%d" % (  params["nIters"], params["nTrain"], paramStr, i )
        print study
        i += 1

    if params["trainASM"]: 
        os.mkdir( os.path.join( output, study ) )    
    else: 
        study = "i-%d-t-%d-%ss-%d" % (  params["nIters"], params["nTrain"], paramStr, i - 2 )

    output = os.path.join( output, study )
    return output


def process( fPts, fImgs, train, method, maxPx, fSize ):
    params ={ "nIters" : 7, 
              "nTrain" : 500,
              "filterPts" : fPts,
              "filterImgs" : fImgs,
              "trainASM" : train, 
              "writePCA" : True,
              "maxPx" : maxPx,
              "fSize" : fSize,
              "method" : method
              }


    params = OrderedDict( sorted( params.items(), key = lambda t : len(t[0]) ) )
    ##Methods: "SSD", "NCorr", or "grad"
    ASMout = getASMfolder( params )
    appASMout = getMethodSubFolder( params, ASMout )

    fh = FileHelper( params["nIters"], params["nTrain"], ASMout, params["filterPts"], params["filterImgs"] )

    if params["filterPts"]:
        asm = ActiveShapeModel( [43,35] ) 
    else: 
        asm = ActiveShapeModel( [36,31] )    

    if params["trainASM"]:
        asm = fh.readInPoints( asm )
        asm = ShapeAligner( asm, params["nIters"], ASMout ).alignTrainingSet( )
        fh.writeOutASM( asm ) #write out to read in later
    else: 
        asm = fh.readInASM( asm )

    ### Calculate Principal components

    asm.PCA()

    if params["trainASM"] or params["writePCA"]:
        ### Draw PCA stuffs
        if not os.path.exists( os.path.join( ASMout, "PCA" ) ) :
            os.mkdir( os.path.join( ASMout, "PCA" ) )
        wu = WriteUp( asm, fh )
        wu.PCAresults()

    if not params["trainASM"] :
        ### Apply ASM to image
        img = cv2.imread( "C:\Users\Valerie\Desktop\MicroExpress\CASME2\CASME2_RAW\CASME2-RAW\sub01\EP02_01f\img1.jpg")
        img =  cv2.cvtColor( img, cv2.COLOR_BGR2GRAY)
        appASM = ApplyASM( asm, params["nIters"], params["nTrain"],
                          appASMout, img, params['method'], 
                          params['maxPx'], params['fSize']  )
        appASM.applyASM()



#trainingRun()
applyRun()

