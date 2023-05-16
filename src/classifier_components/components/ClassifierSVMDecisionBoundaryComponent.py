from classifier_components.ClassifierComponent import ClassifierComponent
import plotly.graph_objects as go
import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd
from dash import dcc
from dash import html
from plotly.graph_objs import *
from utils.DecisionBoundaryUtil import DecisionBoundaryUtil
from utils.DecisionBoundaryUtil import DecisionBoundaryUtil
import numpy as np

"""

AUTHOR: Alfred Greenwood
DATE CREATED: 03/03/2023
PREVIOUS MAINTAINER: Alfred Greenwood
DATE LAST MODIFIED: 29/04/2023

Child of 'ClassifierComponent', this class defines an
appropriate 'componentLayout' to represent user input.
Displays a scatter graph of all data (training and testing)
alongside a number of hyperplanes produced by the machine
learning model to seperate the classifiers. Only works for
2 dimensions and for linear SVM kernels.

Inputs:
modelInfo : contains all the information relating to the model 
            to be represented (Defined in SettingCallbacks.py)
            in the form of a dictionary. Relevant keys are 
            described below:

        modelData:
            Contains the trained machine learning model
        trainingData:
            Contains the pandas dataset representing the data used for training
            SVM
        testingData:
            Contains the pandas dataset representing the data used for testing
            SVM
        colourKey:
            Contains a dictionary mapping the data classifiers to colours so that
            the colours of any graphs do not change. Additionally used to determine
            which classifiers are compared to which from the SVC coefficients
"""
class ClassifierSVMDecisionBoundaryComponent(ClassifierComponent):
    def __init__(self, modelInfo):
        # Save machine learning model
        self.svc = modelInfo["modelData"]
                
        # Name component title and add tooltips
        self.componentTitle = html.Span(
            dmc.Tooltip(
                label = html.Div(children = [
                    # HTML for tooltip
                    html.H1("SVM decision boundary"),
                    html.P("Support vector machines (SVM) are a machine learning method that utilises a set"),
                    html.P("of hyperplanes. These hyperplanes seperate the machine learning models divide between"),
                    html.P("two classifiers, assigning predicted values to marked categories. The model predicts"),
                    html.P("for any number of input training features and supports any SVM Kernel. However this"),
                    html.P("component will only support 2 dimensional linear Kernels.")
                    ]),
                children=[html.P("SVM Decision boundary")],
                id="svm-tooltip",
                className ="svmToolTip",
                withArrow = True,
            ))
        
        # Check for whether 2 inputs are given, any other number will not work
        if(len(modelInfo["modelData"].feature_names_in_) > 2):
            self.graph = html.P("Higher Dimensions are not implemented")
        elif(len(modelInfo["modelData"].feature_names_in_) <= 1):
            self.graph = html.P("More than 1 dimension is required")
        else:
            # Check if SVC kernel is linear, otherwise the visualisation will not work
            if(self.svc.kernel == "linear"):
                # Save the features of the training data used, to act as x and y axis later
                dataKeys = modelInfo["modelData"].feature_names_in_

                # Save a key for the colours, the colour keys are saved in the order that
                # the hyperplanes are stored. This means it not just acts to maintain consistency
                # in the graphs colouring but also figure out which hyperplane correlates to which
                # two classifiers
                key = modelInfo["colourKey"]

                # Unique classifiers are put into an array in correct order
                uniqueClassifiers = list(key.keys())

                # Coefficients works in order of all pairs from the first classifier to the last. As
                # using the unique classifiers above, this array generates a list of all pairs for the
                # unique classifiers sharing the same index as the machine learning models hyperplane
                # coeficients
                planePairs = [(a, b) for index, a in enumerate(uniqueClassifiers) for b in uniqueClassifiers[index + 1:]]

                # find minimum and maximum values across the training and testing data to find the smallest and
                # largest X values
                minX = min(float(modelInfo["trainingData"][0][dataKeys[0]].min()), float(modelInfo["testingData"][0][dataKeys[0]].min()))
                maxX = max(float(modelInfo["trainingData"][0][dataKeys[0]].max()), float(modelInfo["testingData"][0][dataKeys[0]].max()))

                # Generate a numpy array from the largest and smallest X values to map hyperplanes to
                xx = np.linspace(minX, maxX)

                # generate empty pandas dataframe to store hyperplane information
                hyperPlanes = pd.DataFrame(columns=["Classifier","yy", "upper", "lower", "xx"])
                hyperPlane = []
            
                # Iterate through all hyperplanes
                for i in range(0, len(self.svc.coef_)):
                    # Find first SVC coefficient
                    w = self.svc.coef_[i]
                    a = -w[0] / w[1]
                    # Map all Y coordinates of the line to the values within min and max X made earlier        
                    yy = a * xx - (self.svc.intercept_[i]) / w[1]

                    # Create the upper and lower bounds of the hyper-plane
                    b = self.svc.support_vectors_[0]
                    yy_down = a * xx + (b[1] - a * b[0])
                    b = self.svc.support_vectors_[-1]
                    yy_up = a * xx + (b[1] - a * b[0])

                    # Append X and Y coordinates of hyperplane i to a dataframe of all positions of
                    # hyperplane i. As i matches the relevant pair of classifiers above sets the
                    # classifier as the correlating pair of classifiers.
                    hyperPlane.append(pd.DataFrame(({"Classifier": planePairs[i][0]+"/"+planePairs[i][1], "yy": yy, "upper": yy_up, "lower": yy_down, "xx": xx})))
               
                # Concat all hyperplane dataframe arrays into a singular array that contains all hyperplanes
                hyperPlanes = pd.concat(hyperPlane)

                # Generate scatter graph object through
                boundUtil = DecisionBoundaryUtil()
                scatterData = boundUtil.plotScatterGraph(modelInfo["trainingData"], modelInfo["testingData"], modelInfo["colourKey"], modelInfo["shapeKey"])
                scatterData.update(showlegend = False)

                # Append all hyperplanes to the scatter graph object
                line1 = px.line(hyperPlanes, x=hyperPlanes["xx"], y=hyperPlanes["yy"], color=hyperPlanes["Classifier"])
                
                # Create graph object figure and add hyperplane information to it
                self.fig=go.Figure(data=line1.data)
                # Add scatter graph to figure
                self.fig.add_trace(scatterData)
                
                # Calculate the minimum and maximum Y values from the training and testing data
                minY = min(float(modelInfo["trainingData"][0][dataKeys[1]].min()), float(modelInfo["testingData"][0][dataKeys[1]].min()))
                maxY = max(float(modelInfo["trainingData"][0][dataKeys[1]].max()), float(modelInfo["testingData"][0][dataKeys[1]].max()))
                # Calculate the differences between the largest and smallest Y coordinates, then add
                delta = maxY-minY
                # Increase the size of the minimum and maximum Y coordinates by 5% of the difference of
                # the largest and smallest y values to act as extra space padding on the scatter graph
                minY -= delta*0.05
                maxY += delta*0.05

                # Update the look of the scatter graph
                self.fig.update_layout(
                    coloraxis_showscale=False,

                    # Add labels to the X and Y axis of the graph
                    xaxis_title=dataKeys[0],
                    yaxis_title=dataKeys[1],

                    # Configure max values on axis to be 5% of the largest and smallest values on the y axis
                    # to prevent near-vertical Hyperplanes taking up the entire y axis
                    yaxis_range=[minY, maxY],

                    # Update axis names
                    margin={'t': 50,'l':10,'b':5,'r':30},

                    # Customise the colours of the plot
                    paper_bgcolor="#232323", 
                    font_color = "#f5f5f5", 
                    plot_bgcolor="#232323")

                # Create graph from the figure and add it to the SVM decision boundary component
                self.graph = dcc.Graph(figure = self.fig)
            else:
                self.graph = html.P("SVM decision boundaries can only be visualised currently for linear SVM kernels")
        
        # Create contents of the component
        self.componentChildren = html.Div(self.graph)