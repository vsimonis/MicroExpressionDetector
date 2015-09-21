from ParallelASM import Shape, Point, PASM
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import math

pal = sns.xkcd_palette( ["pink", "azure", "bright yellow" ])
mpal = sns.xkcd_palette( ['black', 'black', 'black'])
newpal = sns.xkcd_palette( ["crimson", "navy", "poop"] )
MUL = 1

## Setup
def setup( ):
    s1 = Shape( [ Point(200,340), Point( 0, 200), Point( 350,200) ] )
    s2 = Shape( [ Point(210,320), Point( 5, 205), Point( 340,190) ] )
    s3 = Shape( [ Point(205,300), Point( 10, 190), Point( 344,204) ] )
    s4 = Shape( [ Point(199,380), Point( -5, 205), Point( 333,203) ] )
    s5 = Shape( [ Point(190,290), Point( 0, 190), Point( 351,201) ] )

    asm = PASM( [0,1], 10 )

    asm.addShape( s1 )
    asm.addShape( s2 )
    asm.addShape( s3 )
    asm.addShape( s4 )
    asm.addShape( s5 )
    return asm

## Calculate PCS:
def PCA( asm ):
    asm.calcMeanShape()
    map( lambda x : x.calcDiff( asm.meanShape ), asm.allShapes )
    cov = map( lambda x : x.calcSingleCov(), asm.allShapes )
    S = sum( cov ) 

    vals, vecs = np.linalg.eig( S )
    vecs = np.array( vecs )
    return vals, vecs


def plotOnePointOneEv( evIx, ptIx, asm, vals, vecs, color, axes):
    axes.plot( [ asm.meanShape.allPts[ptIx], asm.meanShape.allPts[ptIx] + MUL * math.sqrt(vals[evIx] )* vecs[ptIx][evIx] ] , 
             [ asm.meanShape.allPts[ptIx+1], asm.meanShape.allPts[ptIx+1] + MUL * math.sqrt( vals[evIx] )* vecs[ptIx + 1][evIx] ],
             c = color, 
             lw = 1)

def plotOnePointOneEvOrigin( evIx, ptIx, vals, vecs, color, axes):
    axes.plot( [0, vecs[ptIx][evIx] * vals[evIx]] , 
            [ 0, vecs[ptIx + 1][evIx] * vals[evIx] ],
            c = color, 
            lw = 1)


def plotEVmpCentered( asm, vals, vecs, newpal, axes):
    for pt in [0,2,4]:
        plotOnePointOneEv( 0, pt, asm, vals, vecs, newpal[pt/2], axes )
        plotOnePointOneEv( 1, pt, asm, vals, vecs, newpal[pt/2], axes )
        plotOnePointOneEv( 2, pt, asm, vals, vecs, newpal[pt/2], axes )


def plotEVOriginCentered( vals, vecs, newpal, axes):
    for pt in [0,2,4]:
        for i in range( 3 ):
            plotOnePointOneEvOrigin( i, pt, vals, vecs, newpal[pt/2], axes[i] )




def project( evIx, asm, vals, vecs ):
    X = np.add( asm.meanShape.allPts, np.multiply( vecs[:,evIx], math.sqrt( vals[evIx]  )))
    x,y = reravel( X )
    #s = Shape( [ Point( X[0], X[1]), Point( X[2], X[3] ), Point( X[4], X[5] ) ] )
    sv = []
    for a, b in zip( x, y):
        sv.append( Point( a, b ) )
    s = Shape( sv )
    return s

def singlePoint( ptIx, evIx, asm, vals, vecs ):
    return Point( asm.meanShape.xs[ptIx] + MUL * math.sqrt( vals[evIx] ) * vecs[ptIx][evIx], 
                 asm.meanShape.ys[ptIx] + MUL * math.sqrt(vals[evIx]) * vecs[ptIx+1][evIx] )

def reravel( vect ):
    x, y = [], []
    vect = np.ravel( vect ) 
    for i in range( len( vect ) ):
        if i % 2 == 0:
            x.append( vect[i] )
        else: 
            y.append( vect[i] )
    return x, y

def showVaryMultiplePCS( asm, vals, vecs, numPlots, numPCs, newpal):
    f, axes = plt.subplots( 1, numPlots, sharex = True, sharey = True )
    bs = []
    for p in range( numPCs ):
        rs = np.linspace( - MUL * math.sqrt( vals[p] ), MUL * math.sqrt( vals[p] ), numPlots )
        bs.append( rs )
    P = vecs[:, 0:numPCs]
    for pl in range(numPlots) :
        b = [ bs[p][pl] for p in range(len(bs) ) ]
        X = np.add( asm.meanShape.allPts, np.dot( P, b ) )
        x, y = reravel( X )
        s = Shape( [ Point (pt[0], pt[1] ) for pt in zip(x,y) ])
        s.draw( newpal, axes[pl] ) ## diff
        axes[pl].plot( s.xs, s.ys, lw =1, c ='k')
    f.savefig( "simple-example-%d-at-a-time.png" % numPCs)

def showVary( asm, vals, vecs, numPlots, eval ):
    # Vary one eigenvalue
    f, axes = plt.subplots( 1, numPlots, sharex = True, sharey = True )

    vals = np.ravel( vals )
    rs = np.linspace( - MUL * math.sqrt( vals[eval] ), MUL * math.sqrt( vals[eval] ), numPlots )
    
    for m in range( len(rs) ):
        reps = np.add(asm.meanShape.allPts,np.multiply( np.ravel(vecs[:,eval] ), rs[m] ))
        x, y = reravel( reps )
        s = Shape( [ Point (pt[0], pt[1] ) for pt in zip(x,y) ])
        s.draw( newpal, axes[m] ) ## diff
        axes[m].plot( s.xs, s.ys, lw =1, c ='k')

    plt.savefig( 'simple-example-PC%d.png'% eval )



### Main stuff
asm = setup()

# PCA
vals, vecs = PCA( asm )

# Variance explained
for i in range(  2 * asm.n  ):
    print "%d: %f, %f" % ( i, vals[i] / sum( vals ), sum( vals[:i+1] ) / sum(vals ) )

# Setup grid
f, axes = plt.subplots( 1, 3 )
f1, axes1 = plt.subplots( 1,1)


# Draw mean shape
asm.meanShape.draw( mpal, axes1)

# Draw all shapes
for sh in asm.allShapes:
    sh.draw( pal, axes1 )


# Draw centered eigenvectors
plotEVmpCentered( asm, vals, vecs, newpal, axes1 )
plotEVOriginCentered( vals, vecs, newpal, axes )

# Example projection
s1 = project( 0, asm, vals, vecs)
s1.draw( newpal, axes1) 

f.savefig('simple-example-EVs.png')
f1.savefig( 'simple-example-EVs-origin.png')

for j in range( 3 ):
    showVaryMultiplePCS( asm, vals, vecs, 7, j+1, pal)
    showVary( asm, vals, vecs, 7, j )





