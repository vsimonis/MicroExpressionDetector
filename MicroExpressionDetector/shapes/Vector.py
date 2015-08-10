from Point import Point
import numpy as np
import math

class Vector(Point):
    def __init__( self, *args, **kwargs):
        super( Vector, self ).__init__( *args, **kwargs)

    @property
    def v( self ):
        return [[ self.__x ],[ self.__y ]]

    def transform( self, transDict ):
        x1, y1 = np.dot( transDict['rot'], self.v ) + transDict['t']
        return Point( x1, y1 )

    def rotate( self, rot ):
        x1, y1 = np.dot( rot , self.v )
        return Point( x1, y1 )

    def scale( self, scale ):
        x1, y1 = np.multiply( scale, self.v )
        return Point( x1, y1 )

    def translate( self, vect ):
        x1, y1 = np.add( self.v, vect )
        return Point( x1, y1 ) 


    @staticmethod
    def unit( v ): 
        if v[0] == 0 and v[1] == 0:
            return v
        else:
            return v / np.linalg.norm( v )

    @staticmethod
    def angleBetween( v1, v2 ):
        return math.atan2( v1[0], v1[1] ) - math.atan2( v2[0], v2[1] )


