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
import numpy as np

"""

AUTHOR: Alfred Greenwood
DATE CREATED: 03/03/2023
PREVIOUS MAINTAINER: Alfred Greenwood
DATE LAST MODIFIED: 03/03/2023

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
        
        if(len(modelInfo["modelData"].feature_names_in_) > 3):
            self.graph = html.P("Higher Dimensions are not yet implemented")
        elif(len(modelInfo["modelData"].feature_names_in_) == 3):
            features = modelInfo["trainingData"][0]

            # Need a better name for this variable
            classifiers = modelInfo["trainingData"][1]

            dataKeys = features.keys()
            
            self.fig = go.FigureWidget()
            z = lambda x,y: (-self.svc.intercept_[0]-self.svc.coef_[0][0]*x-self.svc.coef_[0][1]*y) / self.svc.coef_[0][2]

            #tmp = np.linspace(-2,2,51)
            #x,y = np.meshgrid(tmp,tmp)

            for X in classifiers.unique():
                for Y in classifiers.unique():
                    if X != Y:
                        xm, xM = X[:,0].min(), X[:, 0].max()
                        ym, yM = X[:,1].min(), X[:, 1].max()
                        x = np.linspace(xm, xM, 10)
                        y = np.linspace(ym, yM, 10)
                        x, y =np.meshgrid(x, y)
                        self.fig.add_surface(x=x, y=y, z=z(x,y), colorscale='Greys', showscale=False, opacity=0.9)

            self.fig.add_scatter3d(x=dataKeys[0], y=dataKeys[1], z=dataKeys[2], mode='markers', marker=dict(color=classifiers), showlegend=True)
            
            self.fig.update_layout(
                # Update axis names
                autosize=True, 
                margin={'t': 50,'l':10,'b':5,'r':30},

                # Customise the colours of the plot
                paper_bgcolor="#232323", 
                font_color = "#f5f5f5", 
                plot_bgcolor="#232323")


            self.graph = dcc.Graph(figure = self.fig)

        else:
            features = modelInfo["trainingData"][0]

            # Need a better name for this variable
            classifiers = modelInfo["trainingData"][1]

            dataKeys = features.keys()
            
            self.fig = go.FigureWidget()
                        
            self.fig.add_scatter(x=modelInfo["trainingData"][0][dataKeys[0]], y=modelInfo["trainingData"][0][dataKeys[1]], mode='markers', marker=dict(color=classifiers), showlegend=True)
            
            self.fig.update_layout(
                # Update axis names
                autosize=True, 
                margin={'t': 50,'l':10,'b':5,'r':30},

                # Customise the colours of the plot
                paper_bgcolor="#232323", 
                font_color = "#f5f5f5", 
                plot_bgcolor="#232323")


            self.graph = dcc.Graph(figure = self.fig)
        
        
        self.componentChildren = html.Div(self.graph)