import numpy as np
from pathos.multiprocessing import ProcessingPool as PPool
import functools

class SimpleASM ( object ):
    def __init__( self, listOfShapes ):
        self.shapeList = listOfShapes

    def scale( self, scaling ):
        return PPool().map( lambda line: SimpleShape( PPool().map( lambda x :  x.scale( scaling ) ,  line)), map( lambda y : y.pointList, self.shapeList ) )

    def rotate( self, rotation ):
        return map( lambda line: SimpleShape( PPool().map( lambda x :  x.scale( rotation ) ,  line)), PPool().map( lambda y : y.pointList, self.shapeList ) )
        
    def translate( self, translation ):
        return map( lambda line: SimpleShape( PPool().map( lambda x :  x.scale( translation ) ,  line)), PPool().map( lambda y : y.pointList, self.shapeList ) )

class SimpleShape ( object ):
    def __init__( self, listOfPoints ):
        self.pointList = listOfPoints

    #def scale( self, scaling ):
        #result = Pool().amap( lambda x: 
        #result = p.amap( lambda x : x.scale( scaling ), self.pointList ).get()


class SimplePoint( object ):
    def __init__( self, tupleOfCoords ):
        self.coords = tupleOfCoords 

    @property
    def x( self ):
        return self.coords[0]


    @property
    def y( self ):
        return self.coords[1]


    def scale( self, scaling ):
        x,y = np.multiply( scaling, [self.x, self.y] )
        print "done" 
        return SimplePoint( (x,y))
    

