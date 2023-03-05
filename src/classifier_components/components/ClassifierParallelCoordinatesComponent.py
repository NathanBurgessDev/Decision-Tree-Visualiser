from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
import plotly.express as px
import pandas as pd
from dash import dcc
import numpy as np
import plotly.graph_objects as go

"""
AUTHOR: Ethan Temple-Betts
DATE CREATED: 22/02/2023
PREVIOUS MAINTAINER: Ethan Temple-Betts
DATE LAST MODIFIED: 04/03/2023

This class will create a parallel coordinates plot
using the testing data for the model. The colour of the lines
represents the predeicted classification.

Inputs
dict modelInfo :    {"modelData" : model, 
                    "trainingData" : [xTrain, yTrain],
                    "testingData" : [xTest, yTest],
                    "modelArguments" : arguments, 
                    "testTrainSplit" : split, 
                    "classifierType" : classType,
                    "modelName" : str(filename)}

"""
class ClassifierParallelCoordinatesComponent(ClassifierComponent):

    def __init__(self, modelInfo):

        # Extract xTest data, yTest data and the model
        xTest = modelInfo["testingData"][0]
        yTest = modelInfo["testingData"][1]
        model = modelInfo['modelData']

        # Predict the classes of xTest data and store result in
        # pred dataframe
        predictions = model.predict(xTest)
        yTestDF = yTest.to_frame()
        classifier = yTestDF.columns[0]
        pred = pd.DataFrame() 
        pred[classifier] = predictions

        # Add the true class and predicted class data
        # to the xTest data frame
        xTest["True Class"] = yTestDF[classifier].values
        classes = (np.unique(pred[classifier])).tolist()
        mapping = self.createClassMap(classes)
        pred[classifier] = pred[classifier].map(mapping)
        xTest[classifier] = pred[classifier].values

        # Map the true classes -> ints and store these
        # values in a 'dummy' column in xTest
        dfg = pd.DataFrame({"True Class":xTest["True Class"].unique()})
        dfg['dummy'] = dfg.index
        xTest = pd.merge(xTest, dfg, on = "True Class", how='left')

        # Create an array of feature names and remove
        # the true class, dummy and predicted columns
        features = xTest.columns.values.tolist()
        features.remove("True Class")
        features.remove('dummy')
        features.remove(classifier)

        # Create dimensions for the remaining features
        dimensions = self.createPlotDimensions(features, xTest)

        # Create the 'True Class' dimension and plot data using
        # dummy values and label the axis with the true class
        dim = dict(range=[0, xTest['dummy'].max()],
                tickvals = dfg['dummy'], ticktext = dfg["True Class"],
                label="True Class", values=xTest['dummy'])
        dimensions.append(dim)

        # Create the plot and color using predicted class
        fig = go.Figure(data=go.Parcoords(
            line = dict(color = xTest[classifier],
                        colorscale = 'spectral'),
            dimensions=dimensions))
        
        # Customise the colours of the plot
        fig.update_layout(
            paper_bgcolor="#232323",
            font_color = "#f5f5f5",
            plot_bgcolor="#232323")
        
        self.componentTitle = "Parallel Coordinates"

        # Update the componentChildren property to be a html div
        # containing a seperate div for dimension controls;
        # div[('-' button), (feature dropdown), ('+' button)]
        # and below this the parallel coordinates plot
        self.componentChildren = html.Div(
            [html.Div(children=[
            html.Button(
            "-",
            id="pc_del_dim",
            className="pcButton"),

            dcc.Dropdown(
            options=features,
            value = features[0],
            id='pc_dim_select',
            className = "pcDimDropdown"),

            html.Button(
            "+",
            id="pc_add_dim",
            className="pcButton")],
            className = "pcControlContainer"),
            
            dcc.Graph(
            figure = fig,
            id="pc_plot")])
        
    
    ''' 
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Create a dictionary, which maps class names -> ints

    Inputs:
    list classes[str or int] : a list of unique class names

    Returns:
    dict mapping : A dictionary mapping class names -> int
    
    '''
    def createClassMap(self, classes):
        mapping = {}
        count = 0
        val = list(range(len(classes)))
        for c in classes:
            mapping[c] = val[count]
            count+=1

        return mapping
    

    ''' 
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Create a list, which contains valid paracoord dimensions

    Inputs:
    list[str] features : a list of feature names in data to be
    made into dimensions

    dataframe data : A dataframe containing the data to be
    plotted 

    Returns:
    list[dict] dimensions : Valid paracoord dimensions
    '''
    def createPlotDimensions(self, features, data):
        dimensions = []
        for i in features:
            dim = dict(range=[data[i].min(),data[i].max()],
                    label=i,
                    values=data[i],
                    visible=False)
            
            dimensions.append(dim)

        return dimensions



    