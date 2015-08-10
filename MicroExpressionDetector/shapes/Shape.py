import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
from Point import Point

class Shape( object ):
    """
    Shape object

    Data members:
    - shapePoints
    - R
    - allPoints
    - diffAllPoints
    
    """

    def __init__(self, pointList ):

        self.shapePoints = []
        
        # Add points to shape
        if isinstance( pointList[0], list):
            for [x,y] in pointList:
                self.shapePoints.append( Point(x,y) )
        elif isinstance( pointList[0], tuple):
            for (x,y) in pointList:
                self.shapePoints.append( Point(x,y) )
        else:
            self.shapePoints = pointList
        
    @property
    def xs( self ):
        """
        returns all x values of all points for a given shape
        """
        return map( lambda pt : pt.x, self.shapePoints )

    @property
    def ys( self ):
        """
        returns all y values of all points for a given shape
        """
        return map( lambda pt : pt.y, self.shapePoints )

    @property
    def n( self ):
        """
        returns the number of points in a given shape
        """
        return len( self.shapePoints )
    
    
    def centroid( self ):
        return Point( np.mean( self.xs ) , np.mean( self.ys ) )

    def unravel( self ):
        allPts = []
        for pt in self.shapePoints:
            allPts.append( pt.x)
            allPts.append( pt.y )
        return allPts 


    # Shape operations
    def transform( self, transformation ):
        return map( lambda q : q.transform( transformation ), self.shapePoints )

    def rotate( self, rotation ):
        return map( lambda q : q.rotate( rotation ), self.shapePoints )

    def translate( self, translation ):
        return map( lambda q : q.translate( translation ) , self.shapePoints )

    def scale( self, scaling ):
        return map( lambda q : q.scale( scaling ) , self.shapePoints )


    def draw( self, palette, axis ):
        _ = axis.scatter( self.xs, self.ys, c = palette, s= 10 )


    def __str__( self ):
        a = map( str, self.shapePoints )
        return ''.join( a )




