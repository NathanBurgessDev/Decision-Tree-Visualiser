from dash.dependencies import Input, Output, State, ALL
from dash import ctx
import dash
from UserSession import UserSession
import pandas as pd
import numpy as np

def get_callbacks(app):

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
    @app.callback(
        [Output(component_id="prediction", component_property="children")],
        [Input("predict-button", component_property="n_clicks"),
            State(dict(name="prediction-features", idx=ALL), "value")]
    )
    def predictInput(clicks, features):
        
        if "predict-button" == ctx.triggered_id:
            if not None in features:
                df = pd.DataFrame(data = np.array([features]), 
                    columns = UserSession().instance.selectedModel.feature_names_in_)
               
                return [UserSession().instance.selectedModel.predict(df)]
            
        return dash.no_update