from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
from utils.TreeUtil import TreeUtil

"""
AUTHOR: Ethan Temple-Betts
DATE CREATED: 22/02/2023
PREVIOUS MAINTAINER: Ethan Temple-Betts
DATE LAST MODIFIED: 22/02/2023

"""
class ClassifierTreeComponent(ClassifierComponent):

    def __init__(self, modelInfo):
        # An instance of 'TreeUtil is created'
        treeUtil = TreeUtil()

        # The model is parsed to 'TreeUtil.generateDecisionTree', this will 
        # return a 'dcc.Graph' object containing the tree
        self.tree = treeUtil.generateDecisionTree(modelInfo["modelData"])

        self.componentTitle = "Model Decision Tree"
        # Set component layout property to be a div containing the tree graph
        # Important : className of this div must be "classifierComponent" to format correctly
        self.componentChildren = html.Div(self.tree)


    