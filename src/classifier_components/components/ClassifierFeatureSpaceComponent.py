from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
import plotly.express as px
import pandas as pd
from dash import dcc
import numpy as np
import plotly.graph_objects as go

"""
AUTHOR: Ethan Temple-Betts
DATE CREATED: 20/03/2023
PREVIOUS MAINTAINER: Ethan Temple-Betts
DATE LAST MODIFIED: 20/03/2023

This class will create the feature space plot and provide
drobdown boxes for the user to select upto 3 features to display

Inputs
dict modelInfo :    {"modelData" : model, 
                    "trainingData" : [xTrain, yTrain],
                    "testingData" : [xTest, yTest],
                    "modelArguments" : arguments, 
                    "testTrainSplit" : split, 
                    "classifierType" : classType,
                    "modelName" : str(filename)}

"""
class ClassifierFeatureSpaceComponent(ClassifierComponent):

    def __init__(self, modelInfo):
        # Extract the testing data used to calculate what
        # features can be selected
        xTest = modelInfo["testingData"][0]

        self.componentTitle = "Feature Space"

        fig = px.scatter()

        # Customise the colours of the plot
        fig.update_layout(
            paper_bgcolor="#232323",
            font_color = "#f5f5f5",
            plot_bgcolor="#232323")
        
        # Update the componentChildren property
        self.componentChildren = html.Div(children = [
            html.Div(children = [ 
                     dcc.Dropdown(
                        options=xTest.columns,
                        id='fs_xfeature_select',
                        className = "fsFeatDropdown"),
                     dcc.Dropdown(
                        options=xTest.columns,
                        id='fs_yfeature_select',
                        className = "fsFeatDropdown"),
                     dcc.Dropdown(
                        options=xTest.columns,
                        id='fs_zfeature_select',
                        className = "fsFeatDropdown")],
                    className = "fsControlContainer"),

            dcc.Graph(figure = fig, id = "fs_plot")])




    