from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys 
import numpy as np
import cv2
from pointAnnotator import Ui_MainWindow


NP = 20

class Gui( QtWidgets.QMainWindow):
    def __init__( self, parent = None):
        QtWidgets.QWidget.__init__( self, parent )
        self.initUI()


    def initUI( self ):
        # Instantiate classes
        self.ui = Ui_MainWindow()
        self.ui.setupUi( self )
        
        self.ui.img.mousePressEvent = self.pixelSelect

        # Register actions (buttons)
        self.ui.dirSearch.clicked.connect( self.browseDir )
        self.ui.nxtImg.clicked.connect( self.advanceImg )
        self.ui.skip.clicked.connect( self.skip )

        # Data members
        self.pointsToDraw = []
        self.img = None
        self.allImages = None
        self.ix = None
        self.numPoints = 0
        self.pointsLeft = NP


    def pixelSelect( self, event ):
        position = QtCore.QPoint( event.pos().x(),  event.pos().y())
        self.pointsToDraw.append( position )
        self.update()
        self.numPoints += 1
        self.pointsLeft -= 1
        self.ui.ptsLeft.setText( str( self.pointsLeft ) )
        self.ui.numPts.setText( str( self.numPoints) )
        
        #print event.pos().x(), event.pos().y()
    def skip( self ):
        self.pointsToDraw = []
        self.numPoints = 0
        self.pointsLeft = NP
        if self.ix < len(self.allImages) - 1:
            self.ix += 1
        else:
           mb = QtWidgets.QMessageBox()
           mb.setText( "All done!" )
           mb.exec_()
        self.update()

    def paintEvent( self, event ):
        #if self.img is not None:
            #self.ui.img.setPixmap(self.convertFrame( self.img ))
        if self.ix is not None:
            self.cImgLoc = self.allImages[ self.ix ]
            self.cImgPath = os.path.join( self.folder, self.cImgLoc)
            #print cImgPath
            self.ui.imgText.setText( str( self.cImgLoc ))
        
            pixmap = QtGui.QPixmap( self.cImgPath )
            #self.ui.img.show()
    #        self.ui.img.paintEvent(event)
            qp = QtGui.QPainter()
        
            qp.begin( pixmap )
            p = QtGui.QPen()
            p.setColor( QtCore.Qt.red )
            p.setWidth( 10 )
            qp.setPen( p )
        
            for pt in self.pointsToDraw:
                qp.drawPoint(pt)
            qp.end()

            self.ui.img.setPixmap( pixmap )
            self.ui.img.setAlignment( QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        


    def browseDir( self ):
        folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        #folder ="C:/Users/Valerie/Desktop/MicroExpress/CASME2/Cropped/Cropped/sub01/EP02_01f"
        print folder
        f = folder.split("/")
        
        # Get study and subject and display
        self.folder = os.path.abspath(folder)
        self.study = f.pop()
        self.subject = f.pop()

        self.ui.dirView.setText( self.folder )
        self.ui.stuText.setText( self.study )
        self.ui.subText.setText( self.subject )

        # Get files and display
        self.allImages = next(os.walk(self.folder))[2]
        self.ix = 0
        #inputImg = cv2.imread( cImgPath )
        #print inputImg
        #if self.isColor( inputImg ):
        #    self.img = cv2.cvtColor( inputImg, cv2.COLOR_RGB2GRAY )
        #else:
       # self.img = inputImg
        print "here"
        self.update()
        
    def advanceImg( self ):
        self.writeFile()
        self.skip()

    def gray2qimage(self, gray):
        """
        Convert the 2D numpy array `gray` into a 8-bit QImage with a gray
        colormap.  The first dimension represents the vertical image axis.
        """
        if len(gray.shape) != 2:
            raise ValueError("gray2QImage can only convert 2D arrays")
      
        gray = np.require(gray, np.uint8, 'C')

        h, w = gray.shape

        result = QtGui.QImage(gray.data, w, h, QtGui.QImage.Format_Indexed8)
        result.ndarray = gray
        for i in range(256):
            result.setColor(i, QtGui.QColor(i, i, i).rgb())
        return result

    def convertFrame(self,imgIn):
        """                                                    
        converts frame to format suitable for QtGui            
        """
        try:
            img = self.gray2qimage( imgIn )
            img = QtGui.QPixmap.fromImage(img)

            return img
        except:
            return None

    def isColor( self, imgIn ):
        ncolor = np.shape(imgIn)[2]
        boolt = int(ncolor) > 2
        return boolt
    def closeEvent( self, event ):
        self.writeFile()
        event.accept()
   
    def writeFile( self ):
        with open( os.path.join( self.folder, "output20", "%s.txt" % self.cImgLoc), "w") as file:
            for pt in self.pointsToDraw:
                file.write( "%d\t%d\n" % ( pt.x(), pt.y() ) )
            
        
#    def mousePressEvent( self, QMouseEvent):
#        print QMouseEvent.pos()
'''
    def mouseReleaseEvent( self, QMouseEvent):
        cursor = QtGui.QCursor()
        self.pointsToDraw.append( cursor.pos() )
        self.update()
'''
        

def main():
    app = QtWidgets.QApplication( sys.argv )
    #filter = ValEventFilter()
    #app.installEventFilter(filter)
    g = Gui()
    g.show()
    
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()