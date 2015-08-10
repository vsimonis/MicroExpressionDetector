from ActiveShapeModels import ASM, Point, Shape
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np

#s1 = Shape( [ Point(200,300), Point(100, 200), Point(300, 50 ) ] )
#s2 = Shape( [ Point(150,250), Point(50, 100 ), Point(250, 0) ] )



s1 = Shape( [ Point(857, -129), Point(89,-409), Point(-404,254), Point( 96,957), Point(877,712) ])

f, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)

s1.draw( sns.xkcd_palette( ["light blue" ]), 0, ax1)
#s2.draw( sns.xkcd_palette( ["light blue"] ), ax2)

cmShape  = ASM.centroid( s1 )
#cmMeanShape = ASM.centroid( s2  )


ax1.scatter( cmShape.x, cmShape.y, c='r')
#ax2.scatter( cmMeanShape.x, cmMeanShape.y, c='r')
ax1.plot( [s1.shapePoints[0].x, s1.shapePoints[1].x],
         [s1.shapePoints[0].y, s1.shapePoints[1].y],
         color= 'r', ls = '-')

#ax2.plot( [s2.shapePoints[0].x, s2.shapePoints[1].x],
#         [s2.shapePoints[0].y, s2.shapePoints[1].y],
#         color= 'r', lw = 1, ls = '-')


t = [[ -cmShape.x ], [ -cmShape.y ]] 
        
## Scale
d1 = s1.shapePoints[0].dist( s1.shapePoints[1] )
#d2 = s2.shapePoints[0].dist( s2.shapePoints[1] )
s = 1/d1
        
## Rotation
#http://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
p0 = [ s1.shapePoints[0].x, s1.shapePoints[0].y ]
#m0 = [ s2.shapePoints[0].x, s2.shapePoints[0].y ]
axisVector = [ 1, 0 ]
        
thetaP = ASM.angleV( p0, axisVector )
#thetaM = ASM.angleV( m0, axisVector )

thetaRot = math.pi / 2 - thetaP

rot = [[ math.cos( thetaRot ), -math.sin( thetaRot ) ],
        [ math.sin( thetaRot ), math.cos( thetaRot ) ] ]

#d= { 'rot' : np.multiply( s , rot) , 't': t}
#s1.applyTrans( d )A


for pt in s1.shapePoints:
    pt.translate( t )
s1.update()
s1.draw( sns.xkcd_palette( ["light blue"] ), 0, ax2)

for pt in s1.shapePoints:
    pt.rotate( rot )
s1.update()
s1.draw( sns.xkcd_palette( ["light blue"] ), 0, ax3)




cmMeanShape1 = ASM.centroid( s1 )
ax2.scatter( cmMeanShape1.x, cmMeanShape1.y, c='r')
ax2.plot( [s1.shapePoints[0].x, s1.shapePoints[1].x],
         [s1.shapePoints[0].y, s1.shapePoints[1].y],
         color= 'r', lw = 1, ls = '-')

plt.show()

### Checks 
print d1
print d2 
print s2.shapePoints[0].dist( s2.shapePoints[1] ) #should be == d1

print thetaP
print thetaM
print ASM.angleV([ s2.shapePoints[0].x, s2.shapePoints[0].y ], axisVector )

plt.show()
