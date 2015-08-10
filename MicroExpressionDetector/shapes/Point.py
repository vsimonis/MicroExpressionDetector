import numpy as np
import math

class Point( object ):

    def __init__( self, x, y):
        self.__x = float(x)
        self.__y = float(y)
        
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
        #print 'new y'

    def setX( self,x ):
        self.__x = x
        #punrint 'new x'

    def dist( self, pt):
        return math.sqrt( (self.__x - pt.x)**2 + (self.__y - pt.y)**2 )
    

    def __str__(self):
        return '%f\t%f\n' % ( self.x, self.y )

