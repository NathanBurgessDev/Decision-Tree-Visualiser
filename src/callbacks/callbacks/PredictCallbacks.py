from dash.dependencies import Input, Output, State, ALL, MATCH
from dash import ctx
import dash
from UserSession import UserSession
import pandas as pd
import numpy as np
from utils.TreeUtil import TreeUtil
from igraph import Graph
from AppInstance import AppInstance
import plotly.graph_objects as go
from dash import dcc

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

It will get the path that the user input will take through the tree, it will extract this path
draw a new scatter plot with those edges and overlay it ontop of the original tree.

It will get the old decision boundary plot and overlay a scatter plot with the new points ontop.
"""
app = AppInstance().instance.app
@app.callback(
    [Output(component_id="prediction", component_property="children"),
        Output({'type': 'decision-boundary-component', 'index': ALL}, 'children'),
        Output({'type': 'decision-tree-component', 'index': ALL}, 'children')
        ],
    [Input("predict-button", component_property="n_clicks"),
        State(dict(name="prediction-features", idx=ALL), "value"),
        Input("trained-models", component_property="value")]
)
def predictInput(clicks, features, modelFilename):

    if "predict-button" == ctx.triggered_id and not None in features:
        modelInfo = UserSession().instance.modelInformation[modelFilename]
        #get the model info from singleton
        #make a dataframe out of the input features
        df = pd.DataFrame(data = np.array([features]), 
                columns = UserSession().instance.selectedModel.feature_names_in_)
        classification = UserSession().instance.selectedModel.predict(df)

        #make sure that all features have inputs and there is both a boundary and tree
        if((modelInfo["classifierType"] == "DecisionTreeClassifier")):                

            #create empty arrays for the new tree and boundary plots
            dTree = []
            graph = []

            #tree highlight path behaviour 
            #only highlight tree if its a decision tree classifier
            #THIS RE-USES SOME CODE FROM TREEUTIL WHICH IS ATTRIBUTED TO ETHAN
            #get the tree
            tree = modelInfo["modelData"].tree_
            #get the feature names of the tree
            featureNames = modelInfo["modelData"].feature_names_in_
            #create a tree util
            treeUtil = TreeUtil()
            #generate a tree - same as the original one
            treeUtil.generateDecisionTree(modelInfo["modelData"], modelInfo["modelData"], modelInfo["modelData"].tree_)

            #create a graph and add the correct edges and vertices etc.
            graphComp = Graph(directed = "T")
            graphComp.add_vertices(treeUtil.getVerticies())
            graphComp.add_edges(treeUtil.getEdges())

            #get an array of the edges between nodes
            Edges = [e.tuple for e in graphComp.es]

            #create empty array for the path
            path = []
            currNode = 0
            #iterate until the eval node has no children - it has been classified
            while(tree.children_left[currNode] != -1 and tree.children_right[currNode] != -1):
                #get the threshold value of the current node
                threshold = tree.threshold[currNode]
                #set the previous node to be this
                previousNode = currNode

                #check the correct feature value against the correct threshold
                if(float(df[featureNames[tree.feature[currNode]]].iloc[0]) <= float(threshold)):
                    #go left down the tree
                    for edge in Edges:
                        if(edge[0] == previousNode ):
                            currNode = edge[1]
                            break
                else:
                    #go right down the tree
                    count = 0
                    for edge in Edges:
                        if(edge[0] == previousNode):
                            count += 1
                            currNode = edge[1]
                            if(count == 2):
                                break

                #add the previous and current node to the path, a tuple representing the edge it took
                path.append((previousNode, currNode))

            #calculate the layout of the tree to match the one used in tree generation
            lay = graphComp.layout('rt')

            #make an array of positions given each edge tuple
            position = {k: lay[k] for k in range(modelInfo["modelData"].tree_.node_count)}
            #calculate an array of the Y values used in the scatter
            Y = [lay[k][1] for k in range(modelInfo["modelData"].tree_.node_count)]
            #M is the maximum height in Y 
            M = max(Y)

            #E is set to the path taken in the prediction - this is extracted from the graph
            E = path

            #iterate to create an array of X positions and Y positions for each edge
            Xe = []
            Ye = []
            for edge in E:
                Xe+=[position[edge[0]][0],position[edge[1]][0], None]
                Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

            #draw the scatter to include the new edges - these are thicker than the original
            edges = go.Scatter(x=Xe,
                y=Ye,
                mode='lines',
                line=dict(color='rgb(210,210,210)', width=4),
                hoverinfo='none'
                )

            #get the original tree from singleton class
            dTree = UserSession().instance.selectedTree
            #add the highlighted edge to this plot
            dTree.add_trace(edges)
            #set dTree to be the new contents of the tree
            dTree = [dcc.Graph(figure = dTree)]
                
            
            #boundary plot point behaviour
            numFeatures = len(features)

            #if a decision boundary plot exists and it is trained with fewer than 3 features
            if(numFeatures < 3 and UserSession().instance.selectedBoundary != None):
                #determine whether it is 1D or 2D and set the x and y appropriately
                xPoint = [features[0]]
                if(numFeatures == 1):
                    yPoint = [0]
                else:
                    yPoint = [features[1]]

                #create a new scatter with just the new point
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

                #get the original graph from the singleton class
                graph = UserSession().instance.selectedBoundary
                #overlay the new scatter
                graph.add_trace(scatter)
                #remove legends
                graph.update_layout(showlegend = False)
                #set the new graph object
                graph = [dcc.Graph(figure = graph)]
            

            #return the classification and updated components.
            return classification, graph, dTree
        else:
            return classification, [], []
    return dash.no_update
