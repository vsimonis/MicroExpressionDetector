import os
from image_processing.PreProcessing import PreProcessing as pp
from feature_extraction.GaborWindowExtractor import GaborWindowExtractor as w
data = "C:\Users\Valerie\Desktop\MicroExpress\CASME2\Cropped\Cropped"
sub = "sub01"
ep = "EP02_01f"
img = "reg_img46.jpg"
I = pp.readInImg( os.path.join( data, sub, ep, img) )

gw = w( 5, 8, 15, 8 )
gw.process( I ) 