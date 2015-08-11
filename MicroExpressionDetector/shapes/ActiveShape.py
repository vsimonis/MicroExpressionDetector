from shapes.Shape import Shape
from shapes.Point import Point
import numpy as np

class ActiveShape( Shape ):
    def __init__( self, *args, **kwargs ):
        super( ActiveShape, self).__init__( *args, **kwargs)
        self.R = self.calcR()
    # Shape operations
    def transform( self, transformation ):
        return ActiveShape( map( lambda q : q.transform( transformation ), self.shapePoints ) )

    def rotate( self, rotation ):
        return ActiveShape( map( lambda q : q.rotate( rotation ), self.shapePoints ) )

    def translate( self, translation ):
        return ActiveShape( map( lambda q : q.translate( translation ) , self.shapePoints ) )

    def scale( self, scaling ):
        return ActiveShape( map( lambda q : q.scale( scaling ) , self.shapePoints ) )


    def calcR( self ):
        """
        Calculates distance matrix between all points for a given shape
        sets global variable 
        """
        sp = self.shapePoints
        ## For every point in shapePoints, calculate distance to other points
        R = [ [Point.dist( sp[k], sp[l] ) for k in range( self.n )] for l in range( self.n ) ]
        return R

    
    def calcDiff( self, shape ):
        objectShape = unravel( self )
        compShape = unravel( shape )
        diffAllPts = np.subtract( objectShape, compShape )
        return diffAllPts
     
    def calcSingleCov( self ):
        singleCov = np.dot( np.transpose(np.mat(self.diffAllPts)),  np.mat(self.diffAllPts) )
        return singleCov


