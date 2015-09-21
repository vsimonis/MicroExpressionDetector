import numpy as np
import math

class Point( object ):

    def __init__( self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @classmethod
    def fromTuple( cls, tup ):
        x = tup[0]
        y = tup[1] 
        return cls( x, y )
        
    ## Properties (avoid need to update) 
    @property
    def p( self ):
        return ( self.__x, self.__y )

    @property
    def x( self ):
        return self.__x

    @property
    def y( self ):
        return self.__y

    def setY( self,y ):
        self.__y = y

    def setX( self,x ):
        self.__x = x

    @staticmethod
    def dist( p1, p2 ):
        return math.sqrt( (p1.x - p2.x)**2 + (p1.y - p2.y)**2 )

    def __str__(self):
        return '%f\t%f\n' % ( self.x, self.y )

