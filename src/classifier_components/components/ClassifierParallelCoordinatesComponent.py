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
using the TESTING data for the model. The colour of the lines
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
        # Extract x and y test data from modelinfo
        xTest = modelInfo["testingData"][0]
        yTest = modelInfo["testingData"][1]

        # Extract the MLM
        model = modelInfo['modelData']

        # Use the model to make class predictions for the
        # testing dataset
        predictions = model.predict(xTest)

        # Convert the yTest data to a dataframe
        # which will contain the correct classifications
        yTestDF = yTest.to_frame()

        # The classifier variable is the feature name
        # that the user selected as the classifier
        classifier = yTestDF.columns[0]

        # Create a dataframe to hold the class predictions
        pred = pd.DataFrame() 
        pred[classifier] = predictions

        # Add a column to the xTest dataframe which contains
        # the true classifications of the data.
        # .values is needed here to prevent indexing issues
        # between the 2 dataframes
        xTest["True Class"] = yTestDF[classifier].values

        # Create an array containing the all unique classes
        classes = (np.unique(pred[classifier])).tolist()

        # The mapping dictionary will contain mappings
        # from class -> int so that the classification
        # can be used to colour the lines
        mapping = {}
        count = 0
        val = list(range(len(classes)))
        for c in classes:
            mapping[c] = val[count]
            count+=1
        
        pred[classifier] = pred[classifier].map(mapping)

        # Add the predicted classes as a column in xTest.
        # (This won't show in the plot as a dimension but is used
        # to colour the lines). .values is again important to
        # prevent indexing issues
        xTest[classifier] = pred[classifier].values

        # Map the true classfication -> int and store these
        # values in a 'dummy' column
        dfg = pd.DataFrame({"True Class":xTest["True Class"].unique()})
        dfg['dummy'] = dfg.index
        xTest = pd.merge(xTest, dfg, on = "True Class", how='left')

        # An aray to store the dimensions (features)
        # used for the plot
        dimensions = []
        features = xTest.columns.values.tolist()

        # True Class could still contain str values
        # so needs to be removed
        features.remove("True Class")

        # We don't want the dummy values to be plotted
        # yet so they are removed
        features.remove('dummy')

        # This feature is used to assign colour
        # and should not be a dimension so it is removed
        features.remove(classifier)

        # Iterate through the remaining features and create
        # dimensions for each of them
        for i in features:
            dim = dict(range=[xTest[i].min(),xTest[i].max()],
                    label=i,
                    values=xTest[i],
                    visible=False)
            
            dimensions.append(dim)

        # Create the 'True Class' dimension and use the
        # dummy values to plot data but the class label
        # as the axis annotations
        dim = dict(range=[0, xTest['dummy'].max()],
                tickvals = dfg['dummy'], ticktext = dfg["True Class"],
                label="True Class", values=xTest['dummy'])
        dimensions.append(dim)

        # Create the plot and use the predicted class to colour
        # the lines
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
        # containing a seperate div for dimension control;
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


    