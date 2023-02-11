import base64
import io
from io import StringIO
import pandas as pd
import plotly.express as px
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import plotly.graph_objs as go
import igraph as ig
from igraph import Graph, EdgeSeq
import pickle


"""
AUTHOR: Ethan Temple-Betts
DATE CREATED: UNKNOWN
PREVIOUS MAINTAINER: Ethan Temple-Betts
DATE LAST MODIFIED: UNKNOWN

Used to store common functions that relate to the handling of
user inputted files, such as .csv and .sav files.
"""
class ImportUtil:

    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Converts the the given file contents into a string of data

    INPUTS
    str file : The full filename

    base64 content The contents of that file in base64
    '''
    def readContent(file, content):
        content_type, content_string = content.split(',')
        contentBytes = base64.b64decode(content_string)
        stringContent = contentBytes.decode('utf-8')
        return stringContent

    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Converts a string of csv data into a dataframe object

    INPUTS
    str csv : The contents of a scv file as a string
    '''
    def csvToDataFrame(csv):
        data = StringIO(csv)
        df = pd.read_csv(data, sep=",")
        return df

    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Converts base64 data into a binary stream/BytesIO object

    INPUTS
    str file : The full filename

    base64 content The contents of that file in base64
    '''
    def readPickle(file, content):
        content_type, content_string = content.split(',')
        contentBytes = base64.b64decode(content_string)
        return io.BytesIO(contentBytes)

    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Reconstructs a pickled object that has been converted to a
    BytesIO object into the MLM that was orginally pickled

    INPUTS
    BytesIO file : A pickled file converted to a BytesIO object
    '''
    def unPickle(file):
        return pickle.loads(file.read())

"""
AUTHOR: Ethan Temple-Betts
DATE CREATED: UNKNOWN
PREVIOUS MAINTAINER: Ethan Temple-Betts
DATE LAST MODIFIED: UNKNOWN

Used to store common functions that relate to the creation of
plotly graphs
"""
class GraphUtil():

    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Creates a 2D plotly scatter graph of the data contained in
    df. If the colour paramater is not boolean False, then it is
    used to colour the data based on the values of df[colour].

    INPUTS
    DataFrame df: Contains the desired data to be plotted

    str x: The desired x axis feature

    str y: The desired y axis feature

    (str or bool) colour: Optionally specifies which feature to
    use to colour the data
    '''
    def scatter2D(df, x, y, colour):
        if(colour == False):
            graph = px.scatter(df, x=x, y=y)
        else:
            graph = px.scatter(df, x=x, y=y, color=colour)
        return graph

    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Creates a 3D plotly scatter graph of the data contained in
    df. If the colour paramater is not boolean False, then it is
    used to colour the data based on the values of df[colour].

    INPUTS
    DataFrame df: Contains the desired data to be plotted

    str x: The desired x axis feature

    str y: The desired y axis feature

    str z: The desired z axis feature

    (str or bool) colour: Optionally specifies which feature to
    use to colour the data
    '''
    def scatter3D(df, x, y, z, colour):
        if(colour == False):
            graph = px.scatter_3d(df, x=x, y=y, z=z)
        else:
            graph = px.scatter_3d(df, x=x, y=y, z=z, color=colour)
        graph.update_traces(marker={'size': 4})
        return graph

    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Returns an empty plotly scatter graph.
    '''
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

        # make the main scatter plot 
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


    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    When given an igraph Graph this function will return
    a plotly graph, which represents the graphs structure.
    Most of code comes from https://plotly.com/python/tree-plots/.

    INPUTS
    igraph.Graph G: The Graph object to be displayed
    int nr_vertices: The number of verticies in the graph
    '''
    def generateTreeGraph(G, nr_vertices):
        lay = G.layout('rt')
        v_label = list(map(str, range(nr_vertices)))
        position = {k: lay[k] for k in range(nr_vertices)}
        Y = [lay[k][1] for k in range(nr_vertices)]
        M = max(Y)

        es = EdgeSeq(G)
        E = [e.tuple for e in G.es]

        L = len(position)
        Xn = [position[k][0] for k in range(L)]
        Yn = [2*M-position[k][1] for k in range(L)]
        Xe = []
        Ye = []
        for edge in E:
            Xe+=[position[edge[0]][0],position[edge[1]][0], None]
            Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

        labels = v_label

        '''
        AUTHOR: Ethan Temple-Betts
        PREVIOUS MAINTAINER: Ethan Temple-Betts

        Used to assign annotations to nodes on the graph.

        INPUTS
        dict pos: 
        list[int] text:
        '''
        def make_annotations(pos, text, font_size=10, font_color='rgb(0,0,0)'):
            L=len(pos)
            if len(text)!=L:
                raise ValueError('The lists pos and text must have the same len')
            annotations = []
            for k in range(L):
                annotations.append(
                    dict(
                        # G.vs.info is assigned in the readMLM function #
                        text=G.vs["info"][k],
                        x=pos[k][0], y=2*M-position[k][1],
                        xref='x1', yref='y1',
                        font=dict(color=font_color, size=font_size),
                        showarrow=False)
                )
            return annotations

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Xe,
                        y=Ye,
                        mode='lines',
                        line=dict(color='rgb(210,210,210)', width=1),
                        hoverinfo='none'
                        ))
        fig.add_trace(go.Scatter(x=Xn,
                        y=Yn,
                        mode='markers',
                        name='bla',
                        marker=dict(symbol='circle-dot',
                                        size=18,
                                        color='#6175c1',
                                        line=dict(color='rgb(50,50,50)', width=1)
                                        ),
                        text=labels,
                        hoverinfo='text',
                        opacity=0.8
                        ))

        axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    )

        fig.update_layout(annotations=make_annotations(position, v_label),
                    font_size=12,
                    showlegend=False,
                    xaxis=axis,
                    yaxis=axis,
                    margin=dict(l=40, r=40, b=85, t=100),
                    hovermode='closest',
                    plot_bgcolor='rgb(255,255,255)'
                    )

        return fig


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

    
       
        
        

    

        


