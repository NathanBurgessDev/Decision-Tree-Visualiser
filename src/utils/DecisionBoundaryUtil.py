from sklearn.tree import _tree
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import math

class DecisionBoundaryUtil():

    def getModelData(self, model, featureDivisions):
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

        modelData = []

        for j in range (0, len(featureDivisions)):
            tempModelData = []

            divisions = (largestThreshold[j] - smallestThreshold[j]) / steps[j]
            for i in range (0, int(divisions)):
                tempModelData.append(smallestThreshold[j] + (i * steps[j]))
            modelData.append(tempModelData)

        return modelData


    def decisionBoundaries1D(self, model, featureID):

        modelData = self.getModelData(model, [featureID])
 
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
                        showscale=False)

        # Make our graph object
        graph = go.Figure(data=trace)


        # Set the titles of the X and Y Axis
        graph.update_layout(
            xaxis_title=str(model.feature_names_in_[featureID]), 
            title = "Decision Boundary Visualisation For Model Trained With Feature(s) - " 
            + str(model.feature_names_in_[featureID]))

        graph.update_yaxes(visible=False, showticklabels=False)

        return graph



    def decisionBoundaries2D(self, model, divisions):
        modelData = self.getModelData(model, divisions)
        
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
                        showscale=False)

        # Make our graph object
        graph = go.Figure(data=trace)

        # Set the titles of the X and Y Axis
        graph.update_layout(
            xaxis_title=str(model.feature_names_in_[0]), 
            title = "Decision Boundary Visualisation For Model Trained With Feature(s) - " 
            + str(model.feature_names_in_[0] + ", " + str(model.feature_names_in_[1])),
            yaxis_title=str(model.feature_names_in_[1]))

        return graph

    def disolveDecisionTree(self, model, targetFeatureNames):
        tree = model.tree_

        featuresToDissolve = []
        for x in model.feature_names_in_:
            if x not in targetFeatureNames:
                featuresToDissolve.append(x)

        print(featuresToDissolve)