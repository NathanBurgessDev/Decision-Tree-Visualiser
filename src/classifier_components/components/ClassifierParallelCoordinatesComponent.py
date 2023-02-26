from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
import plotly.express as px
import pandas as pd
from dash import dcc
import numpy as np

"""
AUTHOR: Ethan Temple-Betts
DATE CREATED: 22/02/2023
PREVIOUS MAINTAINER: Ethan Temple-Betts
DATE LAST MODIFIED: 23/02/2023

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

        # Generate an array to contain all unique
        # classifications
        classes = (np.unique(pred[classifier])).tolist()

        # This dictionary will store the mappings from class
        # names to ints
        mapping = {}
        count = 0

        # Val is an array of ints [0..n] where n is the 
        # number of unique classes
        val = list(range(len(classes)))

        # Populate the dictionay with mappings from classes to
        # ints
        for c in classes:
            mapping[c] = val[count]
            count+=1

        # Convert the class names to ints in the
        # both dataframe. This allows the plot to work with
        # classification data when the classes are strings
        pred[classifier] = pred[classifier].map(mapping)
        yTestDF[classifier] = yTestDF[classifier].map(mapping)

        # Add a column to the xTest dataframe which contains
        # the true classifications of the data.
        # .values is needed here to prevent indexing issues
        # between the 2 dataframes
        xTest["True Class"] = yTestDF[classifier].values

        # dims contains all the dimensions used for the plot
        # i.e all the columns in xTest including
        # the true classifications
        dims = xTest.columns

        # Add the predicted classes as a column in xTest.
        # (This won't show in the plot as a dimension but is used
        # to colour the lines). .values is again important to
        # prevent indexing issues
        xTest[classifier] = pred[classifier].values


        # Create the plot using the xTest dataframe, and colour
        # based on predicted class
        fig = px.parallel_coordinates(xTest, color=classifier,
                                    dimensions=dims,
                                    color_continuous_scale=px.colors.diverging.Spectral,
                                    color_continuous_midpoint=2)

        # Customise the colours of the plot
        fig.update_layout(paper_bgcolor="#232323", font_color = "#f5f5f5", plot_bgcolor="#232323")
        self.componentTitle = "Parallel Coordinates"

        # Update the componentChildren property to be a html div
        # containing the parallel coordinates plot
        self.componentChildren = html.Div(dcc.Graph(figure = fig))


    