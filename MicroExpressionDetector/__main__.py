from active_shape_models.ActiveShapeModel import ActiveShapeModel
from active_shape_models.ShapeAligner import ShapeAligner
from helpers.FileHelper import FileHelper



output = "C:\\Users\\Valerie\\Desktop\\output\\"

iters = 10
training = 50

asm = ActiveShapeModel( [36,31] )
fh = FileHelper( training-1 , output )
asm = fh.readInPoints( asm )
asm = ShapeAligner( asm, iters, output ).alignTrainingSet( )
fh.writeOutASM( asm, iters, training )
