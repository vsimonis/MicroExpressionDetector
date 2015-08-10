import numpy as np
import math

def unitV( v ): 
    return v / np.linalg.norm( v )

def angleVcp( v1, v2 ):
    v1_u = unitV( v1 )
    v2_u = unitV(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle

def angleVtan( v1, v2 ):
        
    return math.atan2( v1[0], v1[1] ) - math.atan2( v2[0], v2[1] )
""""
 q2 | q1
---------
 q3 | q4
"""  

q1 = ( 3, 4 )
q2 = ( -3, 4 )
q3 = ( -3, -4 )
q4 = ( 3, -4 )

ref = ( 0, 1 )

### Cross product method
print "q1: %f" % math.degrees( angleVcp( q1, ref ))
print "q2: %f" % math.degrees( angleVcp( q2, ref ))
print "q3: %f" % math.degrees( angleVcp( q3, ref ))
print "q4: %f" % math.degrees( angleVcp( q4, ref ))


### tan method
print "q1: %f" % math.degrees( angleVtan( q1, ref ))
print "q2: %f" % math.degrees( angleVtan( q2, ref ))
print "q3: %f" % math.degrees( angleVtan( q3, ref ))
print "q4: %f" % math.degrees( angleVtan( q4, ref ))