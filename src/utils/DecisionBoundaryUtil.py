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
    AUTHOR: Dominic Cripps
    DATE CREATED: UNKNOWN
    PREVIOUS MAINTAINER: Daniel Ferring
    Date Last Modified: 20/02/2023

    Used to acquire the values required to create the heatmap.
    Uses the decison tree fresholds to determine the steps between
    values and the training data itself to determine the heatmap
    bounds.

    Inputs:
    model: The model to be parsed
    featureDivisions: The Number of features used in the model
    trainingData: The data set used to train the model
    """
    def getModelData(self, model, featureDivisions, trainingData):
        smallestThreshold = [None, None]
        largestThreshold = [None, None]
        buffers = [None, None]
        steps = [None, None]
        
        #Calculates the steps (value intervals) for the heatmap creation
        count = 0
        for x in featureDivisions:
            for i in range(0, model.tree_.node_count):
                tempVal = model.tree_.threshold[i]
                if(tempVal != _tree.TREE_UNDEFINED and model.tree_.feature[i] == x):
                    if(largestThreshold[count] == None or tempVal > largestThreshold[count]):
                        largestThreshold[count] = tempVal
                    if(smallestThreshold[count] == None or tempVal < smallestThreshold[count]):
                        smallestThreshold[count] = tempVal

            buffers[count] = (largestThreshold[count] - smallestThreshold[count]) / 5
            largestThreshold[count] += buffers[count]
            smallestThreshold[count] -= buffers[count]
            steps[count] = buffers[count] / 20
            count+=1

        #Stores minimum values for x and y
        heatmapMins = []
        #Stores maximum values for x and y
        heatmapMaxs = []

        #Finds the min and max values of x and y for each feature
        instances = trainingData[0]
        for i in instances:
            min = instances[i].min()
            max = instances[i].max()
            buffer = (max - min) / 10
            heatmapMins.append(min - buffer)
            heatmapMaxs.append(max + buffer)

        #Stores the values required to create the heatmap
        modelData = []

        #Generates the values required to create the heatmap
        for j in range (0, len(featureDivisions)):
            tempModelData = []

            divisions = (heatmapMaxs[j] - heatmapMins[j]) / steps[j]
            for i in range (0, int(divisions)):
                tempModelData.append(heatmapMins[j] + (i * steps[j]))
            modelData.append(tempModelData)

        return modelData

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
        modelData = self.getModelData(model, [featureID], trainingData)
 
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
        modelData = self.getModelData(model, divisions, trainingData)
        
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