from shapes.Shape import Shape

class ActiveShape( Shape ):
    def __init__( self, *args, **kwargs ):
        super( ActiveShape, self).__init__( *args, **kwargs)

    def calcR( self ):
        """
        Calculates distance matrix between all points for a given shape
        sets global variable 
        """
        sp = self.shapePoints
        ## For every point in shapePoints, calculate distance to other points
        self.R = [ [sp[k].dist( sp[l] ) for k in range( self.n )] for l in range( self.n ) ]
        return self.R

    
    def calcDiff( self, shape ):
        self.unravel()
        shape.unravel()
        self.diffAllPts = np.subtract( self.allPts, shape.allPts)
        return self.diffAllPts
     
    def calcSingleCov( self ):
        self.singleCov = np.dot( np.transpose(np.mat(self.diffAllPts)),  np.mat(self.diffAllPts) )
        return self.singleCov


