import sys
sys.path.append( ".." )


from shapes.ActiveShape import ActiveShape
from shapes.Vector import Vector
import logging
import os
import cv2
import copy

class FileHelper( object ):
    """description of class"""

    def __init__( self, nIters, nTrain, out, filterPts, filterImgs ):
        direc = "C:\\Users\\Valerie\\Desktop\\MicroExpress\\facePoints"
        subdir = "session_1"
        self.pointFolder = os.path.join( direc, subdir )
        self.pointFiles = next(os.walk(self.pointFolder))[2]
        self.nTrain = nTrain
        self.nIters = nIters
        self.output = out
        self.exclPts = [ 31 ,36, 66, 67]
        self.doExclPts = filterPts
        self.exclImgs  = [ 15,  36,  58, 155, 165, 166, 167, 183, 245, 292, 299, 312, 340, 341, 405, 461]
        self.doExclImgs = filterImgs
        # setup logging

    @staticmethod
    def readInEbenImg( ):
        img = cv2.imread( 'C:\\Users\\Valerie\\Downloads\\000_1_1.ppm')
        img_gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY ) 
        return img_gray

    @staticmethod
    def readInImage():
        img = cv2.imread( 'C:\\Users\\Valerie\\Desktop\\MicroExpress\\CASME2\\Cropped\\Cropped\\sub02\\EP01_11f\\reg_img46.jpg' )
        img = cv2.imread( 'C:\\Users\\Valerie\Desktop\\MicroExpress\\CASME2\\CASME2_RAW\\CASME2-RAW\\sub01\\EP02_01f\\img1.jpg')
    
        img = cv2.imread( 'C:\\Users\\Valerie\\Downloads\\000_1_1.ppm')
        img_gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY ) 
        #faces = face_cascade.detectMultiScale( gray, 1.3, 5)
        #for (x,y,w,h) in faces:
        #    cv2.rectangle( img, (x,y), (x+w,y+h), (255,0,0),2)
        #    roi_gray = gray[y:y+h, x:x+w]
        #    roi_color = img[y:y+h, x:x+w]

        return img_gray

    def writeOutASM( self, asm ):
        with open( os.path.join(self.output, 'outfile-ASM-%diters-%dtr.txt' % (self.nIters, self.nTrain) ), "w") as output:
            output.write( str(asm.meanShape) )
            output.write( "!!!\n" )
            for shape in asm.allShapes:
                output.write(  str(shape) )
                output.write( "@@@\n" )
            output.write( "!!!\n" )

    def readInASM( self, asm ):
        allLines = None
        #f = "C:\\Users\\Valerie\\Documents\\Visual Studio 2013\\Projects\\ActiveShapeModels\\ActiveShapeModels\\outputs\\outfile-ASM-100iters-500tr.txt"
        with open( os.path.join( self.output, 'outfile-ASM-%diters-%dtr.txt' % (self.nIters, self.nTrain)) , "r") as infile:
            #with open( f, "r") as infile:
            allLines = infile.readlines()
            cleanLines = map( lambda x : x.strip().split(), allLines )
    
        s = []

        for tuple in cleanLines:
            if tuple[0] == '!!!':
                if s != []:
                    asm.meanShape = ActiveShape( s )
                    s = []
                else: 
                    pass
            elif tuple[0] == '@@@':
                if s != [] :
                    asm.addShape( ActiveShape(s) )
                    s = []
                else: 
                    pass
            else:
                s.append( Vector( float(tuple[0]), float(tuple[1]) ) )
        return asm

    def readInOneDude( self, f):
        ptList = [ ]
        ex = copy.deepcopy( self.exclPts )
        with open( os.path.join(self.pointFolder,f), "r" ) as infile:
            allLines = infile.readlines()
            pointLine = False
            cleanLines = [ x.strip() for x in allLines]
            for line in cleanLines:
                if line is '{':
                    pointLine = True
                elif line is '}':
                    pointLine = False
                elif pointLine:
                    ptList.append( map( float, line.split(' ') ) )
                else:
                    pass
        if self.doExclPts:
            while ex != []:
                ptList.pop( ex.pop() )
        return ptList



    def readInPoints( self, asm ):
        m = 0
                        
        for f in self.pointFiles :
            ptList = self.readInOneDude( f )
            if self.doExclImgs:
                if m in ( set( range(self.nTrain) ) - set( self.exclImgs ) ): 
                    asm.addShape( ActiveShape( ptList ) )
            else:
                asm.addShape( ActiveShape( ptList ) )
                
            m += 1

            if m > self.nTrain - 1:
                return asm



