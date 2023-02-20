from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
from utils.DecisionBoundaryUtil import DecisionBoundaryUtil

class ClassifierDecisionBoundaryComponent(ClassifierComponent):

    def __init__(self, modelInfo):
        
        BoundaryUtil = DecisionBoundaryUtil()

        if(len(modelInfo["modelData"].feature_names_in_) == 1):
            self.boundary = BoundaryUtil.decisionBoundaries1D(modelInfo["modelData"], 0, modelInfo["trainingData"])
        elif(len(modelInfo["modelData"].feature_names_in_) == 2):
            self.boundary = BoundaryUtil.decisionBoundaries2D(modelInfo["modelData"], [0, 1], modelInfo["trainingData"])
        else:
            self.boundary = html.P("Higher Dimensions are not yet implemented")

        self.componentTitle = "Decision Boundary Visualisation"
        self.componentChildren = html.Div(id = "decision-boundary-component", children=self.boundary, className="ClassifierComponent")