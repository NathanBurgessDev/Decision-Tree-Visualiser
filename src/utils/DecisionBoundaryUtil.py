import pandas as pd
import plotly.graph_objects as go
import numpy as np
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
    DATE CREATED: 24/02/2023
    PREVIOUS MAINTAINER: Daniel Ferring
    DATE LAST MODIFIED: 21/03/2023

    Generates the values required to create a heatmap using values from
    the model's training data.

    INPUTS:
    trainingData: the data used to train the model
    """
    def getHeatmapValues(self, trainingData, testingData):

        #Stores minimum values for each feature
        mins = []
        #Stores maximum values for each feature
        maxs = []

        #Extracts feature values from the training data
        features = pd.concat([trainingData[0], testingData[0]])

        #Finds the minimum and maximum values for each feature
        for i in features.columns:
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
    DATE LAST MODIFIED: 21/03/2023
    --Uses some logic initially implemented by Dominic Cripps--

    Creates the heatmap object used to represent the decision boundaries of a given model

    INPUTS:
    model: The decision tree model to be represented
    trainingData: The data used to train the model
    key: a dictionary mapping class strings to numerical values
    """
    def plotHeatmap(self, model, heatmapValues, key):

        #List of features used to train the model
        features = model.feature_names_in_

        #Uses the data of a single feature if tree is one-dimensional
        if len(features) == 1:
            predictData = heatmapValues[0]
        #Combines the data of both features if the tree is two-dimensional
        else:
            predictData = []
            for y in heatmapValues[1]:
                for x in heatmapValues[0]:
                    predictData.append([x, y])
        
        #Creates a data frame with predictData as the rows and features as the columns
        predictDF = pd.DataFrame(data = predictData, columns = features)
        #Predicts the classifications for the data frame
        predictions = model.predict(predictDF)

        #List containing the numerical values for each classification
        classifications = [None] * len(predictions)
        #List containing string names of each classification
        classificationsText = [''] * len(predictions)

        #Gets values for the classifications and clasificationsText lists
        for i in model.classes_:
            for j in range(0, len(predictions)):
                if predictions[j] == str(i):
                    classifications[j] = key[str(i)]
                    classificationsText[j] = str(i)
        
        #Regardless of tree dimension the first feature in heatmapValues will be plotted on the x axis
        xData = heatmapValues[0]
        
        #Creates values for the y axis in the case of a one-dimensional tree
        if len(features) == 1:
            yData = [0] * len(xData)
        #Reshapes arrays as necessary and uses the second feature's values for the y axis if the 
        #tree has two dimensions
        else:
            classifications = np.reshape(classifications, (len(heatmapValues[1]), len(heatmapValues[0])))
            classificationsText = np.reshape(classificationsText, (len(heatmapValues[1]), len(heatmapValues[0])))
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
    DATE LAST MODIFIED: 19/03/2023

    Plots a scatter graph of the test and training data of the model,
    used to give an understanding of the accuracy of the decision boundaries

    INPUTS:
    trainingData: the data used to train the model
    testingData: the data used to test the model
    key: a dictionary mapping class strings to numerical values
    """
    def plotScatterGraph(self, trainingData, testingData, key, shapeKey):

        #Custom colourscale used to ensure that markers are slightly darker than the boundaries
        markerColourscale = [[0.0, "rgb(234, 214, 84)"],
                            [1 / 6, "rgb(249, 178, 95)"],
                            [(1 / 6) * 2, "rgb(246, 134, 91)"],
                            [(1 / 6) * 3, "rgb(230, 96, 104)"],
                            [(1 / 6) * 4, "rgb(196, 69, 124)"],
                            [(1 / 6) * 5, "rgb(144, 80, 144)"],
                            [1.0, "rgb(63, 57, 114)"]]

        #Combines training and test data for instances and classifications
        instances = pd.concat([trainingData[0], testingData[0]])
        classifications = pd.concat([trainingData[1], testingData[1]])


        #Maps the classification strings to numberical values according to the key
        classificationsNum = classifications.map(key)
        classificationShapes = classifications.map(shapeKey)

        #There will alwats be at least one feature, which is used as the x axis
        xPlot = instances.iloc[:, 0]

        #Creates the empty y axis for a one dimensional tree
        if len(instances.columns) == 1:
            yPlot = [0] * len(instances)
        #Uses the values of the second feature in the case of a two dimensional tree
        else:
            yPlot = instances.iloc[:, 1]
        
        #Creates the scatter graph object
        scatter = go.Scatter(x = xPlot, 
                            y = yPlot, 
                            mode = 'markers',
                            hoverinfo = 'text',
                            hovertext = classifications,
                            marker = dict(size = 8,
                                        colorscale = markerColourscale,
                                        color = classificationsNum,
                                        symbol = classificationShapes,
                                        line = dict(color = 'black', 
                                        width = 1))
                            )
        
        return scatter

    """
    AUTHOR: Daniel Ferring
    DATE CREATED: 24/02/2023
    PREVIOUS MAINTAINER: Daniel Ferring
    DATE LAST MODIFIED: 21/03/2023

    Combines the heatmap and the scatter plot into a single
    graph object to represent the decision boundaries of a
    given model

    INPUTS:
    model: The decision tree model to be represented
    modelInfo: contains all the information relating to the model 
               to be represented (Defined in SettingCallbacks.py)
    """
    def generateDecisionBoundary(self, modelInfo):
        model = modelInfo["modelData"]
        colourKey = modelInfo["colourKey"]
        shapeKey = modelInfo["shapeKey"]

        #Stores the created graph object for use in the wider system
        decisionBoundary = []

        #Creates heatmap and scatter plot objects
        heatmapValues = self.getHeatmapValues(modelInfo["trainingData"], modelInfo['testingData'])
        heatmap = self.plotHeatmap(model, heatmapValues, colourKey)
        scatter = self.plotScatterGraph(modelInfo["trainingData"], modelInfo["testingData"], colourKey, shapeKey)

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
