from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
from utils.TreeUtil import TreeUtil

"""
AUTHOR: Kieran Patel
DATE CREATED: 17/05/2023

Child of 'ClassifierComponent' this class defines will
define an appropriate 'componentLayout' based on a gradient boosted decision tree
visualisation.
"""
class ClassifierGradientBoostedComponent(ClassifierComponent):

    def __init__(self, modelInfo):
        # An instance of 'TreeUtil is created'
        treeUtil = TreeUtil()

        arrowStyle = {
            "text-align" : "center",
            "width" : "35px",
            "margin-right" : "4px",
            "padding-top" : "10px",
            "padding-bottom" : "10px",
            "height" : "70px",
            "font-size" : "16px",
            "margin-top" : "auto",
            "margin-bottom" : "auto"
        }

        multiTreeShell = html.Div(children = [
            html.Button("<", id="back-button-tree", n_clicks = 0, className = "trainButton", style = arrowStyle),

            html.Div(children = [
                html.H4(id = "subtree-label"),
                html.Div(id = "subtree-graph")
            ],
            id = "subtree-container", style = {"width" : "100%", "min-height" : "50rem"}),

            html.Button(">", id="forward-button-tree", n_clicks = 0, className = "trainButton", style = arrowStyle)
        ],
        style = {"display" : "flex", "max-height" : "30rem", "margin-top" : "20px"})

        # The model is parsed to 'TreeUtil.generateDecisionTree', this will 
        # return a 'dcc.Graph' object containing the tree
        self.componentTitle = "Gradient Boosted Decision Tree"
        # Set component layout property to be a div containing the tree graph
        # Important : className of this div must be "classifierComponent" to format correctly
        self.componentChildren = multiTreeShell




