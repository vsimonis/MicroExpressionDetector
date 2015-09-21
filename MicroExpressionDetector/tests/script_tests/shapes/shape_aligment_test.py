import math
import numpy as np
from active_shape_models.ShapeAligner import ShapeAligner
from active_shape_models.ActiveShapeModel import ActiveShapeModel
from shapes.ActiveShape import ActiveShape

r = math.pi / 4
s = 1.2
t = [[-2],[4] ]

rMat = [ [ s * math.cos( r ), - s* math.sin( r ) ] ,
        [ s * math.sin( r ), s * math.cos( r ) ]] 

def p( x, y ):
    return [[x],[y]]

p1 = p( 1,1 )
p2 = p( 3,4 )
p3 = p( 4,2 )


def trans( p, rMat, t ):
    return np.dot( rMat, p ) + t


n1 = trans( p1, rMat, t)
n2 = trans( p2, rMat, t)
n3 = trans( p3, rMat, t)


AS1 = ActiveShape( [ (1,1), (3,4), (4,2) ] )
AS2 = ActiveShape( [(-2, 5.697), (-2.849, 9.940), (-0.303, 9.091 ) ])
ASM = ActiveShapeModel( [0,1] )
SA = ShapeAligner( ASM, 100, "" )

tdict = SA.calcAlignTransBtwn( AS2, AS1, np.ones( 3 ) ) 

