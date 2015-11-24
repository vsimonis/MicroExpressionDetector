import pandas as pd
from data_parser.CASMELabels import CASMELabels
from feature_extraction.GaborWindowExtractor import GaborWindowExtractor, GaborExtractor
from image_processing.PreProcessing import PreProcessing as pp
import os
import numpy as np

class CASMEParser( object ):
    def __init__( self, method, nScales, nOrientations, imageResolution, nRects ): ## 5,8, 11, 14
        self.excelFile = "CASME2-coding-20140508.xlsx" 
        self.dataDir = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\Cropped\Cropped"
        #self.dataDir = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\CASME2_RAW\CASME2-RAW"
        self.mainDir = "C:\Users\Valerie\Desktop\MicroExpress\CASME2"
        self.nScales = nScales
        self.nOrient = nOrientations
        self.nRect = nRects
        self.imgRes = imageResolution
        ## DIMS needed?
        #self.dims = self.nScales * self.nOrient * self.scaledH * self.scaledW
        self.extractMethod = method

        dict = { "ImgRes" : GaborExtractor( nScales, nOrientations, 15 ), 
                "Rects" :  GaborWindowExtractor( nScales, nOrientations, 15, nRects ) }

        self.gabor = dict[ method ]

    def parseLabels( self ):
        ## Read in excel file to data frame
        excelFile = os.path.join( self.mainDir, self.excelFile )
        table = pd.ExcelFile( excelFile )
        t = table.parse( )


        ## Init parsed data containers
        labelInfo  = {}
        frameInfo = {}

        ## Iterate through images and build label frame
        
        tf = 0
        s = 0
        
        ## Iterate through files and generate labels and features

        ## For each subject
        for sub in os.listdir( self.dataDir ): 
            v = 0
            ## For each video 
            for vid in os.listdir( os.path.join( self.dataDir, sub ) ):
                if vid.endswith( "avi" ):   #skip avis
                    break
               
                ## Each line in main excel file proports to one video, get that info here
                intLabelInfo, labelParams = CASMELabels.getLabelInfo( sub, vid, t, [s, v] )
                f = 0
                
                ## Process each frame
                for frame in os.listdir( os.path.join( self.dataDir, sub, vid ) ):

                    frameInfo = CASMELabels.getFrameParams( intLabelInfo, labelParams, f, frame )
                    frameInfo.update( intLabelInfo )
                    labelInfo.update( { tf :  frameInfo } )
                    
                    f += 1
                    tf += 1
                v += 1
            s += 1
        return labelInfo

    def getFeatures( self ):
        img = pp.readInImg( os.path.join( self.dataDir, "sub01/EP02_01f/reg_img46.jpg" )    )
        if self.extractMethod == "ImgRes" : 
            #Probe sample image for dims
            
            self.nh, self.nw = pp.imgRes( img, self.imgRes )
            dims = self.nScales * self.nOrient * self.nh * self.nw

        elif self.extractMethod == "Rects" :
            dims = self.nOrient * self.nScales * self.nRect 
            self.nh, self.nw =  np.shape( img )

        featureInfo = np.array([ ] ).reshape( 0, dims )        
        ## Iterate through files and generate labels and features
        complete = True
        ## For each subject
        for sub in os.listdir( self.dataDir ): 
            ## For each video 
            for vid in os.listdir( os.path.join( self.dataDir, sub ) ):
                print vid
                if vid.endswith( "avi" ):   #skip avis
                    break
                ## Process each frame
                for frame in os.listdir( os.path.join( self.dataDir, sub, vid ) ):
                    img =  pp.readInImg( os.path.join( self.dataDir, sub, vid, frame ) )
                    if self.extractMethod == "ImgRes":
                        img = pp.downsample( img, self.nh, self.nw )
                    kernels = self.gabor.generateGaborKernels( )
                    try:
                        newFeatures = self.gabor.processGabor( img, kernels )
                        featureInfo = np.vstack( [ featureInfo, newFeatures ])     #control through dict of what method
                    except MemoryError:
                        complete = False
                        break

        return featureInfo, complete

    def run( self ):
        labelInfo = self.parseLabels()
        featureInfo, complete = self.getFeatures()
        return featureInfo, labelInfo, complete