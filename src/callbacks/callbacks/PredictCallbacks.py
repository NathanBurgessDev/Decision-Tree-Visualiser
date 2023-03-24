from dash.dependencies import Input, Output, State, ALL
from dash import ctx
import dash
from UserSession import UserSession
import pandas as pd
import numpy as np
from AppInstance import AppInstance
import plotly.graph_objects as go
from dash import dcc

"""
AUTHOR: Dominic Cripps
DATE CREATED: 23/02/2023
PREVIOUS MAINTAINER: Daniel Ferring
DATE LAST MODIFIED: 19/03/2023

Callback is triggered when the button 'predict-button' is pressed.

Callback output is the children of the html div 'prediction'.

The function 'predictInput' will form a data frame out of the
inputted feature values, it will then use the selected model
to make a prediction and return that to the user.

"""
app = AppInstance().instance.app
@app.callback(
    [Output(component_id="prediction", component_property="children"),
        Output(component_id="decision-boundary-component", component_property="children")],
    [Input("predict-button", component_property="n_clicks"),
        State(dict(name="prediction-features", idx=ALL), "value"),
        State("decision-boundary-component", component_property = "children")]
)
def predictInput(clicks, features, boundaryData):
    
    if "predict-button" == ctx.triggered_id:
        if not None in features:
            df = pd.DataFrame(data = np.array([features]), 
                columns = UserSession().instance.selectedModel.feature_names_in_)

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