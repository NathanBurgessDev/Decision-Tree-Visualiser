from sklearn.tree import _tree
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import math
from dash import dcc

class DecisionBoundaryUtil():

    def getModelData(self, model, featureDivisions, trainingData):
        smallestThreshold = [None, None]
        largestThreshold = [None, None]
        buffers = [None, None]
        steps = [None, None]
        
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

        heatmapMins = []
        heatmapMaxs = []

        instances = trainingData[0]
        for i in instances:
            min = instances[i].min()
            max = instances[i].max()
            buffer = (max - min) / 10
            heatmapMins.append(min - buffer)
            heatmapMaxs.append(max + buffer)

        modelData = []

        for j in range (0, len(featureDivisions)):
            tempModelData = []

            divisions = (heatmapMaxs[j] - heatmapMins[j]) / steps[j]
            for i in range (0, int(divisions)):
                tempModelData.append(heatmapMins[j] + (i * steps[j]))
            modelData.append(tempModelData)

        return modelData


    def decisionBoundaries1D(self, model, featureID, trainingData):

        decisionBoundary = []

        modelData = self.getModelData(model, [featureID], trainingData)
 
        dataframe = pd.DataFrame(data = modelData[featureID], columns = [str(model.feature_names_in_[featureID])])

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

        instances = trainingData[0]

        trace2 = go.Scatter(x=instances.iloc[:, 0], y = [0] * len(modelData[featureID]), 
                            mode='markers',
                            showlegend=False,
                            marker=dict(size=10,
                                        colorscale='sunsetdark',
                                        line=dict(color='black', width=1)),
                           )
 
        # Make our graph object
        


        graph = go.Figure(data=trace)
        graph.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color = "#f5f5f5",
            autosize=True, 
            margin={'t': 50,'l':10,'b':5,'r':30}, 
        )   
        graph.add_trace(trace2)

        # Set the titles of the X and Y Axis
        graph.update_layout(
            xaxis_title=str(model.feature_names_in_[featureID]), 
        )
        
        graph.update_yaxes(visible=False, showticklabels=False)

        decisionBoundary.append(dcc.Graph(figure = graph))

        return decisionBoundary



    def decisionBoundaries2D(self, model, divisions, trainingData):

        decisionBoundary = []

        modelData = self.getModelData(model, divisions, trainingData)
        
        data = []

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

        trace = go.Heatmap(z=classifications, 
                        x = modelData[0], 
                        y = modelData[1], 
                        text = modelText, 
                        colorscale='sunset',
                        hoverinfo='text',
                        colorbar=dict(bgcolor = "#232323"),
                        showscale=False)

        instances = trainingData[0]

        trace2 = go.Scatter(x=instances.iloc[:, 0], y=instances.iloc[:, 1], 
                            mode='markers',
                            showlegend=False,
                            marker=dict(size=10,
                                        colorscale='sunsetdark',
                                        line=dict(color='black', width=1))
                           )

        # Make our graph object
        graph = go.Figure(data = trace)
        graph.update_layout(
            paper_bgcolor="#232323",
            plot_bgcolor="#232323",
            font_color="#f5f5f5",
            autosize=True, 
            margin={'t': 50,'l':10,'b':5,'r':30}, 
        ) 

        graph.add_trace(trace2)

        # Set the titles of the X and Y Axis
        graph.update_layout(
            xaxis_title=str(model.feature_names_in_[0]),
            yaxis_title=str(model.feature_names_in_[1]))
        
        decisionBoundary.append(dcc.Graph(figure = graph))

        return decisionBoundary