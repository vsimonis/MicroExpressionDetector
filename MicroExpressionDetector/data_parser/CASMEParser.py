import pandas as pd
from data_parser.CASMELabels import CASMELabels
from feature_extraction.GaborExtractor import GaborExtractor as gab
from image_processing.PreProcessing import PreProcessing as pp
import os
import numpy as np

class CASMEParser( object ):
    def __init__( self, nScales, nOrientations, downsampledH, downsampledW ): ## 5,8, 11, 14
        self.excelFile = "CASME2-coding-20140508.xlsx" 
        self.dataDir = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\Cropped\Cropped"
        #self.dataDir = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\CASME2_RAW\CASME2-RAW"
        self.mainDir = "C:\Users\Valerie\Desktop\MicroExpress\CASME2"
        self.nScales = nScales
        self.nOrient = nOrientations
        self.scaledH = downsampledH
        self.scaledW = downsampledW
        self.dims = self.nScales * self.nOrient * self.scaledH * self.scaledW
        self.gabor = gab( nScales, nOrientations, 15 )

    def run( self ):
        ## Read in excel file to data frame
        excelFile = os.path.join( self.mainDir, self.excelFile )
        table = pd.ExcelFile( excelFile )
        t = table.parse( )


        ## Init parsed data containers
        labelInfo  = {}
        frameInfo = {}
        featureInfo = np.array([ ] ).reshape( 0, self.dims )

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
                print vid   
                ## Each line in main excel file proports to one video, get that info here
                intLabelInfo, labelParams = CASMELabels.getLabelInfo( sub, vid, t, [s, v] )
                f = 0
                
                ## Process each frame
                for frame in os.listdir( os.path.join( self.dataDir, sub, vid ) ):

                    frameInfo = CASMELabels.getFrameParams( intLabelInfo, labelParams, f, frame )
                    frameInfo.update( intLabelInfo )
                    labelInfo.update( { tf :  frameInfo } )
                    img = pp.downsample( pp.readInImg( os.path.join( self.dataDir, sub, vid, frame ) ), self.scaledH, self.scaledW ) 
                    kernels = self.gabor.generateGaborKernels( ) 
                    featureInfo = np.vstack( [ featureInfo, gab.processGabor( img, kernels ) ])
                    f += 1
                    tf += 1
                v += 1
            s += 1

            return featureInfo, labelInfo