import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from igraph import Graph
from Util import ImportUtil as iu
from Util import GraphUtil as gu
import TreeUtil as T
import unittest

app = dash.Dash(__name__)

app.title = "Data visualisation"

app.layout = html.Div(
    children=[
        html.Div([

            html.H1(children="Results Visualisation"),
        
            dcc.Graph(id='Mygraph'),
            html.Div(id='treevis'),
            
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

            dcc.Upload(
                id="upload-data-MLM",
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

"""
AUTHOR: Ethan Temple-Betts
PREVIOUS MAINTAINER: Ethan Temple-Betts

Displays the visualisation of a decision tree as a tree graph.

INPUTS:
filename: The string name of the file uploaded by the user
contents: The contents of the uploaded file as base64 data
"""
@app.callback(
    [Output(component_id = "treevis", component_property = "children")],
    [Input("upload-data-MLM", "filename"), Input("upload-data-MLM", "contents")]
)
def displayTreeStructure(filename, contents):
    global model
    global df

    # If the user uploads a file then display the tree structure,
    # else display an empty graph
    if contents:
        # Convert the base64 file content into a python MLM
        # object
        model = iu.unPickle(iu.readPickle(filename, contents[0]))
        graphs = []

        tu = T.TreeUtil()

        """ 
        The parseTree function changes several member variables
        within the TreeUtil object.

        verticies : int - represents the number of verticies in
        the tree graph.

        edges : list[tuple] - list of tuples representing the
        undirected and unweighted edges between all vertices.
        Each vertex has an ID (0..n), therefore a tuple (0,1)
        represents an edge between the root node and node 1.

        annotations : list[str] - list of strings that contain
        the feature and threshhold used at each node in the tree.

        These variables can then be accessed through calls to:
        getVerticies()
        getEdges()
        getAnnotations()
        """
        tu.parseTree(model)

        # Specify that the graph is undirected
        G = Graph(directed = "T")
        # Specify the number of verticies in the graph
        G.add_vertices(tu.getVerticies())
        # Add the edges calculated by the call to parseTree()
        G.add_edges(tu.getEdges())
        # VertexSeq "info" holda the annotations for each node
        # indexed by node ID
        G.vs["info"] = tu.getAnnotations()
        # Convert the igraph Graph object into a visual plotly
        # go.Figure() object
        f = gu.generateTreeGraph(G, tu.getVerticies())
        
        graphs.append(dcc.Graph(
                    figure = f))

        return graphs
    else:
        return [dcc.Graph(figure = gu.getGraph())]

"""
AUTHOR: Ethan Temple-Betts
PREVIOUS MAINTAINER: Ethan Temple-Betts

Update the content of the feature dropdowns to contain the
columns of the uploaded CSV.

INPUTS:
filename: The string name of the file uploaded by the user
contents: The contents of the uploaded file as base64 data
"""
@app.callback(
    [Output(component_id = "x_feature", component_property='options'),
     Output(component_id = "y_feature", component_property='options'),
     Output(component_id = "z_feature", component_property='options'),
     Output(component_id = "class_feature", component_property='options')],
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def displayFeatureDropDowns(filename, contents):
    global df

    # If the user uploads a CSV then display the columns, else
    # display empty options
    if contents:
        # Convert the base64file content to a data frame
        df = iu.csvToDataFrame(iu.readContent(filename, contents[0]))
        return df.columns, df.columns, df.columns, df.columns
    else:
        return [], [] , [], []

"""
AUTHOR: Ethan Temple-Betts
PREVIOUS MAINTAINER: Nathan Burgess

Display the feature space extracted from the users CSV.
If a classification feature and an x and y feature is selected,
then display the decsioon boundary.

INPUTS:
str value1: X axis feature
str value2: Y axis feature 
str value3: Z axis feature 
str classFeature: The feature used to classifiy the data

"""
@app.callback(
    Output(component_id = "Mygraph" , component_property = 'figure'),
    [Input("x_feature", component_property = "value"),
     Input("y_feature", component_property = "value"),
     Input("z_feature", component_property = "value"),
     Input("class_feature", component_property = "value")]
)
def displayFeatureSpace(value1, value2, value3, classFeature):
    global df

    cf = False
    # If a classFeature is provided then the scatter graph
    # created will colour code the data based on that feature
    if(classFeature):
        cf = classFeature
        
    # If x,y and z axis features are provided, create a 3d
    # scatter graph
    if(value1 and value2 and value3):
        return gu.scatter3D(df, value1, value2, value3, cf)
    # If x,y is provided, create the 2D plot
    # with decision boundary
    elif(value1 and value2):
        return gu.getDecisionBoundary2D(df,value1,value2,cf)
    # else display an empty graph
    else:
        return gu.getGraph()

if __name__ == "__main__":
    app.run_server(debug=True)