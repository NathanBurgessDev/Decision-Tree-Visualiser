from dash.dependencies import Input, Output, State
from dash import ctx
import dash
from utils.TreeUtil import TreeUtil
from AppInstance import AppInstance
from UserSession import UserSession
from flask import request
"""
AUTHOR: Dominic Cripps
DATE CREATED: 23/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 23/02/2023

Callback is triggered when the button 'predict-button' is pressed.

Callback output is the children of the html div 'prediction'.

The function 'predictInput' will form a data frame out of the
inputted feature values, it will then use the selected model
to make a prediction and return that to the user.

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
    index  = (forwardClick - backClick) % length
    model = classifier.estimators_[index]
    tree = model.tree_
    treeUtil = TreeUtil()
    tree = treeUtil.generateDecisionTree(classifier, model, tree, sessionID)
    return "Subtree : " + str(index + 1) + "/" + str(length), tree

