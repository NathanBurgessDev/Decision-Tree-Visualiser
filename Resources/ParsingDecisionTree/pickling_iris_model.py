import pickle
from sklearn.tree import _tree
from sklearn.datasets import load_iris
from sklearn import tree
import numpy as np
import pandas as pd


df = pd.read_csv('iris.csv')
X = df.iloc[:, 0:4] 
y = df['species_id']

model = tree.DecisionTreeClassifier()
model = clf.fit(X, y)

filename = 'finalized_model.sav'
pickle.dump(clf, open(filename, 'wb'))
