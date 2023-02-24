from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
from utils.DecisionBoundaryUtil import DecisionBoundaryUtil

"""
AUTHOR: Daniel Ferring
DATE CREATED: 19/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 20/02/2023

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

        if(len(modelInfo["modelData"].feature_names_in_) > 2):
            self.boundary = html.P("Higher Dimensions are not yet implemented")
        else:
            self.boundary = BoundaryUtil.generateDecisionBoundary(modelInfo["modelData"], modelInfo["trainingData"])

        #Sets the values for the component to be displayed within the app
        self.componentTitle = "Decision Boundary Visualisation"
        self.componentChildren = html.Div(id = "decision-boundary-component", children=self.boundary)