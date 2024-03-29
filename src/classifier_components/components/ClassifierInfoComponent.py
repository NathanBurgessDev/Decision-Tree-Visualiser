from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
from utils.ToolTipUtil import ToolTip

"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 19/02/2023

Child of 'ClassifierComponent' this class defines 
an appropriate 'componentLayout' based on the model
selected.

"""
class ClassifierInfoComponent(ClassifierComponent):
    
    def __init__(self, modelInfo):
        
        generalInfoChildren = [
                html.Div(children = "General Info", className="textSubTitle"),
                
                html.Br(),

                html.Div(children=" Model Name", style={"font-weight" : "bold"}),
                html.Div(modelInfo["modelName"]),

                html.Br(),

                html.Div(children=" Model Class", style={"font-weight" : "bold"}),
                html.Div(modelInfo["classifierType"]),

                html.Br(),
        ]

        if(hasattr(modelInfo["modelData"], "feature_names_in_")):
            features = []
            for feature in modelInfo["modelData"].feature_names_in_:
                features.append(str(feature))
                features.append(html.Br())
            generalInfoChildren += [
                    html.Div(children=" Features", style={"font-weight" : "bold"}),
                    html.Div(features),
                    html.Br(),
            ]

        if(hasattr(modelInfo["modelData"], "classes_")):
            classes = []
            for classification in modelInfo["modelData"].classes_:
                classes.append(str(classification))
                classes.append(html.Br())
            generalInfoChildren += [
                    html.Div(children=" Classes", style={"font-weight" : "bold"}),
                    html.Div(classes),
                    html.Br(),
                ]

        generalInfoChildren += [
                    html.Div(children=" Test / Train", style={"font-weight" : "bold"}),
                    html.Div(modelInfo["testTrainSplit"]),
                ]

        parameters = []
        for param in modelInfo["modelArguments"]:
            parameters.append(html.Div(children=[param + ":"], style={"font-weight" : "bold"}))
            parameters.append(html.Div(str(modelInfo["modelArguments"][param])))
            parameters.append(html.Br())

        # It seperates the model information into two columns, one for general info,
        # containing things like the classification type, and the other for the 
        # parameters used to train the model.
        generalInfo = html.Div(children = generalInfoChildren, className="classifierInfoComponent")


        parameterInfo = html.Div(
            children =[
                html.Div(children = "Parameter Info", className="textSubTitle"),
                
                html.Br(),

                html.Div(parameters),
            ]
        ,className="classifierInfoComponent")


        modelInfo = html.Div( id = "model-information-component",
            children = [
            generalInfo, 
            parameterInfo,
            ToolTip().generateToolTip("model-information-component", "Model Information", "Displays information about the trained model. Useful when comparing and identifying how models have been trained."),
        ], className="classifierInfoContainer")


        self.componentTitle = "Model Information"

        # Set component layout property to be a div containing modelData
        # Important : className of this div must be "classifierComponent" to format correctly
        self.componentChildren = modelInfo
                                        
