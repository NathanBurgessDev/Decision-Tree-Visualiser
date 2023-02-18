from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
from utils.TreeUtil import TreeUtil

"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

Child of 'ClassifierComponent' this class defines will
define an appropriate 'componentLayout' based on a decision tree
visualisation.
"""
class ClassifierTreeComponent(ClassifierComponent):

    def __init__(self, model):
        # An instance of 'TreeUtil is created'
        treeUtil = TreeUtil()

        # The model is parsed to 'TreeUtil.generateDecisionTree', this will 
        # return a 'dcc.Graph' object containing the tree
        self.tree = treeUtil.generateDecisionTree(model)

        # Set component layout property to be a div containing the tree graph
        # Important : className of this div must be "classifierComponent" to format correctly
        self.componentLayout = html.Div(id = "model-tree-component", children = self.tree, className = "classifierComponent") 


    