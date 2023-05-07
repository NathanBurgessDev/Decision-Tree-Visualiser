from dash.dependencies import Input, Output, State, ALL
from dash import ctx
from UserSession import UserSession
from utils.DecisionBoundaryUtil import DecisionBoundaryUtil
import dash
import copy
from AppInstance import AppInstance
from flask import request
app = AppInstance().instance.app


BoundaryUtil = DecisionBoundaryUtil()

"""
AUTHOR: Daniel Ferring
DATE CREATED: 22/03/2023
PREVIOUS MAINTAINER: Daniel Ferring
DATE LAST MODIFIED: 23/03/2023

Callback is triggered when the user presses the "pairwise-button"

If the number of features selected is vald, the callback trains a new model and
plots a decision boundary, returning the boundary object.

If the number of seleced features is invalid (>2 || <1), an error message is
displayed, informing the user why their input is invalid 
"""

@app.callback(
    [Output(component_id = "pairwise-boundary", component_property = "children"),
        Output(component_id = "feature-error", component_property = "displayed"),
        Output(component_id = "feature-error", component_property = "message")],
    [Input("pairwise-button", "n_clicks"),
        State("trained-models", "value"),
        State("pairwise-features", "value")]
)
def pairwisePlot(clicks, modelName, features):
    error = False
    errorMessage = ""

    if "pairwise-button" == ctx.triggered_id:

        #Checks if selected features are invalid, displays errror message if they are
        if len(features) == 0:
            error = True
            errorMessage = "Error: Please select at least one feature"
            return dash.no_update, error, errorMessage
        if len(features) > 2:
            error = True
            errorMessage = "Error: You cannot select more than two features"
            return dash.no_update, error, errorMessage

        #Creates a copy of modelInfo so that it can be modified without impacting the orginal
        modelInfo = copy.deepcopy(UserSession().instance.modelInformation[str(request.remote_addr)][modelName])
        trainingData = modelInfo['trainingData'][0]
        testingData = modelInfo['testingData'][0]
        
        #Removes unused features from training and testing data
        for x in trainingData.columns:
            if x not in features:
                trainingData = trainingData.drop(x, axis = 1)
        for x in testingData.columns:
            if x not in features:
                testingData = testingData.drop(x, axis = 1)

        #Trains model usin the selected features
        model = modelInfo['selectedSettings'].classifier(**modelInfo['modelArguments']).fit(trainingData, modelInfo['trainingData'][1])

        #Updates the copy of modelInfo to reflect changes
        modelInfo['trainingData'][0] = trainingData
        modelInfo['testingData'][0] = testingData
        modelInfo['modelData'] = model

        #Plots a decision boundary using the modified modelInfo object
        return BoundaryUtil.generateDecisionBoundary(modelInfo), error, errorMessage

    return dash.no_update, error, errorMessage


