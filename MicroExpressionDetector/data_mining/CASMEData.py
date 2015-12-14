from data_mining.ValPandas import ValPandas
class CASMEData( ValPandas ):
    def __init__ ( self, X = None, Y = None, df = None ):
        super( CASMEData, self).__init__( X = X, Y = Y, df = df )
        self.label = ['emotion']
        self.filters = ['subject', 'video', 'frame','isOnset', 'isApex', 'isOffset']  
        if X is None:
            dims = len( df.columns ) - len( self.label ) - len( self.filters)
        else:
            dims = len( X.columns )
        self.feats = ['%s' % i for i in range( dims )]
      
    @property
    def x( self ):
        return self.X[ self.feats]

    @property
    def y(self):
        return self.Y[ self.label ]

    @property
    def Xtrain( self ):
        if self.X is None:
            return self.train[self.feats]
        else :
            a, b = self.train
            return a
            

    @property
    def Xtest( self ):
        if self.X is None:
            return self.test[self.feats]
        else :
            a, b = self.test
            return a


    @property
    def Xval( self ):
        if self.X is None:
            return self.val[self.feats]
        else :
            a, b = self.val
            return a


    @property
    def Ytrain( self ):
        if self.X is None:
            return self.train['emotion']
        else :
            a, b = self.train
            return b[ 'emotion' ]
        

    @property
    def Ytest( self ):
        if self.X is None:
            return self.test['emotion']
        else :
            a, b = self.test
            return b[ 'emotion' ]



    @property
    def Yval( self ):
        if self.X is None:
            return self.val['emotion']
        else :
            a, b = self.val
            return b[ 'emotion' ]


