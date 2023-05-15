import dash
import dash_bootstrap_components as dbc
import traceback
from dash import html
from dash import dcc

"""
AUTHOR: Alfred Greenwood
DATE CREATED: 8/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 07/05/2023

Used to simplify dash commands for the website, this class sets out the layout for the website so the
to simplify code usage of the main program
"""
class PageLayout():

    """
    AUTHOR: Alfred Greenwood
    DATE CREATED: 14/02/2023
    PREVIOUS MAINTAINER: Dominic Cripps
    DATE LAST MODIFIED: 18/02/2023

    Initialisies values for class, setting up each section of the webpage as their own variable
    Inputs: 
    String name: Name of the webpage
    Dash() app : Instance of the app 
    """
    def __init__(self, name, app):
        # Sets a reference to app
        self.app = app
        # Sets title of the app
        self.app.title = name

        # Inititialise dividers - sidebar, component body
        self.sidebarDiv = None
        self.componentsDiv = None

        # A list containing all classifiers that have training support
        self.SUPPORTED_CLASSIFIERS = [
            "Decision Tree Classifier", 
            "Gradient Boosted Classifier",
            "Random Forest Classifier",
            "SVM Classifier",
        ]

        # Initialises HTML that contains all components
        self.displayInit()

        try:
            self.app.layout = html.Div(children=[
            self.sidebarDiv,
            self.componentsDiv,
            ])
        except:
            traceback.print_exc()
        

    """
    AUTHOR: Alfred Greenwood
    DATE CREATED: 14/02/2023
    PREVIOUS MAINTAINER: Dominic Cripps
    DATE LAST MODIFIED: 07/05/2023

    Defines the HTML divs that contain both the sidebar div and main body div.
    """
    def displayInit(self):
        
        # Defines the structure of the sidebar div.
        self.sidebarDiv = html.Div([   
            # Adds a title
            html.H1(children="Results Visualisation", className="title"),
            # Adds a link to the user manual
            html.A("View User Manual", href='https://team44usermanual.netlify.app/', className="link"),
            html.H3(children = "Select A Model"),
            # A dropdown containing all available / trained models
            html.Div(id = "drop-down-parent", children = [dcc.Dropdown(id="trained-models", options = [], className = "dropdown")]),

            # Error Popup objects 

            # This one is for errors caused by uploading the dataframe
            dcc.ConfirmDialog(
                id="upload-df-alert",
                message="Error!"
            ),

            # This one is for errors that occur when performing sanitation checks
            # during training
            dcc.ConfirmDialog(
                id="training-alert",
                message="Error!"
            ),

            # New Section for user session UI components
            html.H3(children="Session", style = {"border-top" : "2px solid rgb(200,200,200)", "padding" : "4px", "padding-top" : "10px"}),

            html.H4(id = "session-id-display", children="Current Session : "),
            # Input component to take a session name
            dcc.Input(
                id="user-session-name",
                placeholder="Input Session ID",
                className = "textInput"
            ),
            html.Button("Enter User Session", id="user-session-button", n_clicks = 0, className = "trainButton"),

            # New section indicated the heading 'Train'
            html.H3(children="Train", style = {"border-top" : "2px solid rgb(200,200,200)", "padding" : "4px", "padding-top" : "10px"}),

            # Upload component used for dataframes
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

            # Title and checklist for selecting which features to train              
            html.H4(children="Training Features"),
            dbc.Checklist(
                id="training-features",
                options=[],
                value=[],
                className="checklist",
            ),

            # Title and checklist for selecting which feature to use as classifier
            html.H4(children="Classifier"),
            dbc.Checklist(
                id="classifier",
                options=[],
                value=[],
                className="checklist",
            ),

            # Title and dropdown for selecting which classifier to train the model with
            html.H4 (children="Model"),
            html.Div([dcc.Dropdown(id="training-class", options = self.SUPPORTED_CLASSIFIERS)], className = "dropdown"),

            # Title and slider for selecting the Test and Train split of the 
            # imported dataframe.
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

            # Input component to take model filename
            dcc.Input(
                id="training-filename",
                placeholder="Input Model Filename",
                className = "textInput"
            ),

            html.Div([html.Br()]),

            # Button used to train the appropriate model
            html.Button("Train", id="train-button", n_clicks = 0, className = "trainButton"),

            html.Div([html.Br()]),

            # Div that will contain all settings that are specific to the selected
            # classifier.
            html.Div(id = "classifier-settings", children = [], style={"margin-bottom" : "20px"}),

        ], className="settings")


        # Define the div that will contain all components related to the selected model
        self.componentsDiv = html.Div(id="model-components", className="classifierComponentContainer", children=[])
        

    """
    AUTHOR: Alfred Greenwood
    DATE CREATED: 14/02/2023
    PREVIOUS MAINTAINER: Dominic Cripps
    DATE LAST MODIFIED: 18/02/2023

    Updates the app layout and runs the dash server.

    Inputs: 
    Boolean dbg : representing whether the webapp should run in debug mode or not
    """
    def runServer(self, dbg):
        # Run server
        self.app.run_server(debug=dbg)
