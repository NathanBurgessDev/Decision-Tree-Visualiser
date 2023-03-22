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
                    html.Div(title, style = {"font-size" : "16px", "font-weight" : "bold", "margin" : "5px", "text-align" : "left"}),
                    html.Div(componentText, style = {"font-size" : "12px", "margin" : "5px"})
                ],
            style = {
            "background-color" : "rgb(35, 35, 35)",
            "color" : "rgb(240, 240, 240)",
            "overflow-y" : "hidden",
            "max-height" : "200px",
            "width" : "500px" ,
            "border-radius" : "5px",
            "border-style" : "solid",
            "border-color" : "rgb(165, 117, 222)",
            "border-width" : "2px"
            }
            )],
            placement = "bottom",
        )
        return tooltip

    
       
        