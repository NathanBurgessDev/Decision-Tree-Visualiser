from dash.dependencies import Input, Output, State, ALL
from dash import ctx
import dash
from UserSession import UserSession
import pandas as pd
import numpy as np
from utils.TreeUtil import TreeUtil
from igraph import Graph, EdgeSeq

import plotly.graph_objects as go
from dash import dcc

def get_callbacks(app):

    """
    AUTHOR: Dominic Cripps
    DATE CREATED: 23/02/2023
    PREVIOUS MAINTAINER: Dominic Cripps
    DATE LAST MODIFIED: 21/03/2023

    Callback is triggered when the button 'predict-button' is pressed.

    Callback output is the children of the html div 'prediction'.

    The function 'predictInput' will form a data frame out of the
    inputted feature values, it will then use the selected model
    to make a prediction and return that to the user.

    """
    @app.callback(
        [Output(component_id="prediction", component_property="children"),
         Output(component_id="decision-boundary-component", component_property="children")],
        [Input("predict-button", component_property="n_clicks"),
            State(dict(name="prediction-features", idx=ALL), "value"),
            State("decision-boundary-component", component_property = "children"),
            Input("trained-models", component_property="value")]
    )
    def predictInput(clicks, features, boundaryData, modelFilename):
        
        if "predict-button" == ctx.triggered_id:
            if not None in features:
                modelInfo = UserSession().instance.modelInformation[modelFilename]

                df = pd.DataFrame(data = np.array([features]), 
                    columns = UserSession().instance.selectedModel.feature_names_in_)

                #tree highlight behaviour 
                if(modelInfo["classifierType"] == "DecisionTreeClassifier"):
                    tree = modelInfo["modelData"].tree_
                    featureNames = modelInfo["modelData"].feature_names_in_
                    x = [0.0]
                    y = [10.0]
                    path = []
                    currX = 0
                    depth = 0
                    currNode = 0
                    while(tree.children_left[currNode] != -1 and tree.children_right[currNode] != -1):
                        threshold = tree.threshold[currNode]
                        previousNode = currNode
                        if(depth > 0):
                            x.append(x[len(x) - 2])
                            y.append(y[len(y) - 2])

                        if(float(df[featureNames[tree.feature[currNode]]].iloc[0]) <= float(threshold)):
                            currX -= 0.5
                            x.extend([currX, None])
                            currNode += 1
                        else:
                            currX += 0.5
                            x.extend([currX, None])
                            currNode += 2

                        path.append((previousNode, currNode))
                        depth += 1
                        y.extend([10.0 - depth, None])

                    treeUtil = TreeUtil()
                    treeUtil.generateDecisionTree(modelInfo["modelData"], modelInfo["modelData"], modelInfo["modelData"].tree_)

                    print(path)
                    graphComp = Graph(directed = "T")
                    vertices = list(range(0, modelInfo["modelData"].tree_.node_count))
                    graphComp.add_vertices(treeUtil.getVerticies())
                    graphComp.add_edges(treeUtil.getEdges())
                    print(graphComp)

                    lay = graphComp.layout('rt')
                    v_label = list(map(str, range(modelInfo["modelData"].tree_.node_count)))
                    position = {k: lay[k] for k in range(modelInfo["modelData"].tree_.node_count)}
                    Y = [lay[k][1] for k in range(modelInfo["modelData"].tree_.node_count)]
                    M = max(Y)

                    es = EdgeSeq(graphComp)
                    E = path

                    L = len(position)
                    Xn = [position[k][0] for k in range(L)]
                    Yn = [2*M-position[k][1] for k in range(L)]
                    Xe = []
                    Ye = []
                    for edge in E:
                        Xe+=[position[edge[0]][0],position[edge[1]][0], None]
                        Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

                    print(Xe)
                    print(Ye)


                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=Xe,
                        y=Ye,
                        mode='lines',
                        line=dict(color='rgb(210,210,210)', width=2),
                        hoverinfo='none'
                        ))    
                    fig.show()


                
                #boundary plot point behaviour
                classification = UserSession().instance.selectedModel.predict(df)
                numFeatures = len(features)

                if(numFeatures < 3 and boundaryData != None):
                    xPoint = [features[0]]
                    if(numFeatures == 1):
                        yPoint = [0]
                    else:
                        yPoint = [features[1]]

                    scatter = go.Scatter(x = xPoint, 
                                y = yPoint, 
                                mode = 'markers',
                                hoverinfo = 'text',
                                hovertext = classification + ' (user input)',
                                marker = dict(size = 10,
                                            colorscale = 'sunset',
                                            color = numFeatures + 1,
                                            symbol = 27,
                                            line = dict(color = 'black', 
                                            width = 1))
                                )

                    graph= boundaryData[0]["props"]
                    graph = go.Figure(graph["figure"])
                    graph.add_trace(scatter)
                    graph.update_layout(showlegend = False)

                    return classification, [dcc.Graph(figure = graph)]
                
                else:
                    return classification, dash.no_update
        return dash.no_update, dash.no_update