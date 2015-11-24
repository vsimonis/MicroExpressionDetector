import pandas as pd
import numpy as np


SET = { 0: 'Training',
       1: 'Testing',
       2: 'Validation'}

def valTab( lab, k, w, data, setInt):
    # Margin
    c1 = data.loc[data.set == setInt,'M-%d-%d' % (lab,k)]
  
    # Bin margin
    binner = np.arange( -1.1,1.1,0.1)
    c1b = np.digitize( c1, bins = binner )
    
    # Zero Crossings
    c2 = data.loc[data.set == setInt,'ZC-%d-%d-%d' % (lab,k,w)]
    
    # Cross tabs

    ct = pd.crosstab( c1b, c2, dropna = False)

    # Index for row bins (margin)
    rix = []
    for i in range(len( binner )):
        if i < len(binner)-1:
            rix.append('(%.1f,%.1f]'% (binner[i], binner[i+1]))


    ct.index = pd.Index(rix[:len(ct)], name = 'M')

    return ct

def writeHeader( out ):
    out.write("\\documentclass[final.tex]{subfiles}\n")
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

def endTable( out, lab, k, w, set):
    out.write("\\end{tabular}\n \\\\")
    out.write("\\caption{%s Margin/Zero-Crossing space for %d labels, %d iterations, %d window}\n" % (SET[set], lab, k, w ))
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
    out.write(" & \\multicolumn{%d}{c|}{\\textbf{Zero-crossings}}\\\\\n" % (c-1))
    out.write("\\hline\n")
    out.write("\\textbf{Margin} &")
    for icx in range(len(cols)):
        colname = cols[icx]
        if icx == len(cols) - 1:
            out.write( "\\textbf{%d}" % int(colname))
        else:
            out.write( "\\textbf{%d} &" % int(colname))
    out.write( "\\\\\n")
    out.write("\\hline\n")
    
    ## Rows
    for irx, row in ct.iterrows():
        out.write( '\\textbf{%s} &' % irx)
        for i in range(len(row.values)):
            if i == len(row.values) - 1:
                out.write( "%d" % row.values[i] )
            else:
                out.write( "%d &" % row.values[i])
        out.write( "\\\\\n" )
        out.write("\\hline\n")

    return out

def main():
     data = pd.read_csv('./csvs/final-100.csv')
     out = StringIO.StringIO()
     out = writeHeader( out )
     
