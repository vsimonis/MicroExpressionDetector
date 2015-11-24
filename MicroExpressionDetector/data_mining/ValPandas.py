import pandas as pd
import numpy as np
import scipy as sp
import math

class ValPandas(object):
 
    def __init__ ( self, X = None, Y = None, df = None ):

        self.sets = { 'train': 0,
                     'test': 1,
                     'val' : 2 }
        self.X = X
        self.Y = Y
        self.df = df
        

    def addEmptyCols( self, colnames ):
        if type(colnames) is list:
            temp = pd.DataFrame( np.zeros( (len( self.df), len(colnames)) ), 
                                columns = colnames, 
                                index = range(len(self.df)) )
            self.df = self.df.join( temp ) 
    
    def addData( self, colName, vals, setStr):
        if setStr is None:
            self.df.loc[:,colName] = vals
        else:
            self.df.loc[ self.df.set == self.sets[setStr], colName ] = vals

    
    def splitData( self, ptr, pte, pval ):
        """ Adds a column to data called 'set' that creates 
        training, testing, validation according to probs given"""
        if self.X is None:
            self.df['set'] = self.sample( len( self.df), [ptr,pte,pval])
        else:
            self.X['set'] = self.sample( len( self.X), [ptr,pte,pval] )
            self.Y['set'] = self.sample( len( self.Y), [ptr,pte,pval] )
        
        
    @property
    def train( self ):
        if self.X is None:
            return self.df[ self.df.set == self.sets['train'] ]
        else:
            return self.X[ self.X.set == self.sets['train'] ] , self.Y[ self.Y.set == self.sets['train'] ]
            

    @property
    def test( self ):
        if self.X is None:
            return self.df[ self.df.set == self.sets['test'] ]
        else:
            return self.X[ self.X.set == self.sets['test'] ] , self.Y[ self.Y.set == self.sets['test'] ]
            
    
    @property
    def val( self ):
        if self.X is None:
            return self.df[ self.df.set == self.sets['val'] ]
        else:
            return self.X[ self.X.set == self.sets['val'] ] , self.Y[ self.Y.set == self.sets['val'] ]

    @staticmethod
    def sample( n, p ):
        """ Creates a list (of idxs) of length n, with class probas defined by 
        list p"""
        assert type(p) is list
        cnt = 0
        ix = list()
        for prob in p:
            if cnt == 0:
               ix = np.hstack( (ix, np.zeros( n * prob)))
            else:
               ix = np.hstack( (ix, np.ones( n * prob) * cnt) )
            cnt += 1

        np.random.shuffle( ix )
        ix = list(ix)
        

        while n - len(ix) > 0:
            ix.append(0)
        return ix

    def getSubset( self, setStr ):
        if self.X is None:
            return self.df[ self.df.set == self.sets[setStr] ]
        else:
            return self.X[ self.X.set == self.sets[setStr] ], self.Y[ self.Y.set == self.sets[setStr] ]
            

