import dash_bootstrap_components as dbc
from dash import html

"""
AUTHOR: Daniel Ferring
DATE CREATED: 22/03/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 22/03/2023

This is a simple util class that will generate a tooltip object based on provided 
user input for target component, title, and component description.
"""

class ToolTip():
    
    def generateToolTip(self, componentID, title, componentText):
        tooltip = dbc.Tooltip(
            target = componentID,
            children = [
                html.Div(children = [
                    html.Div(title, className = "toolTipTitle"),
                    html.Div(componentText, className = "toolTipDescription")
                ], className = "toolTipContainer")],
            placement = "bottom",
        )
        return tooltip

    
       
        