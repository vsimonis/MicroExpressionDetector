from data_parser.CASMEParser import CASMEParser
import numpy as np
import pandas as pd
import os
import numpy as np



OUT = "C:\\Users\\Valerie\\Desktop\\output"

res = [ 0.05, 0.1, 0.5 ]

orient =  [ 8 ]
scales = [ 5, 8, 11 ]

"""
for nScales in scales:
    for nOrient in orient:
        for imgRes in res:
"""


nScales = 5
nOrient = 8
imgRes = 0.06 
cp = CASMEParser( nScales, nOrient, imgRes)
featureInfo, labelInfo, retval = cp.run()

if retval:
    ## To DataFrames
    labels = pd.DataFrame.from_dict( labelInfo, orient = 'index' )
    feats = pd.DataFrame( featureInfo )

    ## Check data
    #labels[ (labels['video'] == 0) & (labels['subject'] == 0) ]

    ## To .CSV
    # Column headers (Yes) & indices (No) ???
    #pd.DataFrame.to_csv( labels, os.path.join( OUT, "CASME-Labels.csv" ), index=False)
    pd.DataFrame.to_csv( feats, os.path.join( OUT, "Gabor-S%d-O%d-H%d-W%d.csv" ) % (nScales, nOrient, cp.nh, cp.nw ), index=False )
else:
    print "Failboat"
  

    



#######################################################










 
             