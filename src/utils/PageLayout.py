import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

"""
AUTHOR: Alfred Greenwood
DATE CREATED: 8/02/2023
PREVIOUS MAINTAINER: Alfred Greenwood
DATE LAST MODIFIED: 14/02/2023

Used to simplify dash commands for the website, this class sets out the layout for the website so the
to simplify code usage of the main program
"""
class PageLayout():
    """
    Initialisies values for class, setting up each section of the webpage as their own variable
    Inputs: 
        name: Name of the webpage
    """
    def __init__(self, name, app):
        # Initialise the app
        self.app = app
        self.app.title = name

        # Inititialise dividers for the top half of the webapp then initialise in a seperate function
        self.sidebarDiv = None
        self.componentsDiv = None
        self.topNavInit()

        
    """
    Initialises the HTML div that contains the graphs, title and settings including the file upload and
    graph axis settings
    """
    def topNavInit(self):
        
        # Initialising the settings on the left side of the GUI with the upload box and graph settings
        self.sidebarDiv = html.Div([   
            html.H1(children="Results Visualisation", className="title"),
            html.H3(children = "Select A Model"),
            html.Div(id = "drop-down-parent", children = [dcc.Dropdown(id="trained-models", options = [], className = "dropdown")]),

            dcc.ConfirmDialog(
                id="upload-df-alert",
                message="Error!"
            ),

            dcc.ConfirmDialog(
                id="training-alert",
                message="Error!"
            ),

            html.H3(children="Train", style = {"border-top" : "2px solid rgb(200,200,200)", "padding" : "4px", "padding-top" : "10px"}),
            dcc.Upload(
                id="upload-dataset",
                children=[
                    html.Div(
                        id="upload-message-dataset",
                        children = ["Click To Upload A Dataset (.csv)"]
                    )  
                ],
                multiple=True, 
                className="upload"
            ),  
                               
            html.H4(children="Training Features"),
            dbc.Checklist(
                id="training-features",
                options=[],
                value=[],
                className="checklist",
            ),

            html.H4(children="Classifier"),
            dbc.Checklist(
                id="classifier",
                options=[],
                value=[],
                className="checklist",
            ),

            html.H4 (children="Class"),
            html.Div([dcc.Dropdown(id="training-class", options = ["Decision Tree Classifier", "Gradient Boosted Classifier"])], className = "dropdown"),

            
            html.H4 (children="Test - Train Split"),
            dcc.Slider(
                id="test-train-split",
                min = 0.05,
                max = 0.95,
                step = 0.025,
                value = 0.3,
                marks = {
                    0.05 : {"label": "0.05"},
                    0.25 : {"label": "0.25"},
                    0.5 : {"label": "0.5"},
                    0.75 : {"label": "0.75"},
                    0.95 : {"label": "0.95"}
                }
            ),
           
            html.Div(id = "classifier-settings", children = []),
            
            dcc.Input(
                id="training-filename",
                placeholder="Input Model Filename",
                className = "textInput"
            ),

            html.Div([html.Br()]),

            html.Button("Train", id="train-button", n_clicks = 0, className = "trainButton"),

            html.Div([html.Br()]),

        ], className="settings")

        self.componentsDiv = html.Div(id="model-components", className="classifierComponentContainer")
        

    """
    Runs the dash server
    Inputs: 
        dbg: Boolean representing whether the webapp should run in debug mode or not
    """
    def runServer(self, dbg):
        # Adds all segments to the 
        self.app.layout = html.Div(children=[
            self.sidebarDiv,
            self.componentsDiv,
            ])

        # Run server
        self.app.run_server(debug=dbg)
