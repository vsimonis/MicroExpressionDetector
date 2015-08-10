from ParallelASM import PASM, Shape, Point
import numpy as np
from matplotlib import pyplot as plt
import math
import seaborn as sns
import random
from FaceDraw import FaceDraw

def PCA( asm ):
    asm.calcMeanShape()
    map( lambda x : x.calcDiff( asm.meanShape ), asm.allShapes )
    cov = map( lambda x : x.calcSingleCov(), asm.allShapes )
    S = sum( cov ) 

    vals, vecs = np.linalg.eig( S )
    vecs = np.array( vecs )
    return asm, vals, vecs
    

def main():
    asm = readIn() 
    asm, vals, vecs = PCA( asm )
    # Variance explained
    with open('faces-results.txt', 'w') as outfile:
        for i in range( 20 ):
            outfile.write("%d: %f, %f \n" % ( i, vals[i] / sum( vals ), sum( vals[:i+1] ) / sum(vals ) ) )

    ## Reproject multiple PCS and vary evals 
    for i in range( 10 ):
        showVaryMultiplePCS( asm, vals, vecs, 5, i+1 )
        showVary( asm, vals, vecs, 5, i, 0.25)
        exampleEvalEvecs(asm, vecs, vals, i ) 
    ### Draw all faces
    for sh in asm.allShapes :
        FaceDraw( sh, plt ).drawContrast()
    plt.savefig( 'faces-all.png')
    plt.close()
    

    
    

def reravel( vect ):
    x, y = [], []
    vect = np.ravel( vect ) 
    for i in range( len( vect ) ):
        if i % 2 == 0:
            x.append( vect[i] )
        else: 
            y.append( vect[i] )
    return x, y
           

def showVaryMultiplePCS( asm, vals, vecs, numPlots, numPCs ):
    f, axes = plt.subplots( 1, numPlots )
    bs = []
    for p in range( numPCs ):
        rs = np.linspace( - 0.25 * math.sqrt( vals[p] ), 0.25 * math.sqrt( vals[p] ), numPlots )
        bs.append( rs )
    P = vecs[:, 0:numPCs]
    for pl in range(numPlots) :
        b = [ bs[p][pl] for p in range(len(bs) ) ]
        X = np.add( asm.meanShape.allPts, np.dot( P, b ) )
        x, y = reravel( X )
        s = Shape( [ Point (pt[0], pt[1] ) for pt in zip(x,y) ])
        FaceDraw( s, axes[pl] ).drawBold()
        axes[pl].set_xlim( (-2,2) )
        axes[pl].set_ylim( (-3,3) )

        
    f.savefig('faces-%d-PCs-at-once.png' % numPCs )
    plt.close()
        
        
def projectOnePC( evIx, b, asm, vals, vecs ):
    X = np.add( asm.meanShape.allPts, np.multiply( vecs[:,evIx],  b ) )
    x,y = reravel( X )
    sv = []
    for a, b in zip( x, y):
        sv.append( Point( a, b ) )
    s = Shape( sv )
    return s

                 

def showVary( asm, vals, vecs, numPlots, eval, lim ):
    # Vary one eigenvalue
    f, axes = plt.subplots( 1, numPlots, sharex = True, sharey = True )

    vals = np.ravel( vals )
    rs = np.linspace( -lim * math.sqrt( vals[eval] ), lim * math.sqrt( vals[eval] ), numPlots )
    
    for m in range( len(rs) ):
        s = projectOnePC( eval, rs[m], asm, vals, vecs )
        FaceDraw( s, axes[m] ).drawBold()
        axes[m].set_xlim( (-2,2) )
        axes[m].set_ylim( (-3,3) )
        plotEigenvectors( asm, vecs, vals, eval, axes[m], lim )
        FaceDraw( asm.meanShape, axes[m] ).drawContrast()
    f.savefig('faces-PC-%d.png' % eval )
    plt.close()

def plotEigenvectors( asm, vecs,vals, evIx, axes, lim ):
    for ptIx in np.multiply( 2, range(asm.n) ):
        axes.plot( [ asm.meanShape.allPts[ptIx], asm.meanShape.allPts[ptIx] + lim * math.sqrt(vals[evIx] )* vecs[ptIx][evIx] ] , 
                 [ asm.meanShape.allPts[ptIx+1], asm.meanShape.allPts[ptIx+1] + lim * math.sqrt( vals[evIx] )* vecs[ptIx + 1][evIx] ],
                 c = '#A0A0A0', 
                 lw = 0.5)
        axes.plot( [ asm.meanShape.allPts[ptIx], asm.meanShape.allPts[ptIx] - lim * math.sqrt(vals[evIx] )* vecs[ptIx][evIx] ] , 
                 [ asm.meanShape.allPts[ptIx+1], asm.meanShape.allPts[ptIx+1] - lim * math.sqrt( vals[evIx] )* vecs[ptIx + 1][evIx] ],
                 c = '#A0A0A0', 
                 lw = 0.5)

   

def reProjectCumulative( asm, numVals, vals, vecs ):
    P = vecs[:, 0:numVals]
    b = [ np.transpose(np.mat( vals[ 0: numVals ] )) ] 

    X = np.add( asm.meanShape.allPts, np.dot( P, b ) )
    x,y = reravel( X )
    return Shape( [ Point (pt[0], pt[1] ) for pt in zip(x,y) ])





def exampleEvalEvecs( asm, vecs, vals, evIx ):
    vecs = np.array( vecs )
    newPts = np.add( asm.meanShape.allPts, np.multiply(math.sqrt( vals[evIx] ), vecs[:,evIx] ) )
    print np.shape( newPts)
    #x, y = reravel( np.multiply( vals[0], vecs[:,0] ) )
    newx, newy = reravel( newPts )
    print np.shape( newx) 
    ## Mean Shape
    FaceDraw( asm.meanShape, plt ).drawBold()
    ## Eigenvectors
    plt.plot( [asm.meanShape.xs, np.add( asm.meanShape.xs, newx ) ], 
            [ asm.meanShape.ys, np.add( asm.meanShape.ys, newy ) ], c ='#A0A0A0', lw = 1 )
    plt.xlim( (-6,6) )
    plt.ylim( (-6,6))
    ## New Shape
    #FaceDraw( ( newx, newy), plt ).draw()
    plt.savefig( 'faces-eigenvectors-%d.png' % evIx )
    plt.close()


def exampleVariance( vecs, vals ):
    for e in range(10):
        showVary( asm, vals, vecs, 5, e, 0.5 )

def readIn( ):
    allLines = None
    with open( "outfile-ASM-100iters-500tr.txt", "r") as infile:
        allLines = infile.readlines()
        cleanLines = map( lambda x : x.strip().split(), allLines )
    
    asm = PASM( [36,31],10 )
    s = []

    for tuple in cleanLines:
        if tuple[0] == '!!!':
            if s != []:
                asm.meanShape = Shape( s )
                s = []
            else: 
                pass
        elif tuple[0] == '@@@':
            if s != [] :
                asm.addShape( Shape(s) )
                s = []
            else: 
                pass
        else:
            s.append( Point( float(tuple[0]), float(tuple[1]) ) )
    return asm

if __name__ == "__main__":
    main()