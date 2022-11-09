import sklearn_json as skljson
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import svm

irisDF = pd.read_excel("iris.xlsx")
irisInDF = irisDF.drop(['Species', 'Id'], axis = 1)
irisOutDF = irisDF['Species']
xTrain, xTest, yTrain, yTest = train_test_split(irisInDF, irisOutDF, test_size = 0.3)

irisDecisionTree = DecisionTreeClassifier(random_state=0).fit(xTrain, yTrain)
irisGradientBoosted = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,max_depth=1, random_state=0).fit(xTrain, yTrain)
irisSVM = svm.SVC().fit(xTrain, yTrain)

skljson.to_json(irisDecisionTree, "DecisionTreeClassifier_JSON")
skljson.to_json(irisGradientBoosted, "GradientBoostedClassifier_JSON")
skljson.to_json(irisSVM, "SVM_JSON")
