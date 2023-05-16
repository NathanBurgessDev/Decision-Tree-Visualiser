from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
from utils.TreeUtil import TreeUtil
import dash_mantine_components as dmc

"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Kieran Patel
DATE LAST MODIFIED: 16/05/2023

Child of 'ClassifierComponent' this class defines will
define an appropriate 'componentLayout' based on random forest decision tree
visualisations.

Addiiton: The component now allows for other ensemble models to be visualised

"""
class ClassifierEnsembleModelsComponent(ClassifierComponent):

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
        self.componentTitle = self.getComponentTitle(modelInfo)

        #If the model is a random forest then generate the tooltip for the tree
        if modelInfo["classifierType"] == "RandomForestClassifier":
            # Name component title and add tooltips
            self.componentTitle = html.Span(
                dmc.Tooltip(
                    label = html.Div(children = [
                        # HTML for tooltip
                        html.H1("Random Forest Decision Tree"),
                        html.P("Random Forest is an ensemble model, which generates multiple decision trees"),
                        html.P("which are all applied to the given data and classifies the data using the majority vote of all the trees generated."),
                        html.P("Click the left or right arrows to navigate through the individual trees created by this method."),
                        html.P("You can hover over each node to see its Gini value - a measure of node purity."),
                        html.P("Leaf nodes, represented in green, are the terminal nodes of each tree. They provide the final decision output for the given inputs."),
                        html.P("This method provides a good prediction accuracy by reducing overfitting, but can be slow on large datasets.")
                        ]),
                    children=[html.P("Random Forest Decision Tree")],
                    id="randforest-tooltip",
                    className ="randforestToolTip",
                    withArrow = True,
                ))
        elif modelInfo["classifierType"] == "GradientBoostingClassifier":
            # Name component title and add tooltips
            self.componentTitle = html.Span(
                dmc.Tooltip(
                    label = html.Div(children = [
                        # HTML for tooltip
                        html.H1("Gradient Boosted Decision Tree"),
                        html.P("Gradient Boosting is an ensemble model which generates a series of weak decision trees"),
                        html.P("and each tree learns and improves on the previous by minimizing errors."),
                        html.P("Click the right arrow to navigate through the different stages of boosting, representing successive trees."),
                        html.P("You can hover over each node to see its Gini value - a measure of node purity."),
                        html.P("Leaf nodes, represented in green, are the terminal nodes of each tree. They provide the final decision output for the given inputs."),
                        html.P("Gradient Boosting optimizes for prediction accuracy by sequentially correcting the mistakes of the previous trees"),
                        html.P("but may be more prone to overfitting compared to Random Forest.")
                        ]),
                    children=[html.P("Gradient Boosted Decision Tree")],
                    id="gradboost-tooltip",
                    className ="gradboostToolTip",
                    withArrow = True,
                ))



        # Set component layout property to be a div containing the tree graph
        # Important : className of this div must be "classifierComponent" to format correctly
        self.componentChildren = multiTreeShell

    def getComponentTitle(self, modelInfo):
        classifier = modelInfo["classifierType"]
        if classifier == "GradientBoostingClassifier":
            return "Gradient Boosted Decision Tree"
        elif classifier == "RandomForestClassifier":
            return "Random Forest Decision Tree"
        else:
            #Can add more ensemble models here
            return "Unknown Decision Tree"




