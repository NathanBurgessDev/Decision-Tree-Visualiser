from dash.dependencies import Input, Output, State, ALL
from dash import ctx
import dash
from dash import Dash, dcc, html
from UserSession import UserSession
import pandas as pd
import numpy as np
from AppInstance import AppInstance



"""
AUTHOR: Ethan Temple-Betts
DATE CREATED: 04/03/2023
PREVIOUS MAINTAINER: Ethan Temple-Betts
DATE LAST MODIFIED: 04/03/2023

Callback is triggered when the '+' or '-' buttons are pressed

Callback output is the parallel coordinates figure.

The function 'changeDim' will attempt to add or remove
the feature curently selected in the dimension dropdown box
based on wether the '-' or '+' button was pressed.
It does this by changing the dimensions visibility property
to True or False, whichever is appropriate.

"""
app = AppInstance().instance.app
@app.callback(
    [Output(component_id="pc_plot", component_property="figure")],
    [Input("pc_dim_select", component_property="value"),
        Input("pc_add_dim", component_property = "n_clicks"),
        Input("pc_del_dim", component_property = "n_clicks"),
        Input("pc_plot", component_property = "figure")]
)
def changeDim(value, addClicks, delClicks, fig):
    
    if "pc_add_dim" == ctx.triggered_id:
        for i in fig['data'][0]['dimensions']:
            # If the specified dimension is not visible
            # then make it visible
            if (value == i['label']) and (i['visible'] == False):
                i['visible'] = True

    elif "pc_del_dim" == ctx.triggered_id:
        for i in fig['data'][0]['dimensions']:
            # If the specified dimension is visible
            # then make it  not visible
            if (value == i['label']) and (i['visible'] == True):
                i['visible'] = False


    return [fig]
