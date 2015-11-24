from data_parser.CASMEParser import CASMEParser
import numpy as np
import pandas as pd
import os
import numpy as np



OUT = "C:\\Users\\Valerie\\Desktop\\output"

res = [ 0.03, 0.04, 0.05, 0.06, 0.07 ]

orient =  [ 8 ]
scales = [ 5, 9 ]
rects = [ 8, 16, 32, 64, 128]
for method in ["ImgRes", "Rects"]:

    for nScales in scales:
        for nOrient in orient:
            if method == "ImgRes":
                for imgRes in res:
                    cp = CASMEParser( method, nScales, nOrient, imgRes, 0)
                    featureInfo, labelInfo, retval = cp.run()

                    if retval:
                        ## To DataFrames
                        labels = pd.DataFrame.from_dict( labelInfo, orient = 'index' )
                        feats = pd.DataFrame( featureInfo )

                        print feats
                        feats = feats.reindex()
                        print feats

                        ## Check data
                        #labels[ (labels['video'] == 0) & (labels['subject'] == 0) ]

                        ## To .CSV
                        # Column headers (Yes) & indices (No) ???
                       # pd.DataFrame.to_csv( labels, os.path.join( OUT, "CASME-Labels.csv" ))
                        pd.DataFrame.to_csv( feats, os.path.join( OUT, "Gabor-%s-S%d-O%d-H%d-W%d-nR%d.csv" ) % (method, nScales, nOrient, cp.nh, cp.nw, cp.nRect ))
                    else:
                        print "Failboat"
  

            else: 
                for nRect in rects:
                    cp = CASMEParser( method, nScales, nOrient, 0, nRect)

                    featureInfo, labelInfo, retval = cp.run()

                    if retval:
                        ## To DataFrames
                        labels = pd.DataFrame.from_dict( labelInfo, orient = 'index' )
                        feats = pd.DataFrame( featureInfo )
                        pd.DataFrame.to_csv( feats, os.path.join( OUT, "Gabor-%s-S%d-O%d-H%d-W%d-nR%d.csv" ) % (method, nScales, nOrient, cp.nh, cp.nw, cp.nRect ) )
                    else:
                        print "Failboat"
  

    



#######################################################










 
             