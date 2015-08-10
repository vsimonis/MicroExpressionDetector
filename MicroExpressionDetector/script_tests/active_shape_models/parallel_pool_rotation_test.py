#from pathos.multiprocessing import ProcessingPool as Pool
#import pathos.multiprocessing as mp

from pathos.multiprocessing import ProcessPool as Pool
from ActiveShapeModelsBetter import ASMB, Point, Shape
import dill


if __name__ == "__main__":
    asm = ASMB( [0,1],10 )
    asm.addShape(Shape([ Point( 100,200), Point(200,440), Point( 400,300)] ))
    p = Pool()
    p.map(Point.rotate, asm.allShapes, [[-1,1],[1,-1]]) 