from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
from utils.DecisionBoundaryUtil import DecisionBoundaryUtil
import dash_bootstrap_components as dbc

"""
AUTHOR: Daniel Ferring
DATE CREATED: 19/02/2023
PREVIOUS MAINTAINER: Daniel Ferring
DATE LAST MODIFIED: 21/03/2023

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
        
        title = 'Decision Boundary'
        description = 'This visualisation represents the decisions made by the tree. '\
        'The axes are the features used to train the model and the data instances are plotted within the feature space as markers. '\
        'The colours of the instances represent their true class (taken from the data set). The colour of the section that they are plotted in '\
        'represents the class that the model would predict them to be. It should be noted that the colour of the markers is slightly darker than '\
        'that of their predicted class, this is done to make them more distinguishable from the background.'
        
        BoundaryUtil = DecisionBoundaryUtil()

        if(len(modelInfo["modelData"].feature_names_in_) > 2):
            self.boundary = html.P("Higher Dimensions are not supported for this visualisation")
        else:
            self.boundary = [html.Div(id = "decision-boundary", children = BoundaryUtil.generateDecisionBoundary(modelInfo)),
                            dbc.Tooltip(
                                children = [
                                    html.Div(children = [
                                        html.H1(title, style = {'color' : 'blue'}),
                                        html.P(description, style = {'color' : 'black'})
                                    ],
                                style={'background-color' : 'GhostWhite', 'width' : '600px'})],
                                target = "decision-boundary",
                                placement = "bottom",
                )
            ]

        #Sets the values for the component to be displayed within the app
        self.componentTitle = "Decision Boundary Visualisation"
        
        self.componentChildren = html.Div(id = "decision-boundary-component", children=self.boundary)