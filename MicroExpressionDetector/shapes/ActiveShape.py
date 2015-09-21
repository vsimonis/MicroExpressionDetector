from shapes.Shape import Shape
from shapes.Point import Point
from shapes.Vector import Vector
import numpy as np

class ActiveShape( Shape ):
    def __init__( self, *args, **kwargs ):
        super( ActiveShape, self).__init__( *args, **kwargs)
        self.R = self.calcR()
    # Shape operations
    def transform( self, transformation ):
        return ActiveShape( map( lambda q : q.transform( transformation ), self.shapePoints ) )

    def M( self, scaling, theta ):
        return ActiveShape( map( lambda q : q.M( scaling, theta ), self.shapePoints ) )

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


    def shapeDist( self, shape ):
        d = map( lambda x, y : Point.dist( x,y ), self.shapePoints, shape.shapePoints )
        return d
        
    def calcSingleCov( self, shape ):
        # Difference from mean shape
        objectShape = self.unravel( self.shapePoints )
        compShape = self.unravel( shape.shapePoints )
        diffAllPts = np.subtract( objectShape, compShape )
        singleCov =  np.dot( np.transpose(np.mat(diffAllPts)),  np.mat(diffAllPts) )
        return singleCov
     
    @staticmethod
    def deravel( vect ):
        x, y = [], []
        for i in range( len( vect ) ):
            if i % 2 == 0:
                x.append( vect[i] )
            else: 
                y.append( vect[i] )
        return x, y
           
    @classmethod
    def createShape( cls, allPts ):
        xs,ys = cls.deravel( allPts )
        return cls( zip( xs, ys) )
