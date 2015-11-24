### AdaBoost
#from sklearn.ensemble import AdaBoostClassifier
#from sklearn.naive_bayes import MultinomialNB
#from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import math
import os
from data_mining.CASMEData import  ValPandas, CASMEData
import re
from matplotlib import pyplot as plt

minSplit = [ 5 * i for i in range( 1, 30 ) ] 


OUT = "C:\Users\Valerie\Desktop\output"

results = {}
i = 0
for file in os.listdir( OUT ):
    if file != "CASME-Labels.csv":

        ## Parse data
        a = file.split("-") 
        [_, m] = a[:2]
        [s,o,h,w,r] = map( lambda x: int( re.findall( r'\d+', x )[0] ), a[2:] )
        print m, s, o, h, w, r

        l = "CASME-labels.csv"
        try:
            X = pd.DataFrame.from_csv( os.path.join( OUT, file ) )
        except MemoryError:
            print "mem"
            pass
        Y = pd.DataFrame.from_csv( os.path.join( OUT, l ))
        df = CASMEData( X = X, Y = Y )
        try:
            df.splitData( 0.6, 0.3, 0.1 )
        except MemoryError:
            print "mem"
            pass


        fig = plt.figure()
        _ = plt.plot( [0.5,1], [0.5,1])
        ax = fig.add_subplot(111)
        # Tune params
        maxTest = 0
        for ms in minSplit :                                  #actually minleaf, change name

            clf = DecisionTreeClassifier( min_samples_split = 25, min_samples_leaf = ms )
            try:
                _ = clf.fit( df.Xtrain, df.Ytrain ) 
                YpredTrain = clf.predict( df.Xtrain )
                YpredTest = clf.predict( df.Xtest )
                trainAcc = accuracy_score( df.Ytrain, YpredTrain )
                testAcc = accuracy_score( df.Ytest, YpredTest)
                _ = plt.scatter( trainAcc, testAcc )
                _ = plt.xlabel( "Training Accuracy" )
                _ = plt.ylabel( "Testing Accuracy" )

                if trainAcc - testAcc < 0.1 and testAcc > maxTest   :
                    maxTest = testAcc
                    _ = ax.annotate( '(%d, %d)' % (ms, 25), xy=( trainAcc, testAcc), textcoords='offset points', size = 8)

                    results.update( { i : { "Method" : m,
                                            "Scales": s,
                                            "Orientations" : o,
                                            "Height" : h,
                                            "Width" : w,
                                            "Rectangles" : r,
                                            "Training" : trainAcc,
                                            "Testing" : testAcc,
                                            "MinLeaf" : ms} } )

                
                    i += 1
            except MemoryError:
                print "mem"
                pass
                        
        fig.savefig( "out-%s-S%d-O%d-H%d-W%d-R%d.png" % ( m, s, o, h, w, r) )
        plt.close( fig )

df = pd.DataFrame.from_dict( results, orient = 'index')
df.to_csv( "results-dm.csv" )

df = df[["Method", "Height", "Width", "Rectangles", "Orientations", "Scales", "MinLeaf", "Training", "Testing" ]] 
df = df.sort( columns = ["Height", "Scales", "Rectangles"] )

def writeHeader( out ):
    out.write("\\documentclass[writeup.tex]{subfiles}\n")
    out.write("\\begin{document}\n")
    return out
    
def writeFooter( out):
    out.write("\\end{document}\n")
    return out

def startTable( out ):
    out.write("\\begin{table}[H]\n")
    out.write("\\centering\n")
    out.write("\\begin{tabular}")
    return out
def endTable( out ):
    out.write("\\end{tabular}\n \\\\")
    out.write("\\caption{Accuracy results}\n" )
    out.write("\\end{table}\n")
    out.write("\\hspace{5mm}\n")
    return out

def crossTable( out, ct ):
    cols = ct.columns
    rows = ct.index
    

        ## Column Headers
    c = len(cols) + 1

    out.write("{|*{%d}{r|}}\n" % c)
    out.write("\\hline\n")
    for icx in range(len(cols)):
        colname = cols[icx]
        if icx == len(cols) - 1:
            out.write( "\\textbf{%s}" % (colname))
        else:
            out.write( "\\textbf{%s} &" % (colname))
    out.write( "\\\\\n")
    out.write("\\hline\n")
    
        ## Rows
    for irx, row in ct.iterrows():
        #out.write( '\\textbf{%s} &' % irx)
        for ix, val in enumerate( row.values ):
            if ix == len(row.values) - 1:
                if isinstance( val, str ):
                    out.write( "%s" % val )
                elif isinstance( val, long):
                    out.write( "%d" % val )
                else:
                    out.write( "%.2f" % (val * 100) )
                
            else:
                if isinstance( val, str):
                    out.write( "%s &" % val )
                elif isinstance( val, long):
                    out.write( "%d &" % val )
                else:
                    out.write( "%.2f &" % (val * 100) )

        out.write( "\\\\\n" )
        out.write("\\hline\n")

    return out

def tableout( df ):
    with open("results.tex", 'w') as out:
        writeHeader( out )
        startTable( out )
        crossTable( out, df )
        
        endTable( out )
        writeFooter( out )

tableout( df )