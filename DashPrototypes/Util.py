import base64
import io
from io import StringIO
import pandas as pd
import plotly.express as px
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import plotly.graph_objs as go

"""
Contains functions that relate to the processsing of
data imports
"""
class ImportUtil:

    ### Converts base64 data to a string ###
    def readContent(file, content):
        content_type, content_string = content.split(',')
        contentBytes = base64.b64decode(content_string)
        stringContent = contentBytes.decode('utf-8')
        return stringContent

    ### Converts a string of csv data to a dataframe ###
    def csvToDataFrame(csv):
        data = StringIO(csv)
        df = pd.read_csv(data, sep=",")
        return df

"""
Contains functions that relate to the creation
of plotly scatter graphs
"""
class GraphUtil():

    ### Returns a 2d plotly scatter graph using the provided params ###
    def scatter2D(df, x, y, colour):
        if(colour == False):
            graph = px.scatter(df, x=x, y=y)
        else:
            graph = px.scatter(df, x=x, y=y, color=colour)
        return graph

    ### Returns a 3d plotly scatter graph using the provided params ###
    def scatter3D(df, x, y, z, colour):
        if(colour == False):
            graph = px.scatter_3d(df, x=x, y=y, z=z)
        else:
            graph = px.scatter_3d(df, x=x, y=y, z=z, color=colour)
        graph.update_traces(marker={'size': 4})
        return graph

    ### Returns a blank plottly scatter graph ###
    def getGraph():
        return px.scatter()

    ### Returns a 2d scatter graph with a heatmap to represent
    ### the decision boundary
    ### Credit for a lot of the decision boundary work goes to: Anisotropic
    ### https://www.kaggle.com/code/arthurtok/decision-boundaries-visualised-via-python-plotly
    def getDecisionBoundary2D(df,startX,startY,classFeature):



        # create a target map and a numerical dataframe using the ModelUtil class
        targetMap = ModelUtil.getTargetMap(df,classFeature)
        newDf = ModelUtil.getNumericalDataFrame(df,targetMap,classFeature)
        # get the training set using the ModelUtil class
        trainingSet = ModelUtil.getTrainingSet(newDf,startX,startY)
        classificationSet = newDf[classFeature]
        h=0.2
        # train a decision tree classifier on the training set
        model = DecisionTreeClassifier()
        model.fit(trainingSet,classificationSet)

        # Get the min and max of the dataset to set boundaries for how big out meshgrid
        # needs to be
        x_min, x_max = trainingSet.iloc[:, 0].min() - 1,trainingSet.iloc[:, 0].max() + 1
        y_min, y_max = trainingSet.iloc[:, 1].min() - 1, trainingSet.iloc[:, 1].max() + 1

        # Make a meshgrid with the min and max x and y values
        # Arange is used to create an array of values from min to max with a step of h
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h)
                     , np.arange(y_min, y_max, h))
        y_ = np.arange(y_min, y_max, h)

        #Z is an array of predictions made on the heatmap
        # np.c_ concatenates 2 1D arrays into 1 2D array
        #i.e. x[1,2,3], y[4,5,6] = z[[1,4],[2,5],[3,6]]
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        # Make a Heatmap using the array of values we previously created
        trace1 = go.Heatmap(x=xx[0], y=y_, z=Z,
                  colorscale='sunset',
                  showscale=False)

        # Make our graph object
        graph = go.Figure(data=trace1)

        # make the main  scatter plot 
        trace2 = go.Scatter(x=trainingSet.iloc[:, 0], y=trainingSet.iloc[:, 1], 
                            mode='markers',
                            showlegend=False,
                            marker=dict(size=10,
                                        color=classificationSet, 
                                        colorscale='sunsetdark',
                                        line=dict(color='black', width=1))
                            )

        # Place the main scatter plot over the previously created heatmap
        graph.add_trace(trace2)

        # Set the titles of the X and Y Axis
        graph.update_layout(
            xaxis_title=trainingSet.columns[0],
            yaxis_title=trainingSet.columns[1])

        return graph


"""
Contains functions that relate to the creation of decision trees
(i.e. retraining a model) 
"""
class ModelUtil():
    # getTargetMap returns a dictionary that maps the unique values in a classification
    # column to numerical values
    def getTargetMap(df,classificationCol):
        # get the unique values in the classification column
        uniqueValues = df[classificationCol].unique()
        numArray = []
        n = 0
        # map each unique value to a numerical value
        for x in uniqueValues:
            numArray.append(n)
            n+=1
        
        # create a dictionary that maps the unique values to numerical values
        targetMap = dict(zip(uniqueValues,numArray))

        return targetMap
    # getTrainingSet returns a new dataframe containing only the specified columns
    def getTrainingSet(df,x,y):
        return df[[x,y]].copy()
    # getNumericalDataFrame applies a target map to the class feature in a dataframe
    # and returns the resulting dataframe
    def getNumericalDataFrame(df,targetMap,classFeature):
       # make a copy of the dataframe
        newDf = df.copy()
        # apply the target map to the class feature
        newDf[classFeature] = newDf[classFeature].apply(lambda x: targetMap[x])
        return newDf

    
       
        
        

    

        


