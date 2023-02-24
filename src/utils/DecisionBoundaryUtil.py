from sklearn.tree import _tree
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import math
from dash import dcc

"""
AUTHOR: Daniel Ferring
DATE CREATED: 19/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 21/02/2023

Used to create visualisations of a given model's decision
boundaries. Can create either 1D or 2D representations.
"""
class DecisionBoundaryUtil():

    """
    AUTHOR: Daniel Ferring
    DATE CREATEDD: 24/02/2023
    PREVIOUS MAINTAINER: Daniel Ferring
    DATE LAST MODIFIED: 24/03/2023

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
    AUTHOR: Dominic Cripps
    DATE CREATED: UNKNOWN
    PREVIOUS MAINTAINER: Daniel Ferring
    Date Last Modified: 20/02/2023

    Generates a visual representation of the decision boundary
    of a 1 dimensional decision tree. Returns a graph object
    within an array.

    Inputs:
    model: The model to be represented
    featureID: The ID of the feature being plotted
    trainingData: The data set used to train the model
    """
    def decisionBoundaries1D(self, model, featureID, trainingData):

        decisionBoundary = []

        #Gets the data required to create the heatmap
        modelData = self.getHeatmapValues(trainingData)
 
        #Extracts relevant data from the training data
        dataframe = pd.DataFrame(data = modelData[featureID], columns = [str(model.feature_names_in_[featureID])])

        #Predicts classifications using the model
        Z = model.predict(dataframe)

        classifications = [None] * len(Z)
        modelText = [''] * len(Z)
        count = 0 
        for x in model.classes_:
            for i in range (0, len(Z)):
                if(Z[i] == str(x)):
                    classifications[i] = count
                    modelText[i] = str(x)
            count+=1


        # Make a Heatmap using the array of values we previously created
        trace = go.Heatmap(z=classifications, 
                        x = modelData[featureID], 
                        y = [0] * len(modelData[featureID]), 
                        text = modelText, 
                        colorscale='sunset',
                        hoverinfo='text',
                        colorbar=dict(bgcolor = "#232323"),
                        showscale=False)

        #Extracts data instances to be plotted as a scatter graph
        instances = trainingData[0]

        #Creates the scatter graph to be overlaid on the decison boundary
        trace2 = go.Scatter(x=instances.iloc[:, 0], y = [0] * len(modelData[featureID]), 
                            mode='markers',
                            showlegend=False,
                            marker=dict(size=10,
                                        colorscale='sunsetdark',
                                        line=dict(color='black', width=1)),
                           )
 
        #Creates the graph object, adding the heatmap to it
        graph = go.Figure(data=trace)
        graph.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color = "#f5f5f5",
            autosize=True, 
            margin={'t': 50,'l':10,'b':5,'r':30}, 
        )  
        #Adds the scatter plot to the graph
        graph.add_trace(trace2)

        # Set the titles of the X and Y Axis
        graph.update_layout(
            xaxis_title=str(model.feature_names_in_[featureID]), 
        )
        
        graph.update_yaxes(visible=False, showticklabels=False)

        decisionBoundary.append(dcc.Graph(figure = graph))

        return decisionBoundary


    """
    AUTHOR: Dominic Cripps
    DATE CREATED: UNKNOWN
    PREVIOUS MAINTAINER: Daniel Ferring
    Date Last Modified: 20/02/2023

    Generates a visual representation of the decision boundary
    of a 2 dimensional decision tree. Returns a graph object
    within an array.

    Inputs:
    model: The model to be represented
    divisions: The IDs of the two features being plotted
    trainingData: The data set used to train the model
    """
    def decisionBoundaries2D(self, model, divisions, trainingData):

        decisionBoundary = []

        #Gets the data required to create the heatmap
        modelData = self.getHeatmapValues(trainingData)
        
        data = []

        #Collects the data required for each feature and combines them
        tempData = []
        for x in modelData[0]:
            for y in modelData[1]:
                tempData.append(x)
        data.append(tempData)

        tempData = []
        for y in modelData[1]:
            for x in modelData[0]:
                tempData.append(y)
        data.append(tempData)
    
        modelDataCombination = []
        for y in modelData[1]:
            for x in modelData[0]:
                modelDataCombination.append([x, y])

        dataframe = pd.DataFrame(data = modelDataCombination, columns = model.feature_names_in_)

        #Uses the model to predict classifications
        Z = model.predict(dataframe)

        classifications = Z
        modelText = [''] * len(Z)
        count = 0 

        for x in model.classes_:
            for i in range (0, len(Z)):
                if(Z[i] == str(x)):
                    classifications[i] = count
                    modelText[i] = str(x)
            count+=1

        classifications = classifications.reshape(len(modelData[1]), len(modelData[0]))
        modelText = np.reshape(modelText, (len(modelData[1]), len(modelData[0])))

        #Creates a heatmap using the relevant data
        trace = go.Heatmap(z=classifications, 
                        x = modelData[0], 
                        y = modelData[1], 
                        text = modelText, 
                        colorscale='sunset',
                        hoverinfo='text',
                        colorbar=dict(bgcolor = "#232323"),
                        showscale=False)

        #Extracts data instances to be plotted as a scatter graph
        instances = trainingData[0]

        #Creates the scatter graph to be overlaid on the heatmap
        trace2 = go.Scatter(x=instances.iloc[:, 0], y=instances.iloc[:, 1], 
                            mode='markers',
                            showlegend=False,
                            marker=dict(size=10,
                                        colorscale='sunsetdark',
                                        line=dict(color='black', width=1))
                           )

        #Creates the graph object, adding the heatmap to it
        graph = go.Figure(data = trace)
        graph.update_layout(
            paper_bgcolor="#232323",
            plot_bgcolor="#232323",
            font_color="#f5f5f5",
            autosize=True, 
            margin={'t': 50,'l':10,'b':5,'r':30}, 
        ) 
        #Adds the scatter plot to the graph
        graph.add_trace(trace2)

        # Set the titles of the X and Y Axis
        graph.update_layout(
            xaxis_title=str(model.feature_names_in_[0]),
            yaxis_title=str(model.feature_names_in_[1]))
        
        decisionBoundary.append(dcc.Graph(figure = graph))

        return decisionBoundary