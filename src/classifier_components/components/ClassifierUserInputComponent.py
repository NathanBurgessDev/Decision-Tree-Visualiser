from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
import dash_bootstrap_components as dbc
from sklearn.metrics import accuracy_score
from utils.ToolTipUtil import ToolTip

"""
AUTHOR: Dominic Cripps
DATE CREATED: 22/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 23/02/2023

Child of 'ClassifierComponent', this class defines an
appropriate 'componentLayout' to represent user input.
The user will be able to input feature values and a
classification will be returned, alongside the models accuracy.

Inputs:
modelInfo : contains all the information relating to the model 
            to be represented (Defined in SettingCallbacks.py)
"""
class ClassifierUserInputComponent(ClassifierComponent):

    def __init__(self, modelInfo):

        testingData = modelInfo["testingData"]
        
        predY = modelInfo["modelData"].predict(testingData[0])
        trueY = testingData[1]
        accuracy = str(round(accuracy_score(trueY, predY) * 100, 3)) + "%"

        layout = [
                html.Div(children = "Model Accuracy", className="textSubTitleCenter"),
                html.Div(id = "accuracy", children = accuracy, style={"text-align" : "center", "margin-top" : "10px", "font-weight" : "bold"}),

                html.Div(children = "Prediction", className="textSubTitleCenter"),
                html.Div(id = "prediction", children = "Input Features To Start", style={"text-align" : "center", "margin-top" : "10px", "font-weight" : "bold"}),

                html.Div(children="Features", className="textSubTitleCenter"),

        ]
     
        featuresLayout = []
        for x in modelInfo["modelData"].feature_names_in_ : 
            featuresLayout += [
                html.Div(children = x, className = "featureTitle"),

                dbc.Input(
                    id=dict(name="prediction-features", idx=x), 
                    className = "featureInput",
                    placeholder = "Enter Feature Data",
                ),

                html.Br(),
        ]

        features = html.Div(children = featuresLayout, className = "featureList"),

        layout += features

        layout += [
            html.Br(),
            html.Button("Predict", id="predict-button", n_clicks = 0, className = "trainButton"),
            html.Br(),
            ToolTip().generateToolTip("user-input-component", "User Input", "The model will classify each sample of the testing data and compare the results to each samples true value, this is displayed under 'Accuracy'. The user can input their own custom data (all training features must have a value) the model then classifies this and the result is shown. The custom point is plotted on the decision boundary and the path taken to that classification is highlighted on the Decision Tree."),
        ]

        self.componentTitle = "Predict User Input"
        self.componentChildren = html.Div(id = "user-input-component", children=layout, style={"height" : "100%"})