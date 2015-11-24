import os
import pandas as pd

DATA = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\Cropped\Cropped"
DATA = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\CASME2_RAW\CASME2-RAW"
DATA = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\CASME2_RAW_selected\CASME2_RAW_selected"
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
        if vid.endswith( "avi" ):
            pass
        else: 
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

pd.DataFrame.from_dict( accum, orient = 'index' )


