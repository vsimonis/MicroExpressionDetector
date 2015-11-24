from feature_extraction.GaborExtractor import GaborExtractor as gab
from image_processing.PreProcessing import PreProcessing as pp
import os
from matplotlib import pyplot as plt
import numpy as np

                                    

#http://stackoverflow.com/questions/28995146/matlab-ind2sub-equivalent-in-python
def getOrientationScaleIx( ix, no, ns ):
    return ind2sub( ix, no, ns )

## Given number of rectangles wanted, returns 
def ind2sub( ix, nrows, ncols ):
    row = ix / ncols
    col = ix % ncols # or numpy.mod(ind.astype('int'), array_shape[1])
    return (row, col)



def getRectangleParams( img, numRects): ## only works with even
    nrows = 0
    ncols = 0
    cs = np.shape( img )
    cs = list( cs )

    while numRects != 1:
        maxIx = np.argmax( cs )
        replace( cs, 2, maxIx )
        if maxIx == 0:
            nrows += 1
        else:
            ncols += 1
        numRects /= 2
    print cs, 2**nrows, 2**ncols
    return cs, (2**nrows, 2**ncols)


def replace( vect, mult, maxIx):
    v = vect.pop( maxIx)
    vect.insert( maxIx, v / mult )

  

def sliceImg( img, rectSize, rectIx ):
    slices = []
    for nr in range( rectIx[0] ):
        for nc in range( rectIx[1] ):
            slices.append( list( img[ nr * rectSize[0] + nr :  nr * rectSize[0] + nr + rectSize[0],
                                nc * rectSize[1] + nc :  nc * rectSize[1] + nc + rectSize[1]] ) )                              
    return slices        



def findMaxMag( fImg ):
    return np.argmax( fImg )


def getResponseVals( fImg, maxLoc):
    return fImg[ maxLoc[0] ][ maxLoc[1] ]

    




data = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\Cropped\Cropped"
sub = "sub01"
ep = "EP02_01f"
img = "reg_img46.jpg"
I = pp.readInImg( os.path.join( data, sub, ep, img) ) 

ns = 5
no = 8 
ksize = 21

g = gab( ns, no, ksize )
f = g.generateGaborKernels()
imgs = g.processGaborRaw( I, f )

fVect = []                                   

for fIx, fImg in enumerate( imgs ):
    o,s = getOrientationScaleIx( fIx, no, ns )

    maxLocs = []
    rsize,  rIx = getRectangleParams( fImg, 128)
    slices = sliceImg( fImg, rsize, rIx )

    for slice in slices:
        sliceR, sliceC = np.shape( slice )
        if s == 0:
            maxLoc = findMaxMag( slice )
            maxLoc = ind2sub( maxLoc, sliceR, sliceC )
            

        fVect.append( getResponseVals( fImg ,maxLoc) )        



