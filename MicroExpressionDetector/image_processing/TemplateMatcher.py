from helpers.FileHelper import FileHelper
from shapes.ActiveShape import ActiveShape
from shapes.Vector import Vector
from pathos.multiprocessing import ProcessingPool as PPool
import numpy as np 
import math
import time

class TemplateMatcher(object):
    def __init__( self, method, n ):

        ## Training
        self.ebenImg, self.ebenShape = TemplateMatcher.getEben()
        #self.templates = self.genTemplates() 
        self.method = method
        self.n = n
                                                                            

    def performMatching( self, I, model ):
        r = self.genRegionsArr( I, model )
        t = self.genTemplatesArr()
        
        matchesDx = PPool().map( self.match, r,t )
        return np.ravel( matchesDx )

    def match( self, r, t):
        ixs = TemplateMatcher.matIxs( self.n ** 2 )
        ix = 0
        ws = map( lambda x : TemplateMatcher.slice( r, self.n, x ), ixs )
        if self.method == "SSD" :
            resp = map( lambda w : self.SSD( t, w ), ws )
            ix = np.argmin( resp )
        else : 
            resp = map( lambda w : self.normCorr( t, w ), ws )
            ix = np.argmin( resp )

        return TemplateMatcher.coordOffset(ixs[ix], self.n ** 2)


            
    def processRegionSSD( self, r ):
        """
        Matches each point in the region to minimum SSD template from entire list of templates
        """
        ixs = TemplateMatcher.matIxs( self.n ** 2 )
        ## 5 x 5 windows for region r
        ws = map( lambda x : TemplateMatcher.slice( r, self.n, x ), ixs )

        ts = map(  lambda w : map( lambda t : TemplateMatcher.SSD( t, w ), self.templates ) , ws)
        tMatch = map( lambda x : np.argmin( x, axis = 0), ts )
        lMatch = map( lambda x : np.min( x, axis = 0) ,ts )
        ix = np.argmin( lMatch )
        return TemplateMatcher.coordOffset(ixs[ix], self.n ** 2)#, tMatch[ix] ixs[ix].x, ixs[ix].y, tMatch[ix]

    def processRegionNormCorr( self, r ):
        ixs = TemplateMatcher.matIxs( self.n ** 2 )
        ## 5 x 5 windows for region r
        ws = map( lambda x : TemplateMatcher.slice( r, self.n, x ), ixs )

        ts = map(  lambda w : map( lambda t : self.normCorr( t, w ), self.templates ) , ws)
        tMatch = map( lambda x : np.argmax( x, axis = 0), ts )
        lMatch = map( lambda x : np.max( x, axis = 0) ,ts )
        ix = np.argmax( lMatch )
        return  TemplateMatcher.coordOffset(ixs[ix], self.n**2)#, tMatch[ix]
        
        



    def performMatchingOld( self, I, model ):
        start = time.time()  
        ixs = TemplateMatcher.matIxs( self.n ** 2 )
        if self.method == "SSD":
            stuff = PPool().map( self.processRegionSSD, self.genRegionsArr(I, model) ) 
        else:
            stuff = PPool().map( self.processRegionNormCorr, self.genRegionsArr(I, model) ) 
        print "match: %f" % ( time.time() - start)
        return stuff

    

    def genRegionsArr( self, I, model ):
        regions = []
        for pt in model.shapePoints :
            regions.append( TemplateMatcher.slice( I, self.n, pt ) )
        return regions


    def genTemplatesArr( self ):
        templates = []
        for pt in self.ebenShape.shapePoints :
            templates.append( TemplateMatcher.slice( self.ebenImg, self.n, pt ) )
        return templates

    def genTemplatesDict( self ):
        templates = {}
        ix = 0
        for pt in self.ebenShape.shapePoints :
            templates.update( { ix :  TemplateMatcher.slice( self.ebenImg, 5, pt ) } )
        return templates


    @staticmethod
    def getEben( ):
        i = 20
        tr = 500
        out =    "C:\\Users\\Valerie\\Desktop\\output\\20-500-1" 
        ### END OF NEED?
        fh = FileHelper( i, tr, out, False,False ) 
        trainImg = fh.readInEbenImg()
        trainPts = fh.readInOneDude( '000_1_1.pts')  
        return trainImg, ActiveShape( trainPts )
   
    ### Matrix Manipulation
    @staticmethod
    def hinge( v, n ):
        # return lower and upper bounds of n x n region around float/int v
        lower = int(round(v) - math.floor( n / 2 ))
        upper = int(round(v) + math.floor( n / 2 ))
        return lower, upper

    @staticmethod
    def slice( mat, n, pt ):
        """
        Slices matrix centered around point pt to have size nxn
        If area includes the edge of imaged area, 0 padded rows/cols
        are added
        
        
           lc           uc
        lr --------------
           |
           |
           |
        ur --------------
        """
        
        lc, uc = TemplateMatcher.hinge( pt.x, n ) ## column limits
        lr, ur = TemplateMatcher.hinge( pt.y, n )
        nr, nc = np.shape( mat )
        nr = nr - 1
        nc = nc - 1
    
        alc, auc = lc, uc 
        alr, aur = lr, ur 
        rpb, rpa, cpl, cpr = [0,0,0,0]

        if lc < 0:
            alc = 0
            cpl = -lc 

        if uc > nc:
            auc = nc 
            cpr = uc - auc 

        if lr < 0:
            alr = 0
            rpb = -lr

        if ur > nr:
            aur = nr 
            rpa = ur - aur 

        return np.pad( mat[ alr : aur + 1 , alc : auc + 1 ], (( rpb, rpa ),( cpl, cpr )), mode ='constant' )



    ## http://stackoverflow.com/questions/28995146/matlab-ind2sub-equivalent-in-python
    def ind2sub(array_shape, ind):
        rows = (int(ind) / array_shape[1])
        cols = (int(ind) % array_shape[1]) # or numpy.mod(ind.astype('int'), array_shape[1])
        return (rows, cols)
    

    def normCorr( self, template, image ):
        t = np.ravel( template - np.mean( template ))
        nt = math.sqrt( sum( t ** 2 ) )
        i = np.ravel( image - np.mean( image )) 
        ni = math.sqrt( sum( i ** 2 ) )
        if ni == 0 or nt == 0:
            return 0
        th = np.divide( t, nt )
        ih = np.divide( i, ni )
        return sum ( th * ih )

    @staticmethod
    def SSD( template, image ):
        t = np.ravel(template - np.mean( template ))
        i = np.ravel(image - np.mean( image ))
        return sum( ( t - i ) ** 2 )

    @staticmethod    
    def matIxs( n ):
        """
        Given region of size n x n, returns all col, row indices for iteration

        x --> col
        y --> row
        """
        rows, cols = np.indices( (n,n) )
        row = rows.flatten()
        col = cols.flatten()
        
        return map( lambda x: Vector( x[0], x[1] ), zip( col, row )  )

    @staticmethod
    def coordOffset( pt, n ):
        y = pt.y   #row
        x = pt.x   #col
        return Vector.unit( [[ x - ( n - 1) / 2],[ y - ( n - 1 ) / 2  ] ])

    def corr( template, image ):
        t = np.ravel( template - np.mean( template ))
        i = np.ravel( image - np.mean( image )) 
        return sum( t * i )


        




