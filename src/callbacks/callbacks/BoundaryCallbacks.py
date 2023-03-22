from dash.dependencies import Input, Output, State, ALL
from dash import ctx
from UserSession import UserSession
from utils.DecisionBoundaryUtil import DecisionBoundaryUtil
import pandas as pd
import copy

BoundaryUtil = DecisionBoundaryUtil()

def get_callbacks(app):

    @app.callback(
        Output(component_id = "pairwise-boundary", component_property = "children"),
        [Input("pairwise-button", "n_clicks"),
         State("trained-models", "value"),
         State("pairwise-features", "value")]
    )
    def test(clicks, name, features):
        if "pairwise-button" == ctx.triggered_id:
            print("Pressed")
            modelInfo = copy.deepcopy(UserSession().instance.modelInformation[name])
            trainingData = modelInfo['trainingData'][0]
            testingData = modelInfo['testingData'][0]
            
            for x in trainingData.columns:
                if x not in features:
                    trainingData = trainingData.drop(x, axis = 1)
            
            for x in testingData.columns:
                if x not in features:
                    testingData = testingData.drop(x, axis = 1)

            model = modelInfo['selectedSettings'].classifier(**modelInfo['modelArguments']).fit(trainingData, modelInfo['trainingData'][1])

            modelInfo['trainingData'][0] = trainingData
            modelInfo['testingData'][0] = testingData
            modelInfo['modelData'] = model

            return BoundaryUtil.generateDecisionBoundary(modelInfo)


