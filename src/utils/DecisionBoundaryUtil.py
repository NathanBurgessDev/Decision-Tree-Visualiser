from sklearn.tree import _tree
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import math
from dash import dcc

"""
AUTHOR: Daniel Ferring
DATE CREATED: 19/02/2023
PREVIOUS MAINTAINER: Daniel Ferring
DATE LAST MODIFIED: 24/02/2023

Used to create visualisations of a given model's decision
boundaries. Can create either 1D or 2D representations.
"""
class DecisionBoundaryUtil():

    """
    AUTHOR: Daniel Ferring
    DATE CREATEDD: 24/02/2023
    PREVIOUS MAINTAINER: Daniel Ferring
    DATE LAST MODIFIED: 24/02/2023

    Generates the values required to create a heatmap using values from
    the model's training data.

    INPUTS:
    trainingData: the data used to train the model
    """
    def getHeatmapValues(self, trainingData):

        #Stores minimum values for each feature
        mins = []
        #Stores maximum values for each feature
        maxs = []

        #Extracts feature values from the training data
        features = trainingData[0]

        #Finds the minimum and maximum values for each feature
        for i in features:
            min = features[i].min()
            max = features[i].max()

            #Applies a buffer so that the visualisation extends a bit beyond each 
            #min and max value (looks nicer)
            buffer = (max - min) / 10
            mins.append(min - buffer)
            maxs.append(max + buffer)
        
        #Stores the values that will be used to create the heatmap
        heatmapValues = []

        #The divisions for each axis of the heatmap grid, increasing this value will increase
        #the resolution of the decision boundary at the expense of performance
        divisions = 150

        #Creates a list of values for each feature (each list becomes an axis in the heatmap)
        #and appends them to heatmapValues
        for i in range(0, len(features.columns)):
            featureValues = []

            #Uses the range in values and number of divisions to calculate the step needed between each value
            step = (maxs[i] - mins[i]) / divisions

            #Generates the values for the feature's list
            for j in range(0, divisions):
                value = mins[i] + (step * j)
                featureValues.append(value)
            
            heatmapValues.append(featureValues)
        
        return heatmapValues
    
    """
    AUTHOR: Daniel Ferring
    DATE CREATED: 24/02/2023
    PREVIOUS MAINTAINER: Daniel Ferring
    DATE LAST MODIFIED: 24/02/2023
    --Uses logic initially implemented by Dominic Cripps--

    Creates the heatmap object used to represent the decision boundaries of a given model

    INPUTS:
    model: The decision tree model to be represented
    trainingData: The data used to train the model
    """
    def plotHeatmap(self, model, trainingData):
        #creates lists used to create the heatmap
        heatmapValues = self.getHeatmapValues(trainingData)

        #List of features used to train the model
        features = model.feature_names_in_

        #Uses the data of the single feature if tree is one-dimensional
        if len(features) == 1:
            predictData = heatmapValues[0]
        #Combines the data of both features if the tree is two-dimensional
        else:
            predictData = []
            for y in heatmapValues[1]:
                for x in heatmapValues[0]:
                    predictData.append([x,y])
        
        #Creates a data frame with predictData as the rows and features as the columns
        predictDF = pd.DataFrame(data = predictData, columns = features)
        #Predicts the classifications for the data frame
        predictions = model.predict(predictDF)

        #List containing the numerical representation of each classification
        classifications = [None] * len(predictions)
        #List containing string names of each classification
        classificationsText = [''] * len(predictions)
        #Used to assign a numerical value to each class
        classificationNum = 0

        #Gets values for the classifications and clasificationsText lists
        for i in model.classes_:
            for j in range(0, len(predictions)):
                if predictions[j] == str(i):
                    classifications[j] = classificationNum
                    classificationsText[j] = str(i)
                classificationNum += 1
        
        #Regardless of tree dimension the first feature in heatmapValues will be plotted on the x axis
        xData = heatmapValues[0]
        
        #Creates values for the y axis in the case of a one-dimensional tree
        if len(features) == 1:
            yData = [0] * len(xData)
        #Reshapes arrays as necessary and uses the second feature's values for the y axis if the 
        #tree has two dimensions
        else:
            classifications = np.reshape(classifications, (len(heatmapValues[0]), len(heatmapValues[1])))
            classificationsText = np.reshape(classificationsText, (len(heatmapValues[0]), len(heatmapValues[1])))
            yData = heatmapValues[1]
        
        #Creates the hetmap object
        heatmap = go.Heatmap(
            z = classifications, 
            x = xData, 
            y = yData, 
            text = classificationsText, 
            colorscale = 'sunset',
            hoverinfo = 'text',
            colorbar = dict(bgcolor = "#232323"),
            showscale = False
        )

        return heatmap

    """
    AUTHOR: Daniel Ferring
    DATE CREATED: 24/02/2023
    PREVIOUS MAINTAINER: Daniel Ferring
    DATE LAST MODIFIED: 24/02/2023

    Plots a scatter graph of the training data used to train the model.

    INPUTS:
    trainingData: the data to be plotted
    """
    def plotScatterGraph(self, trainingData):
        #Extracts feature values from the training data
        instances = trainingData[0]

        #There will alwats be at least one feature, which is used as the x axis
        xPlot = instances.iloc[:, 0]

        #Creates the y axis for a one dimensional tree
        if len(instances.columns) == 1:
            yPlot = [0] * len(instances)
        #Uses the values of the second feature in the case of a two dimensional tree
        else:
            yPlot = instances.iloc[:, 1]
        
        #Creates the scatter graph object
        scatter = go.Scatter(x=xPlot, 
                            y = yPlot, 
                            mode='markers',
                            showlegend=False,
                            marker=dict(size=10,
                                        colorscale='sunsetdark',
                                        line=dict(color='black', width=1))
                            )
        
        return scatter

    """
    AUTHOR: Daniel Ferring
    DATE CREATED: 24/02/2023
    PREVIOUS MAINTAINER: Daniel Ferring
    DATE LAST MODIFIED: 24/02/2023

    Combines the heatmap and the scatter plot into a single
    graph object to represent the decision boundaries of a
    given model

    INPUTS:
    model: The decision tree model to be represented
    trainingData: the data used to train the model
    """
    def generateDecisionBoundary(self, model, trainingData):
        #Stores the created graph object for use in the wider system
        decisionBoundary = []

        #Creates heatmap and scatter plot objects
        heatmap = self.plotHeatmap(model, trainingData)
        scatter = self.plotScatterGraph(trainingData)

        #Creates the graph object, the heatmap is overlaid with the scatter graph
        graph = go.Figure(data = heatmap)
        graph.add_trace(scatter)

        #Labels x axis and makes the graph match the aesthetic of the rest of the app
        graph.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color = "#f5f5f5",
            autosize=True, 
            margin={'t': 50,'l':10,'b':5,'r':30},
            xaxis_title = str(model.feature_names_in_[0])
        )

        #Hides y axis if one-dimensional, labels it if two-dimensional
        if len(model.feature_names_in_) == 1:
            graph.update_yaxes(visible=False, showticklabels=False)
        else:
            graph.update_layout(
                yaxis_title = str(model.feature_names_in_[1])
            )
        
        decisionBoundary.append(dcc.Graph(figure = graph))

        return decisionBoundary
