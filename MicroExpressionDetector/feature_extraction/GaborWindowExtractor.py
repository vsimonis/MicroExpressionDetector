from feature_extraction.GaborExtractor import GaborExtractor
import numpy as np
import copy

class GaborWindowExtractor( GaborExtractor ):
    def __init__( self,  nScales, nOrientations, kernelSize, nRects):
        GaborExtractor.__init__(self, nScales, nOrientations, kernelSize )
        self.numRects = nRects


    def getRectangleParams( self, img ): ## only works with even numRects
        nrect = copy.deepcopy( self.numRects )
        nrows = 0
        ncols = 0
        cs = np.shape( img )
        cs = list( cs )
        while nrect != 1:
            maxIx = np.argmax( cs )
            self.replace( cs, 2, maxIx )
            if maxIx == 0:
                nrows += 1
            else:   
                ncols += 1
            nrect /= 2

        return cs, (2 ** nrows, 2 ** ncols)

    @staticmethod
    def replace( vect, mult, maxIx):
        v = vect.pop( maxIx)
        vect.insert( maxIx, v / mult )

  
    @staticmethod
    def sliceImg( img, rectSize, rectIx ):
        slices = []
        for nr in range( rectIx[0] ):
            for nc in range( rectIx[1] ):
                slices.append( list( img[ nr * rectSize[0] + nr :  nr * rectSize[0] + nr + rectSize[0],
                                    nc * rectSize[1] + nc :  nc * rectSize[1] + nc + rectSize[1]] ) )                              
        return slices        

    @staticmethod
    def findMaxMag( fImg ):
        return np.argmax( fImg )

    @staticmethod
    def getResponseVals( fImg, maxLoc):
        return fImg[ maxLoc[0] ][ maxLoc[1] ]


    def processGabor( self, img, filters ):

        imgs = self.processGaborRaw( img, filters )

        fVect = []
        for fIx, fImg in enumerate( imgs ):

            o,s = self.getOrientationScaleIx( fIx, self.nOrientations, self.nScales )

            maxLocs = []
            rsize,  rIx = self.getRectangleParams( fImg )

            slices = self.sliceImg( fImg, rsize, rIx )
            for sliceIx, slice in enumerate(slices):
 
                sliceR, sliceC = np.shape( slice )
                if s == 0:
                    maxLoc = self.findMaxMag( slice )
                    maxLoc = self.ind2sub( maxLoc, sliceR, sliceC )
            

                fVect.append( self.getResponseVals( fImg ,maxLoc) )

        return fVect

    #http://stackoverflow.com/questions/28995146/matlab-ind2sub-equivalent-in-python
    @staticmethod
    def getOrientationScaleIx( ix, no, ns ):
        return GaborWindowExtractor.ind2sub( ix, no, ns )

    ## Given number of rectangles wanted, returns 
    @staticmethod
    def ind2sub( ix, nrows, ncols ):
        row = ix / ncols
        col = ix % ncols # or numpy.mod(ind.astype('int'), array_shape[1])
        return (row, col)

