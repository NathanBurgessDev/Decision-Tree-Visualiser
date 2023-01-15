import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output
from Util import ImportUtil as iu
from Util import GraphUtil as gu
import unittest

app = dash.Dash(__name__)

app.title = "Data visualisation"

app.layout = html.Div(
    children=[
        html.Div([

            html.H1(children="Results Visualisation"),
        
            dcc.Graph(id='Mygraph'),
            
        ], className="body"),

        html.Div([
            html.P(
                children="Drop a CSV file below to display its data"
            ),
            
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    ["Drag and drop or click to select a file to upload."],
                    style={
                        "inline-size" : "auto",
                    }
                ),
                style={   
                    "lineHeight": "30px",                 
                    "width": "90%",
                    "height": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                    "background-color" : "initial",
                    "color" : "rgb(0, 0, 0)",
                },
                multiple=True,
            ),

            html.H5(children="Choose a X-axis feature"),
            html.Div([dcc.Dropdown(id="x_feature", options = [])]),
            html.H5(children="Choose a Y-axis feature"),
            html.Div([dcc.Dropdown(id="y_feature", options = [])]),
            html.H5(children="Choose a Z-axis feature"),
            html.Div([dcc.Dropdown(id="z_feature", options = [])]),
            html.H5(children="Choose the classification feature"),
            html.Div([dcc.Dropdown(id="class_feature", options = [])]),
            
        ], className="sidenav")
    ] 
)

@app.callback(
    [Output(component_id = "x_feature", component_property='options'),
     Output(component_id = "y_feature", component_property='options'),
     Output(component_id = "z_feature", component_property='options'),
     Output(component_id = "class_feature", component_property='options')],
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def displayFeatureDropDowns(filename, contents):
    global df
    if contents:
        df = iu.csvToDataFrame(iu.readContent(filename, contents[0]))
        return df.columns, df.columns, df.columns, df.columns
    else:
        return [], [] , [], []

@app.callback(
    Output(component_id = "Mygraph" , component_property = 'figure'),
    [Input("x_feature", component_property = "value"),
     Input("y_feature", component_property = "value"),
     Input("z_feature", component_property = "value"),
     Input("class_feature", component_property = "value")]
)
def displayGraph(value1, value2, value3, classFeature):
    global df

    cf = False
    if(classFeature):
        cf = classFeature
        
    if(value1 and value2 and value3):
        return gu.scatter3D(df, value1, value2, value3, cf)
    elif(value1 and value2):
        # return gu.scatter2D(df, value1, value2, cf)
        return gu.getDecisionBoundary2D(df,value1,value2,cf)
    else:
        return gu.getGraph()

if __name__ == "__main__":
    app.run_server(debug=True)

