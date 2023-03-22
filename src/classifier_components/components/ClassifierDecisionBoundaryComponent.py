from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
from utils.DecisionBoundaryUtil import DecisionBoundaryUtil
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc



"""
AUTHOR: Daniel Ferring
DATE CREATED: 19/02/2023
PREVIOUS MAINTAINER: Daniel Ferring
DATE LAST MODIFIED: 19/03/2023

Child of 'ClassifierComponent', this class defines an
appropriate 'componentLayout' to represent decision boundaries
in 1D or 2D depending on the number of features used to train the
model.

Inputs:
modelInfo : contains all the information relating to the model 
            to be represented (Defined in SettingCallbacks.py)
"""
class ClassifierDecisionBoundaryComponent(ClassifierComponent):

    def __init__(self, modelInfo):
        
        BoundaryUtil = DecisionBoundaryUtil()
        features = modelInfo["modelData"].feature_names_in_

        if(len(features) > 2):
            self.boundary = html.Div(id = "pairwise-plot",
                            children = [
                                html.Div(children = [
                                    html.H3("Select Features to display"),
                                    dbc.Checklist(
                                        id = "pairwise-features",
                                        options = features,
                                        value = []
                                    ),
                                    html.Button("Plot", id = "pairwise-button", n_clicks=0, className = "trainButton")],
                                    style = {'width' : '20%'}),
                                html.Div(id = "pairwise-boundary", style = {'width': '75%'})],
                                style = {"display" : "flex", "flex-direction" : "row", "column-gap" : "5%", }
                            )
        else:
            self.boundary = BoundaryUtil.generateDecisionBoundary(modelInfo)

        #Sets the values for the component to be displayed within the app
        self.componentTitle = "Decision Boundary Visualisation"
        
        self.componentChildren = html.Div(id = "decision-boundary-component", children=self.boundary)