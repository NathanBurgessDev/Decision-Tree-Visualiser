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
    def getDecisionBoundary2D(df,startX,startY,classFeature):




        targetMap = ModelUtil.getTargetMap(df,classFeature)
        newDf = ModelUtil.getNumericalDataFrame(df,targetMap,classFeature)

        trainingSet = ModelUtil.getTrainingSet(newDf,startX,startY)
        classificationSet = newDf[classFeature]
        h=0.2

        model = DecisionTreeClassifier()
        model.fit(trainingSet,classificationSet)

        x_min, x_max = trainingSet.iloc[:, 0].min() - 1,trainingSet.iloc[:, 0].max() + 1
        y_min, y_max = trainingSet.iloc[:, 1].min() - 1, trainingSet.iloc[:, 1].max() + 1

        xx, yy = np.meshgrid(np.arange(x_min, x_max, h)
                     , np.arange(y_min, y_max, h))
        y_ = np.arange(y_min, y_max, h)

        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        trace1 = go.Heatmap(x=xx[0], y=y_, z=Z,
                  colorscale='Viridis',
                  showscale=False)

        graph = go.Figure(data=trace1)

        trace2 = go.Scatter(x=trainingSet.iloc[:, 0], y=trainingSet.iloc[:, 1], 
                            mode='markers',
                            showlegend=False,
                            marker=dict(size=10,
                                        color=classificationSet, 
                                        colorscale='Viridis',
                                        line=dict(color='black', width=1))
                            )

        graph.add_trace(trace2)
        graph.update_layout(
            xaxis_title=trainingSet.columns[0],
            yaxis_title=trainingSet.columns[1])

        return graph


"""
Contains functions that relate to the creation of decision trees
(i.e. retraining a model) 
"""
class ModelUtil():
    def getTargetMap(df,classificationCol):

        uniqueValues = df[classificationCol].unique()
        numArray = []
        n = 0
        for x in uniqueValues:
            numArray.append(n)
            n+=1
        

        targetMap = dict(zip(uniqueValues,numArray))

        return targetMap
    
    def getTrainingSet(df,x,y):
        return df[[x,y]].copy()
    
    def getNumericalDataFrame(df,targetMap,classFeature):
        # doesnt like doing this for some reason
        newDf = df.copy()
        newDf[classFeature] = newDf[classFeature].apply(lambda x: targetMap[x])
        return newDf

    
       
        
        

    

        


