### Filter out training images

from active_shape_models.ActiveShapeModel import ActiveShapeModel
from active_shape_models.ShapeAligner import ShapeAligner
from active_shape_models.ApplyASM import ApplyASM

from helpers.WriteUpHelper import WriteUp
from helpers.FileHelper import FileHelper
from helpers.DrawFace import DrawFace

from shapes.ActiveShape import ActiveShape

import logging
from matplotlib import pyplot as plt
import numpy as np
import os

output = "C:\\Users\\Valerie\\Desktop\\output\\"
iters = 4
training = 500

train = True
write = False
align = True

i = 0
study = "%d-%d-%d" % ( iters, training, i )
if not os.path.exists( os.path.join( output, study ) ) and (train or align ):
    os.mkdir( os.path.join( output, study ) )
    output = os.path.join( output, study )
else:                       
    while os.path.exists( os.path.join( output, study )):
        i += 1
        study = "%d-%d-%d" % ( iters, training, i )
        if train or align:
            os.mkdir( os.path.join( output, study ) )
        else: 
            study = "%d-%d-%d" % ( iters, training, i )
        output =  os.path.join( output, study )



fh = FileHelper( iters, training , output )

if train:
    asm = ActiveShapeModel( [36,31] )
    asm = fh.readInPoints( asm )

### Align Shapes
if align:
    asm = ShapeAligner( asm, iters, output ).alignTrainingSet( )
    fh.writeOutASM( asm ) #write out to read in later


d = map( lambda x: x.shapeDist( asm.normMeanShape ), asm.allShapes )
d1 = np.mean( d, 1 )

min = np.min( d1 )
mn = np.mean( d1 )
q1 = np.percentile( d1, 0.25)
sd = np.std( d1 )
max = np.max( d1 )
q3 = np.percentile( d1, 0.75)
iqr = q3 - q1

cu1 = mn + 2*sd
cu2 = mn + 3*sd

i1 = np.where( d1 > cu1 )[0]
i2 = np.where( d1 > cu2 )[0]

f, (ax1, ax2) = plt.subplots( 1,2, sharex=True, sharey = True )

for ix in list(i1):
    DrawFace( asm.allShapes[ ix ], ax1 ).drawContrast()
for ix in list(i2):
    DrawFace( asm.allShapes[ ix ], ax2 ).drawContrast()

DrawFace( asm.meanShape, ax1).drawBold()
DrawFace( asm.meanShape, ax2).drawBold()

plt.show()
plt.close()

f, (ax1, ax2) = plt.subplots( 1,2, sharex=True, sharey = True )
for ix in ( set(range(500)) - set(i1) ):
    DrawFace( asm.allShapes[ ix ], ax1 ).drawContrast()
for ix in ( set(range(500)) - set(i2) ):
    DrawFace( asm.allShapes[ ix ], ax2 ).drawContrast()
DrawFace( asm.meanShape, ax1).drawBold()
DrawFace( asm.meanShape, ax2).drawBold()

plt.show()
plt.close()