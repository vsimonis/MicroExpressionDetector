 import cv2
import imageProcessingHelp as iph

MAx_FRAMES = 10000
def processImage( videoFile ):
    nframes = 0
    cap = cv2.VideoCapture( videoFile )

    imageSet = {}
    fileHelp = {}
    key = 0
    c = 0


    while(nframes < MAX_FRAMES):
        face_cascade = cv2.CascadeClassifier(CASCADE)                                             )

        ret,img= cap.read()
        if not ret:
            break
        gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY)


        faces = face_cascade.detectMultiScale( gray, 1.3, 5)
        x,y,w,h = faces[0]
        
        info = {}
        d = {}
        j = 0
        roi_gray = gray[y:y+h, x:x+w]

        pyr, reg = iph.scalePyramid( imageIn   , NUMLEVELS, SIGMAPYR ,TAPSPYR)
        ## i iterates levels
        for i in range( len( pyr ) ):
            ## r are msers detected in image
            for r in reg[i]:
                ## Affine Normalization
                props = iph.regionProps( pyr[i], r, (key, i, j) )
                props['ncentroid'] = (props['centroid'][0] *2 ** i, props['centroid'][1] * 2 ** i )
                props['narea'] = props['area'] * 4 ** i
                props['level'] = i
                d[j] = props
                # j flattens all regions to be considered together
                j += 1

            info['TotalRegions'] = len(d)

        # ELIMINATE DUPLICATE REGIONS
        elim = []
        for r0, v0 in d.iteritems():
            ## Finer scale
            cx0 = v0['ncentroid'][0]
            cy0 = v0['ncentroid'][1]
            a0 = v0['narea']
            l0 = v0['level']

            ma0 =  v0['mal']
            for r1, v1 in d.iteritems():
                ## Coarser scale
                cx1 = v1['ncentroid'][0]
                cy1 = v1['ncentroid'][1]
                a1 = v1['narea']
                l1 = v1['level']
        

                ## Conditions
                if l1 - l0 != 1: # only compare to one coarser scale below
                    continue

                # Centroid within 4 pix
                if abs( cx0 - cx1 ) < 4 and abs( cy0 - cy1 )  < 4:
            
                    # Close areas
                    if abs ( a0 - a1 ) / max( a0, a1 ) < 0.2:
                        elim.append( r0 )
                        break
        
                # Small minor axes
                if l0 >= 1 :
                    if ma0 < 25:
                        elim.append( r0 )

        for el in elim:
            if el in d.iterkeys():
                d.pop( el )


        combDict = { key : { 'info' : info, 'regions': d } } 
        imageSet.update( combDict )
        #    print imageSet
        #    break
        key +=1
    return imageSet, fileHelp

            
            
