from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
from utils.DecisionBoundaryUtil import DecisionBoundaryUtil
from utils.ToolTipUtil import ToolTip
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import dcc

"""
AUTHOR: Daniel Ferring
DATE CREATED: 19/02/2023
PREVIOUS MAINTAINER: Daniel Ferring
DATE LAST MODIFIED: 23/03/2023

Child of 'ClassifierComponent', this class defines an
appropriate 'componentLayout' to represent decision boundaries
in 1D or 2D depending on the number of features used to train the
model.

Inputs:
modelInfo : contains all the information relating to the model 
            to be represented (Defined in SettingCallbacks.py)
"""
class ClassifierDecisionBoundaryComponent(ClassifierComponent):

    def __init__(self, modelInfo, sessionID):
        
        title = 'Decision Boundary'
        description = 'This visualisation represents the decisions made by the tree. '\
        'The axes are the features used to train the model and the data instances are plotted within the feature space as markers. '\
        'The colours of the instances represent their true class (taken from the data set). The colour of the section that they are plotted in '\
        'represents the class that the model would predict them to be. It should be noted that the colour of the markers is slightly darker than '\
        'that of their predicted class, this is done to make them more distinguishable from the background.'
        
        BoundaryUtil = DecisionBoundaryUtil()
        features = modelInfo["modelData"].feature_names_in_

        #If the model contains more than two features, the system will display the pairwise plot visualisation
        if(len(features) > 2):
            self.boundary = html.Div(id = "pairwise-plot",
                            children = [
                                html.Div(children = [
                                    html.H3("Select Features to display"),
                                    dbc.Checklist(
                                        id = "pairwise-features",
                                        options = features,
                                        value = [],
                                        style = {"text-align":"left", "margin-left":"20%", "padding-bottom":"5%"}
                                    ),
                                    html.Button("Plot", id = "pairwise-button", n_clicks=0, className = "trainButton")],
                                    style = {"width":"20%", "padding-top":"2%"}),
                                html.Div(id = "pairwise-boundary", style = {'width':'75%'},),
                                dcc.ConfirmDialog(id = "feature-error", message = "")],
                                style = {"display":"flex", "flex-direction":"row", "column-gap":"2%"}
                            )
        #For one or two features, the system displays the standard decision boundary visualisation
        else:
            self.boundary = [
                html.Div(id = "decision-boundary", children = BoundaryUtil.generateDecisionBoundary(modelInfo)),
                ToolTip().generateToolTip("decision-boundary", title, description)           
            ]

        self.componentTitle = "Decision Boundary Visualisation"
        
        self.componentChildren = html.Div(id = {"type" : "decision-boundary-component", "index" : 1}, children=self.boundary)