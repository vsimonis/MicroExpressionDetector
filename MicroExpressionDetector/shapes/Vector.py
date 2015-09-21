from Point import Point
import numpy as np
import math

class Vector( Point ):
    def __init__( self, *args, **kwargs):
        super( Vector, self ).__init__( *args, **kwargs)

    @property
    def v( self ):
        return [[ self.x ],[ self.y ]]

    def transform( self, transDict ):
        x1, y1 = np.add( np.dot( transDict['srot'], self.v ), transDict['t']   )
        return Vector( x1, y1 ) 

    def rotate( self, rot ): #as matrix
        x1, y1 = np.dot( rot , self.v )
        return Vector( x1, y1 )
    
    def M( self, scale, theta ):
        rotMat = self.calcSRotMat( scale, theta )
        return self.rotate( rotMat )

    def scale( self, scale ):
        x1, y1 = np.multiply( scale, self.v )
        return Vector( x1, y1 )

    def translate( self, vect ):
        x1, y1 = np.add( self.v, vect )
        return Vector( x1, y1 ) 

    @staticmethod
    def calcSRotMat( scale, theta ):
        d = scale * math.cos( theta )
        e = scale * math.sin( theta )
        sRotMat = [[ d, - e],
                  [ e,   d] ]

        return sRotMat

    @staticmethod
    def thetaFromRot( rotMat ):
        return math.atan2( rotMat[1][1], rotMat[1][0] )

    @staticmethod
    def unit( v ): 
        if v[0] == 0 and v[1] == 0:
            return v
        else:
            return v / np.linalg.norm( v )

    @staticmethod
    def angleBetween( v1, v2 ):
        return math.atan2( v1[0], v1[1] ) - math.atan2( v2[0], v2[1] )


