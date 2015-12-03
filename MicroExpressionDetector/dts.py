

### AdaBoost
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import math
import pickle
import os
 
#clf = AdaBoostClassifier( 
#    base_estimator = DecisionTreeClassifier( min_samples_leaf = 25, min_samples_split = 25),
#    n_estimators = 50,
#    algorithm='SAMME' )



OUT = "C:\Users\Valerie\Desktop\output"
s, o, h, w = [9, 8, 28,23]
clf = DecisionTreeClassifier()
f = "Gabor-S%d-O%d-H%d-W%d.csv" % (s, o, h, w)
l = "CASME-labels.csv"
X = pd.DataFrame.from_csv( os.path.join( OUT, f ))

Y = pd.DataFrame.from_csv( os.path.join( OUT, l ) )

Y = labels['emotion']
clf.fit( X, Y ) 


