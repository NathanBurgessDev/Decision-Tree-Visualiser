from classifier_components.ClassifierComponent import ClassifierComponent
import plotly as py
from utils.Util import GraphUtil as gu
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import dcc
from dash import html
from plotly.graph_objs import *
from utils.DecisionBoundaryUtil import DecisionBoundaryUtil
from sklearn.inspection import DecisionBoundaryDisplay as DBD
from utils.DecisionBoundaryUtil import DecisionBoundaryUtil
import numpy as np

"""

AUTHOR: Alfred Greenwood
DATE CREATED: 03/03/2023
PREVIOUS MAINTAINER: Alfred Greenwood
DATE LAST MODIFIED: 29/04/2023

Child of 'ClassifierComponent', this class defines an
appropriate 'componentLayout' to represent user input.
The user will be able to input feature values and a
classification will be returned, alongside the models accuracy.

Inputs:
modelInfo : contains all the information relating to the model 
            to be represented (Defined in SettingCallbacks.py)

Inputs:
    modelInfo: Dictionary that contains the following data:
        modelData:
        trainingData:
        testingData:
        modelArguments:
        testTrainSplit:
        classifierType:
        modelName:
"""
class ClassifierSVMDecisionBoundaryComponent(ClassifierComponent):
    def __init__(self, modelInfo):
        self.svc = modelInfo["modelData"]
                
        self.componentTitle = "SVM Decision boundary"
        
        if(len(modelInfo["modelData"].feature_names_in_) > 2):
            self.graph = html.P("Higher Dimensions are not yet implemented")
        elif(len(modelInfo["modelData"].feature_names_in_) <= 1):
            self.graph = html.P("More than 1 dimension must be implemented")
        else:
            features = modelInfo["trainingData"][0]

            key = modelInfo["colourKey"]

            print(key)

            uniqueClassifiers = list(key.keys())
            planePairs = [(a, b) for index, a in enumerate(uniqueClassifiers) for b in uniqueClassifiers[index + 1:]]


            # Need a better name for this variable
            classifiers = modelInfo["trainingData"][1]
            
            dataKeys = features.keys()

            #hyperPlanes = []

            xx = np.linspace(modelInfo["trainingData"][0][dataKeys[0]].min(), modelInfo["trainingData"][0][dataKeys[0]].max())
            hyperPlanes = pd.DataFrame(columns=["Classifier","yy", "upper", "lower", "xx"])
            hyperPlane = []
            
            if(self.svc.kernel == "linear"):
                for i in range(0, len(self.svc.coef_)):
                    w = self.svc.coef_[i]
                    a = -w[0] / w[1]                    
                    yy = a * xx - (self.svc.intercept_[i]) / w[1]

                    b = self.svc.support_vectors_[0]
                    yy_down = a * xx + (b[1] - a * b[0])
                    b = self.svc.support_vectors_[-1]
                    yy_up = a * xx + (b[1] - a * b[0])
                    
                    hyperPlane.append(pd.DataFrame(({"Classifier": planePairs[i][0]+"/"+planePairs[i][1], "yy": yy, "upper": yy_up, "lower": yy_down, "xx": xx})))
                        
                hyperPlanes = pd.concat(hyperPlane)

                classifiers = classifiers.map(key)

                axes = modelInfo["modelData"].feature_names_in_

                print(axes)
                boundUtil = DecisionBoundaryUtil()
                scatterData = boundUtil.plotScatterGraph(modelInfo["trainingData"], modelInfo["testingData"], modelInfo["colourKey"], modelInfo["shapeKey"])
                scatterData.update(showlegend = False)
                """
                scatterData = px.scatter(x=modelInfo["trainingData"][0][dataKeys[0]],
                                         y=modelInfo["trainingData"][0][dataKeys[1]],
                                         color=classifiers,
                                         )"""

                line = px.line(hyperPlanes, x=hyperPlanes["xx"], y=hyperPlanes["yy"], color=hyperPlanes["Classifier"])

                dat = line.data 
                self.fig=go.Figure(data=dat)
                self.fig.add_trace(scatterData)
                
                minY = min(float(modelInfo["trainingData"][0][dataKeys[1]].min()), float(modelInfo["testingData"][0][dataKeys[1]].min()))
                maxY = max(float(modelInfo["trainingData"][0][dataKeys[1]].max()), float(modelInfo["testingData"][0][dataKeys[1]].max()))
                delta = maxY-minY
                minY -= delta*0.05
                maxY += delta*0.05

                self.fig.update_layout(
                    coloraxis_showscale=False,

                    # Configure max values on axis to be 5% of the largest and smallest values on the y axis
                    # to prevent near-vertical Hyperplanes taking up the entire y axis
                    yaxis_range=[minY, maxY],

                    # Update axis names
                    margin={'t': 50,'l':10,'b':5,'r':30},

                    # Customise the colours of the plot
                    paper_bgcolor="#232323", 
                    font_color = "#f5f5f5", 
                    plot_bgcolor="#232323")


                self.graph = dcc.Graph(figure = self.fig)
            else:
                self.graph = html.P("SVM decision boundaries can only be visualised currently for linear SVM kernels")
        
        
        self.componentChildren = html.Div(self.graph)