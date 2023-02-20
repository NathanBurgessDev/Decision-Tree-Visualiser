from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
from utils.DecisionBoundaryUtil import DecisionBoundaryUtil

class ClassifierDecisionBoundaryComponent(ClassifierComponent):

    def __init__(self, model, trainingData):
        
        BoundaryUtil = DecisionBoundaryUtil()

        if(len(model.feature_names_in_) == 1):
            self.boundary = BoundaryUtil.decisionBoundaries1D(model, 0, trainingData)
        elif(len(model.feature_names_in_) == 2):
            self.boundary = BoundaryUtil.decisionBoundaries2D(model, [0, 1], trainingData)
        else:
            self.boundary = html.P("Higher Dimensions are not yet implemented")

        self.componentLayout = html.Div(id = "decision-boundary-component", children=self.boundary, className="ClassifierComponent")