"""
Gets tallies on how many videos, etc... are in the directory tree
"""


import os
DATA = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\Cropped\Cropped"
DATA = "C:\Users\Valerie\Desktop\cropped2"

### NAVIGATING THE IMAGE DATA PATHS      (want to be recursive) 
ts = 0
v = 0
tv = 0
f = 0 
tf = 0

accum = {}
for sub in os.listdir( DATA ):

    ts +=  1
    v = 0
    for vid in os.listdir( os.path.join( DATA, sub ) ):
        v += 1
        tv += 1
        f = 0
        for frame in os.listdir( os.path.join( DATA, sub, vid ) ):
            f += 1
            tf += 1
        accum.update( {(sub, vid) : f} )
    accum.update( {sub : v} )
print ts
print tv
print tf



