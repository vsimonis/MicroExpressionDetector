from Geometry import Shape, Point
from ActiveShapeModelsBetter import ASMB
import functools
import timeit

s = Shape( [ Point(200,300), Point( 150, 200), Point( 130,500) ] )


def add( x ,y) :
    return x + y

timeit.timeit('map( str , s.shapePoints )')
timeit.timeit('[str(x) for x in s.shapePoints ]')


map( add, s.shapePoints ) 


map( functools.partial( Point.rotate, [[ -1,1],[1,1]] ), s.shapePoints )