from dash.dependencies import Input, Output, State, ALL
from dash import ctx
import dash
import plotly.express as px
from UserSession import UserSession
import pandas as pd
import numpy as np

def get_callbacks(app):

    """
    AUTHOR: Ethan Temple-Betts
    DATE CREATED: 20/03/2023
    PREVIOUS MAINTAINER: Ethan Temple-Betts
    DATE LAST MODIFIED: 20/03/2023

    Callback is triggered when the new features are selected

    Callback output is the feature space figure.

    The function 'updateFeatureSpace' will alter the axis of the
    graph depending on the provided features

    """
    @app.callback(
        [Output(component_id="fs_plot", component_property="figure")],
        [Input("fs_xfeature_select", component_property="value"),
         Input("fs_yfeature_select", component_property = "value"),
         Input("fs_zfeature_select", component_property = "value")]
    )
    def updateFeatureSpace(xFeature, yFeature, zFeature):
        # Currenttly trained models
        keys = list((UserSession.modelInformation).keys())
        
        # if no model is selected selct the first model trained
        if UserSession.selectedModel != None:
            modelInfo = UserSession.modelInformation[UserSession.selectedModel]
        else:
            modelInfo = UserSession.modelInformation[keys[0]]

        xTest = modelInfo["testingData"][0]
        yTest = (modelInfo["testingData"][1]).to_frame()
        xTrain = modelInfo["trainingData"][0]
        yTrain = (modelInfo["trainingData"][1]).to_frame()

        xData = pd.concat([xTest, xTrain])
        yData = pd.concat([yTest, yTrain])

        # Combine all train and test data
        data = pd.concat([xData, yData], axis=1)

        # Color points based on classification
        if((yData.columns.values.tolist())[0] in data.columns.values.tolist()):
            color = yData.columns[0]
        else:
            color = data.columns[0]

        # Create 3d or 2d plot depending on provided features
        if xFeature and yFeature and zFeature:
            fig = px.scatter_3d(data_frame=data,
                                x=xFeature, y=yFeature, z=zFeature,
                                color=color)
        elif xFeature and yFeature:
            fig = px.scatter(data_frame=data, x=xFeature, y=yFeature, color=color)
        else:
            fig = px.scatter()

        fig.update_layout(
            paper_bgcolor="#232323",
            font_color = "#f5f5f5",
            plot_bgcolor="#232323")

        return [fig]
