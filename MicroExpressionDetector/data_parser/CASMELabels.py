import pandas as pd
import math
import numpy as np
import re

class CASMELabels( object ):
    @staticmethod
    def getLabelInfo( sub, vid, df, videoKey ):
   
        # Query master table given subject and video
        instance = df.query( 'Subject == %d & Filename == "%s"' % ( int(sub.replace( "sub", "" )), vid) )
    
        # Get important stuff from there
        onset = int( instance.OnsetFrame.values[0] )
        apex =  instance.ApexFrame.values[0] 
        offset = int( instance.OffsetFrame.values[0] )

        s,v = videoKey ## unpack (subject, video, frame)
    

        ## double check boundaries of onset/apex/offset
        accum = {
            "subject" : s,
            "video" : v,
            }
        params = { 
            "emotion" : instance['Estimated Emotion'].values[0], # replace string with num
            "onset" : onset,
            "apex" : CASMELabels.hasApex( apex ),
            "offset" : offset
            }

        return accum, params
    @staticmethod
    def hasApex( a ):
        if a == '/' :
            return None
        else:
            return int( a )

    @staticmethod
    def isOnset( f, onset, apex ):
        return f in range( onset, apex )

    @staticmethod
    def isApex( f, apex ):
        return f == apex

    @staticmethod
    def isOffset( f, apex, offset ):
        return f in range( apex + 1, offset + 1 )

    @staticmethod
    def getEmotion( vidEmotion, frameInfo  ):
        # Translation between string and integer reps of emotions
        emoji = { 'happiness' : 0,
                'disgust' : 1,
                'repression' : 2,
                'fear': 3,
                'sadness' : 4,
                'others' : 5,
                'surprise' : 6,
                'neutral' : 7
                }
    
        if frameInfo['isOnset'] or frameInfo['isApex'] or frameInfo['isOffset']:
            return emoji[ vidEmotion ]
        else:
            return emoji['neutral']
    
    @staticmethod
    def getFrameParams( labelInfo, labelParams, f, frame ):
        if labelParams['apex'] is None:  #estimate halfway as apex
            apex =  int( math.floor( (labelParams['offset'] - labelParams['onset']) / 2 ) )
        else:
            apex = labelParams['apex']
        orgFrame =  map( int, re.findall( r'\d+', frame ))[0]                              
        accum = {
            "frame" : f,
            "isOnset" : CASMELabels.isOnset( orgFrame, labelParams['onset'], apex ),
            "isApex" : CASMELabels.isApex( orgFrame, labelParams['apex'] ),
            "isOffset" :  CASMELabels.isOffset( orgFrame, apex, labelParams['offset'] )
            }

        accum.update( { "emotion" : CASMELabels.getEmotion( labelParams[ 'emotion' ], accum) } )
        return accum
