from dash.dependencies import Input, Output, State
from dash import ctx
import dash
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from utils.TreeUtil import TreeUtil
from AppInstance import AppInstance
from UserSession import UserSession
from flask import request
"""
AUTHOR: Dominic Cripps
DATE CREATED: 23/02/2023
PREVIOUS MAINTAINER: Kieran Patel
DATE LAST MODIFIED: 16/05/2023

Callback is triggered when the buttons 'back-button-tree' or 'forward-button-tree' are clicked.

The callback output is the children of the HTML divs 'subtree-label' and 'subtree-graph'.

The function 'circularTree' checks the type of ensemble model being used and generates the corresponding tree visualization.

Addition: the circular tree now allows checks which type of ensemble model is
being used and outputs the correct tree visualisation.

"""
app = AppInstance().instance.app
@app.callback(
    [Output(component_id="subtree-label", component_property="children"),
        Output(component_id="subtree-graph", component_property="children")],
    [Input("back-button-tree", component_property="n_clicks"),
        Input("forward-button-tree", component_property="n_clicks"),
        State("user-session-name", component_property="value")
        ]
)
def circularTree(backClick, forwardClick, sessionID):
    classifier = UserSession().instance.selectedModel[sessionID]
    length = len(classifier.estimators_)
    index = (forwardClick - backClick) % length
    
    if isinstance(classifier, RandomForestClassifier):
        model = classifier.estimators_[index]
        tree = model.tree_
    elif isinstance(classifier, GradientBoostingClassifier):
        model = classifier.estimators_[index][0]
        tree = model.tree_
    else:
        # Handle other classifier types if needed
        return None

    treeUtil = TreeUtil()
    tree = treeUtil.generateDecisionTree(classifier, model, tree, sessionID)
    
    return "Subtree: " + str(index + 1) + "/" + str(length), tree


