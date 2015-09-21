import cv2
from helpers.FileHelper import FileHelper
from helpers.DrawFace import DrawFace
from shapes.ActiveShape import ActiveShape
from active_shape_models.ActiveShapeModel import ActiveShapeModel
from active_shape_models.ApplyASM import ApplyASM
from shapes.Vector import Vector
from matplotlib import pyplot as plt
from matplotlib import gridspec
import numpy as np
import math
import sys
import copy


def hinge( v, n ):
    lower = int(round(v) - math.floor( n/2 ))
    upper = int(round(v) + math.floor( n/ 2))
    return lower, upper

def slice( mat, n, pt ):
    lc, uc = hinge( pt.x, n )
    lr, ur = hinge( pt.y, n )
    nr, nc = np.shape( mat )
    nr = nr - 1
    nc = nc - 1
    
    alc, auc = lc, uc # copy.deepcopy( lc ), copy.deepcopy( uc )
    alr, aur = lr, ur #copy.deepcopy( lr ), copy.deepcopy( lc )
    rpb, rpa, cpl, cpr = [0,0,0,0]

    if lc < 0:
        alc = 0
        cpl = -lc 

    if uc > nc:
        auc = nc #copy.deepcopy( nc )
        cpr = uc - auc 

    if lr < 0:
        alr = 0
        rpb = -lr

    if ur > nr:
        aur = nr #copy.deepcopy( nr ) 
        rpa = ur - aur 

    return np.pad( mat[ alr : aur + 1 , alc : auc + 1 ], (( rpb, rpa ),( cpl, cpr )), mode ='constant' )



## http://stackoverflow.com/questions/28995146/matlab-ind2sub-equivalent-in-python
def ind2sub(array_shape, ind):
    rows = (int(ind) / array_shape[1])
    cols = (int(ind) % array_shape[1]) # or numpy.mod(ind.astype('int'), array_shape[1])
    return (rows, cols)

def normCorr( template, image ):
    t = np.ravel( template - np.mean( template ))
    nt = math.sqrt( sum( t ** 2 ) )
    i = np.ravel( image - np.mean( image )) 
    ni = math.sqrt( sum( i ** 2 ) )
    if ni == 0 or nt == 0:
        return 0
    th = np.divide( t, nt )
    ih = np.divide( i, ni )
    return sum ( th * ih )

def SSD( template, image ):
    t = np.ravel(template - np.mean( template ))
    i = np.ravel(image - np.mean( image ))
    return sum( ( t - i ) ** 2 )


def matIxs( n ):
    rows, cols = np.indices( (n,n) )
    row = rows.flatten()
    col = cols.flatten()
    
    return map( lambda x: Vector( x[0], x[1] ), zip( row, col )  )

def coordOffset( pt, n ):
    y = pt.y   #row
    x = pt.x   #col
    return x - ( n - 1)/2, y - (n-1)/1 

#def run( ):
i = 20
tr = 500
out =    "C:\\Users\\Valerie\\Desktop\\output\\20-500-1" 

fh = FileHelper( i, tr, out )

ebenFace  =  fh.readInImage()
ebenPoints = fh.readInOneDude( '000_1_1.pts')  
ebenShape = ActiveShape( ebenPoints )
 
#### MATCHING PROCESS

# Read in image
I = cv2.imread( "C:\Users\Valerie\Desktop\MicroExpress\CASME2\CASME2_RAW\CASME2-RAW\sub01\EP02_01f\img1.jpg")
I = cv2.cvtColor( I, cv2.COLOR_BGR2GRAY)

# Align shape
asm = ActiveShapeModel( [36,31] )
asm = fh.readInASM( asm )
asm.PCA()  
appASM = ApplyASM( asm, i, tr, out, I )
m, tdict = appASM.initialPosition( )

def genTemplateArr( ):
    templates = []
    for pt in ebenShape.shapePoints:
        templates.append( slice( ebenFace, 5, pt ) )
    return templates

def genTemplateDict( ):
    templates = {}
    ix = 0
    for pt in ebenShape.shapePoints:
        templates.update( { ix : slice( ebenFace, 5, pt ) } ) 
        ix += 1
    return templates

def genRegionArr( ):
    regions = []
    for pt in m.shapePoints :
        regions.append( slice( I, 25, pt ) )   
    return regions

def genRegionDict( ):
    regions = {}
    ix = 0
    for pt in m.shapePoints :
        regions.update( { ix : slice( I, 25, pt ) } )   
        ix += 1
    return regions    


ixs = matIxs( 25 )
response = {}
meth = 'corr'
### For every region
for rIx, r in genRegionDict().iteritems():

    print rIx

    ## 5 x 5 windows for region r
    ws = map( lambda x : slice( r, 5, x ), ixs )

    
    ## For every template
    minResp =  sys.maxint
    maxResp = 0

    for tIx, t in genTemplateDict().iteritems():

        if meth == 'SSD' :
            resp = map( lambda  w: SSD( t, w), ws )
            minIX = np.argmin( resp )
            mag = resp[ minIX ]

            if mag < minResp :
                minResp = mag
                matchPt = ixs[ minIX ]
                dx, dy = coordOffset( matchPt, 25 )
                response.update({ rIx : { 'tIx' : tIx,  'mag' : mag, 'd' : ( dx, dy ), 'pt' : ( matchPt.x, matchPt.y ) } })
        else:
            resp = map( lambda  w: normCorr( t, w), ws )
            maxIx = np.argmax( resp )
            mag = resp[ maxIx ] 
            if mag > maxResp :
                maxResp = mag
                matchPt = ixs[ maxIx ]
                dx, dy = coordOffset( matchPt, 25 )
                response.update({ rIx : { 'tIx' : tIx,  'mag' : mag, 'd' : ( dx, dy ), 'pt' : ( matchPt.x, matchPt.y ) } })

            
     
def minResponse( ws, t ):
    resp = map( lambda w : SSD( t, w ), ws )
    minIX = np.argmin( resp )
    mag = resp[ minIX ]
    
    
    
        


def singleRegionTemplate( ixs ):
    r = regions[0]

    ## 5 x 5 windows for region r
    ws = map( lambda x : slice( r, 5, x ), ixs )

    ## Get template response
    t = templates[0]
    resp = map( lambda  w: SSD( t, w), ws )
    
    ## Find min
    minIX = np.argmin( resp )
    matchPt = ixs[ minIX ]
    dx, dy = coordOffset( matchPt, 25 )

 


def plotTemplates( ):
    for k, t in genTemplateDict().iteritems():
        plt.imshow( t )
        plt.gca().axes.xaxis.set_ticks([])
        plt.gca().axes.yaxis.set_ticks([])
        plt.savefig( "C:\\Users\\Valerie\\Desktop\\output\\matching\\templates\\%d.png" % k, bbox_inches = 0)


def plotRegionResponse( resp ):
    ts = genTemplateArr()
    rs = genRegionArr()
    for rix, r in resp.iteritems():
        fig = plt.figure()
        gs = gridspec.GridSpec( 2,2 )
        ax1 = fig.add_subplot( gs[ : , 0 ] )
        ax2 = fig.add_subplot( gs[ 0, 1 ])
        ax3 = fig.add_subplot( gs[ 1, 1 ]) # sharex = ax1, sharey = ax1)

    
        ax1.imshow( rs[ rix ] )
        ax1.scatter( r[ 'pt' ][0], r[ 'pt'][1] )
        ax1.set_xlim( -1,25 )
        ax1.set_ylim( 25, -1 )
        ax2.imshow( ts[ rix ] )
        ax3.imshow( ts[ r[ 'tIx' ] ] )
        plt.savefig( "C:\\Users\\Valerie\\Desktop\\output\\matching\\matches\\%d.png" % rix )
        plt.close()
    
        


def plotResponse( resp ):
    f, (ax1, ax2 ) = plt.subplots( 1,2, sharex = True, sharey= True)
    # draw region
    ax1.imshow( r ) 
    ax1.scatter( matchPt.x, matchPt.y )

    ax2.imshow( t )
    plt.xlim( -1, 25 )
    plt.ylim( 25, -1 )
    plt.show()








### PUTTING IT ALL TOGETHER:








                                        








def addFace( ebenFace ):
    plt.imshow( ebenFace )
    plt.gca().axes.xaxis.set_ticks([])
    plt.gca().axes.yaxis.set_ticks([])
    return plt

    
def drawGroundTruth( ebenFace ):
    plt.imshow( ebenFace )
    DrawFace( ebenShape, plt).drawBold()
    DrawFace( ebenShape, plt).drawPoints()
    plt.xlim( 200, 525)
    plt.ylim( 525, 225 )
    plt.show()

def drawIndices( ebenFace ):
    addFace( ebenFace)
    DrawFace( ebenShape, plt).drawBold()
    DrawFace( ebenShape, plt).labelIndices()
    plt.xlim( 200, 525)
    plt.ylim( 525, 225 )
    plt.show()
    
    addFace( ebenFace)
    plt.imshow( ebenFace )
    DrawFace( ebenShape, plt).drawBold()
    DrawFace( ebenShape, plt).labelIndices()
    plt.xlim( 300, 425)
    plt.ylim( 430, 380 )
    #plt.show()


w = [[120,130,140],[115,120,130],[100,115,120]]     #template
f = [[110,120,135],[120,115,95],[100,105,90]]       #image frame
f2 = [[90,120,230],[120,75,95],[100,11,90]]       #image frame

black = [[0,0,0],[0,0,0],[0,0,0]]
white = [[255,255,255],[255,255,255],[255,255,255]]
big = np.reshape( range( 25 ), (5,5 ) )
## max SSD = 255 ^ 2 * number of tiles ( w/o sub mean)






    


addFace(ebenFace)
DrawFace( m, plt ).drawBold()
DrawFace( m, plt ).labelIndices()

                              

### Slicing testing

def sliceTest( big ) :
    nr, nc = np.shape( big )
    for i in range( nr ):
        for j in range( nc ):
            print i, j 
            print slice( big, 3, Vector( j, i ) )
            print slice( big, 5, Vector(j, i ) )
    
                                  