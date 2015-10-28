from data_parser.CASMEParser import CASMEParser

cp = CASMEParser( 5, 8, 14, 11 )
featureInfo, labelInfo = cp.run()
  

    



#######################################################





labels = pd.DataFrame.from_dict( labelInfo, orient = 'index' )

#labels[ (labels['video'] == 0) & (labels['subject'] == 0) ]


 
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
 
clf = AdaBoostClassifier( 
    base_estimator = DecisionTreeClassifier( min_samples_leaf = 25, min_samples_split = 25),
    n_estimators = 50,
    algorithm='SAMME' )




X = featureInfo
Y = labels['emotion']
clf.fit( X, Y ) 


             