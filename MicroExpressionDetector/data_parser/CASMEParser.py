import pandas as pd
from data_parser.CASMELabels import CASMELabels
from feature_extraction.GaborExtractor import GaborExtractor as gab
from image_processing.PreProcessing import PreProcessing as pp
import os
import numpy as np

class CASMEParser( object ):
    def __init__( self, nScales, nOrientations, imageResolution ): ## 5,8, 11, 14
        self.excelFile = "CASME2-coding-20140508.xlsx" 
        self.dataDir = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\Cropped\Cropped"
        #self.dataDir = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\CASME2_RAW\CASME2-RAW"
        self.mainDir = "C:\Users\Valerie\Desktop\MicroExpress\CASME2"
        self.nScales = nScales
        self.nOrient = nOrientations
        self.imgRes = imageResolution
        ## DIMS needed?
        #self.dims = self.nScales * self.nOrient * self.scaledH * self.scaledW
        self.gabor = gab( nScales, nOrientations, 15 )
    

    
    def run( self ):
        ## Read in excel file to data frame
        excelFile = os.path.join( self.mainDir, self.excelFile )
        table = pd.ExcelFile( excelFile )
        t = table.parse( )


        ## Init parsed data containers
        labelInfo  = {}
        frameInfo = {}

        #Probe sample image for dims
        img = pp.readInImg( os.path.join( self.dataDir, "sub01/EP02_01f/reg_img46.jpg" )    )
        self.nh, self.nw = pp.imgRes( img, self.imgRes )
        dims = self.nScales * self.nOrient * self.nh * self.nw
        featureInfo = np.array([ ] ).reshape( 0, dims )


        tf = 0
        s = 0
        
        ## Iterate through files and generate labels and features
        complete = True
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
                    img =  pp.readInImg( os.path.join( self.dataDir, sub, vid, frame ) )
                    img = pp.downsample( img, self.nh, self.nw ) 
                    

                    kernels = self.gabor.generateGaborKernels( ) 
                    try:
                        featureInfo = np.vstack( [ featureInfo, gab.processGabor( img, kernels ) ])
                    except MemoryError:
                        #print "S%d   O%d    H%d    W%d.csv" % (self.nScales, self.nOrient, self.nh, self.nw )
                        complete = False
                        break
                    f += 1
                    tf += 1
                v += 1
            s += 1

        return featureInfo, labelInfo, complete