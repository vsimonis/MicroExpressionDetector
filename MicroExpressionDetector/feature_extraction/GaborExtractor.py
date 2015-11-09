import math
import cv2
import numpy as np

class GaborExtractor( object ):
    def __init__( self, nScales, nOrientations, kernelSize):
        self.nScales = nScales
        self.nOrientations = nOrientations
        self.kSize = kernelSize
        

    def generateGaborKernels( self ):
        ## scales
        frequencies = [ ( math.pi / 2 ) / ( math.pow( math.sqrt( 2 ), u ) ) for u in range(self.nScales) ]
        
        ## orientations
        thetas = [v * math.pi / 8 for v in range(self.nOrientations) ]
        sigma = 1 #average of sigmas shown in Shen2006MutualBoost
        
        # possibility of using ellipse formulation of sigma with major and minor axis components
        # orientations first then scales!!!
        filters = []
        for th in thetas :
            for f in frequencies :
                filters.append (cv2.getGaborKernel( (self.kSize,self.kSize), sigma, th, 1 / f, 1 ) )
        return filters

    ### https://cvtuts.wordpress.com/2014/04/27/gabor-filters-a-practical-overview/
    @staticmethod
    def processGabor(img, filters):   ## apply all filters to one image
         accum = np.zeros_like(img)
         imgs = []
         for kern in filters:
             fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
             np.maximum(accum, fimg, accum)
             imgs.append( accum )     #instead of fimg
         return np.ravel( imgs ) 

    @staticmethod
    def processGaborRaw( img, filters):
        imgs = []
        for kern in filters:
            fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
            imgs.append( fimg )
        return imgs

    
         