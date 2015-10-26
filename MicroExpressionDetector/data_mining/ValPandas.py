import pandas as pd
import numpy as np
import scipy as sp
import math

class ValPandas(object):
 
    def __init__ ( self, df ):
        self.data = df
        self.sets = { 'train': 0,
                     'test': 1,
                     'val' : 2 }
        #self.feats = features
        #self.label = label

    def addEmptyCols( self, colnames ):
        if type(colnames) is list:
            temp = pd.DataFrame( np.zeros( (len( self.data), len(colnames)) ), 
                                columns = colnames, 
                                index = range(len(self.data)) )
            self.data = self.data.join( temp ) 
    
    def addData( self, colName, vals, setStr):
        if setStr is None:
            self.data.loc[:,colName] = vals
        else:
            self.data.loc[ self.data.set == self.sets[setStr], colName ] = vals

    def sliceRows( self, condition ):
        return self.data
    
    def splitData( self, ptr, pte, pval ):
        """ Adds a column to data called 'set' that creates 
        training, testing, validation according to probs given"""
        self.data['set'] = self.sample( len( self.data), [ptr,pte,pval])
        self.splitSets = { }
        
    @property
    def train( self ):
        return self.data[ self.data.set == self.sets['train'] ]

    @property
    def test( self ):
        return self.data[ self.data.set == self.sets['test'] ]
    
    @property
    def val( self ):
        return self.data[ self.data.set == self.sets['val'] ]

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
        
        print len(ix)
        print n

        while n - len(ix) > 0:
            ix.append(0)
        return ix

    def getSubset( self, setStr ):
        return self.data[ self.data.set == self.sets[setStr] ]
