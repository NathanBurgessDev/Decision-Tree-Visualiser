import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State

"""
AUTHOR: Alfred Greenwood
DATE CREATED: 8/02/2023
PREVIOUS MAINTAINER: Alfred Greenwood
DATE LAST MODIFIED: 10/02/2023

Used to simplify dash commands for the website, this class sets out the layout for the website so the
to simplify code usage of the main program
"""
class pageLayout():
    """
    Initialisies values for class, setting up each section of the webpage as their own variable
    Inputs: 
        name: Name of the webpage
    """
    def __init__(self, name):
        # Initialise the app
        self.app = dash.Dash()
        self.app.title = name

        # Inititialise dividers for the top half of the webapp then initialise in a seperate function
        self.titleDiv = None
        self.settingsDiv = None
        self.graphDiv = None
        self.visDiv = None
        self.topDivLayout = None
        self.topNavInit()

        # Init for bottom nav
        self.bottomDivLayout = None
        self.treeDiv = None
        self.ensembleDiv = None
        self.bottomNavInit()
        
        
    """
    Initialises the HTML div that contains the graphs, title, 
    """
    def topNavInit(self):
        self.titleDiv = html.Div(children=[html.H1(children="Results visualisation")], className="title")
        self.settingsDiv = html.Div(children=[], className="data")
        self.graphDiv = html.Div(children=[], className="graphnav")
        self.visDiv = html.Div(children=[], className="visnav")
        gandv = html.Div(children=[self.graphDiv, self.visDiv], className="graphandvis")
        self.topDivLayout = html.Div(children=[self.settingsDiv, gandv, self.titleDiv], className="topnav")

    """
    Initialises the HTML div that is at the bottom of the screen
    """

    def bottomNavInit(self):
        lButton = dbc.Button("<", color="primary", style={"position" : "absolute",
                "left" : "0",
                "bottom" : "0"
            }, className="scrollbutton")
        rButton = dbc.Button(">", color="primary", style={"position" : "absolute",
                "right" : "0",
                "bottom" : "0"
            }, className="scrollbutton")
        self.treeDiv = html.Div([], className="treenav")
        self.ensembleDiv = html.Div([lButton, rButton], className="ensemble")
        self.bottomDivLayout = html.Div(children=[self.treeDiv, self.ensembleDiv], className="bottomnav")
    
    """
    Runs the dash server
    Inputs: 
        dbg: Boolean representing whether the webapp should run in debug mode or not
    """
    def runServer(self, dbg):
        # Adds all segments to the 
        self.app.layout = html.Div(children=[
            self.topDivLayout,
            self.bottomDivLayout
            
            ])

        # Run server
        self.app.run_server(debug=dbg)
