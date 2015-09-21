import numpy as np
import math
w = [[120,130,140],[115,120,130],[100,115,120]]     #template
f = [[110,120,135],[120,115,95],[100,105,90]]       #image frame
f2 = [[90,120,230],[120,75,95],[100,11,90]]       #image frame


      

def response1( w, f ):                         
    fr = np.ravel( f )
    wr = np.ravel( w )

    ws = wr - np.mean( w )
    fs = fr - np.mean( f )

    #print ws
    #print fs

    #print ws ** 2
    #print fs ** 2

    num = np.dot( np.transpose( ws ), fs )
    den = math.sqrt( np.dot( np.transpose( ws**2), fs**2 ) )   
    r = num / den
    return r

def response2( w, f ):
    r1= 0
    for s in range( 2 ):
        for t in range( 2 ):
            wup =   w[s][t] - np.mean( w )
            fup =  f[s][t] - np.mean( f )
            num = wup * fup 
            if num == 0:
                r1 += 0
            else:
                den = math.sqrt( ( wup ** 2 ) + ( fup ** 2) )
                r1+= num/den 
    return r1


def response3( w, f ):
    ws = 0
    fs = 0
    for s in range( 2 ):
        for t in range( 2 ):
            wup =   w[s][t] - np.mean( w )
            fup =  f[s][t] - np.mean( f )
            ws += wup / math.sqrt(     )
            den = math.sqrt( ( wup ** 2 ) * ( fup ** 2) )
            r1+= num/den 

    return r1

response1( w, f )
response1( w, f2 )

response2( w, f )
response2( w, f2 )

#    r1 = 0
#    ws = 0
#    fs = 0
#    for s in range( 2 ):
#        for t in range( 2 ):
#            
#            num = ( w[s][t] - np.mean( w )  ) * ( f[s][t] - np.mean( f ) )
#            if num == 0:
#                r1 += 0
#            else:
#                den = math.sqrt( ( (w[s][t] - np.mean( w ))** 2  ) * ( (f[s][t] - np.mean( f ) )**2 ) )   
#                r1+= num/den 
#    return r1


import cv2

