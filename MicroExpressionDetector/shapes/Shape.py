import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
from shapes.Point import Point
from shapes.Vector import Vector

class Shape( object ):
    """
    Shape object
    """                         

    def __init__(self, pointList ):

        self.shapePoints = []
        
        # Add points to shape

        if isinstance( pointList[0], list):
            for [x,y] in pointList:
                self.shapePoints.append( Vector(x,y) )
        elif isinstance( pointList[0], tuple):
            for (x,y) in pointList:
                self.shapePoints.append( Vector(x,y) )
        
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

    @staticmethod
    def unravel( pointList ):
        allPts = []                      
        for pt in pointList:
            allPts.append( pt.x )
            allPts.append( pt.y )
        return allPts 

    
    def flatten( self ):
        return self.unravel( self.shapePoints )


    
    def draw( self, palette, axis ):
        _ = axis.scatter( self.xs, self.ys, c = palette, s= 3 )


    def __str__( self ):
        a = map( str, self.shapePoints )
        return ''.join( a )




