import pandas as pd
from data_parser.CASMELabels import CASMELabels
from feature_extraction.GaborWindowExtractor import GaborWindowExtractor, GaborExtractor
from image_processing.PreProcessing import PreProcessing as pp
import os
import numpy as np

class CASMEParserMem( object ):
    def __init__( self, nScales, nOrientations ) :
        self.excelFile = "CASME2-coding-20140508.xlsx" 
        self.dataDir = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\Cropped\Cropped"
        #self.dataDir = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\CASME2_RAW\CASME2-RAW"
        self.mainDir = "C:\Users\Valerie\Desktop\MicroExpress\CASME2"
        self.nScales = nScales
        self.nOrient = nOrientations
        self.featureOut = "F:\output"
        self.gabor = GaborExtractor( nScales, nOrientations, 21)

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

    def writeFeatures( self ):
        img = pp.readInImg( os.path.join( self.dataDir, "sub01/EP02_01f/reg_img46.jpg" )    )

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
                    kernels = self.gabor.generateGaborKernels( )

                    newFeatures = np.ravel(self.gabor.processGaborRaw( img, kernels )  )
                    featStr = map( lambda x : '%.15f' % x, newFeatures )
                    featOut = str.join( ',' , featStr )
                    f = open( os.path.join( self.featureOut, "Gabors-S%d-O%d.csv" % (self.nScales, self.nOrient)), "a" )
                    
                    f.write( "%s\n" % featOut )
                    f.close()
                    
    def run( self ):
        labelInfo = self.parseLabels()
        self.writeFeatures()
        return labelInfo