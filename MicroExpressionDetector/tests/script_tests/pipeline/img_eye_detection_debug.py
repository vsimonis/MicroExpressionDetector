import cv2
from matplotlib import pyplot as plt

def preview( img ):
    plt.imshow( img, cmap = 'gray' )
    plt.show()

print sub
print vid
print frame 





I = cv2.imread( os.path.join( DATA, sub, vid, frame )  )
I1 = cv2.cvtColor( I, cv2.COLOR_BGR2GRAY ) 

preview(I1)


eye_cascade = cv2.CascadeClassifier('C:\\OpenCV\\data\\haarcascades\\haarcascade_eye.xml')
eyes = eye_cascade.detectMultiScale( I1 )

