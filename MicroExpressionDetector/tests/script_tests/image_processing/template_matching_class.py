from image_processing.TemplateMatcher import TemplateMatcher
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

i = 20
tr = 500
out =    "C:\\Users\\Valerie\\Desktop\\output\\ASMTraining-MessingAround\\20-500-1" 

fh = FileHelper( i, tr, out, False, False )

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
appASM = ApplyASM( asm, i, tr, out, I, "SSD", 5,5 )
m, tdict = appASM.initialPosition( )

TM = TemplateMatcher( 'SSD', 5 )
TM.performMatching(I, m)