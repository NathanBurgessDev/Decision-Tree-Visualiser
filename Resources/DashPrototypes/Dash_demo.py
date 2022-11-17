import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import base64
import io
from io import StringIO

app = dash.Dash(__name__)

#changes title on the tab
app.title = "Data visualisation"


# The web page layout is all defined in here dash converts it all to html
app.layout = html.Div(
    children=[
        
        # This defines the web page header and paragraph at the top of the page
        html.H1(children="Results Visualisation",),
        
        html.P(
            children=
            """
                Drop a CSV file below to display its data
            """
        ),
        #

        # This is the drop box for files
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
                "background-color" : "initial",
                "color" : "rgb(255, 255, 255)",
            },
            multiple=True,
        ),
        #

        # These are the dropdown boxes to select which features to display
        html.Div([dcc.Dropdown(id="x_feature", options = [])]),
        html.Div([dcc.Dropdown(id="y_feature", options = [])]),
        #

        # This is the graph component
        dcc.Graph(id='Mygraph')
    ] 
)
#

### Takes the data from the uploaded file
### and converts it from bytes to a string
def readContent(file, content):
    # content_type could help to distingush between different file types csv, json, xls
    # at the moment i just assume a csv file
    content_type, content_string = content.split(',')
    contentBytes = base64.b64decode(content_string)
    stringContent = contentBytes.decode('utf-8')
    return stringContent

### Takes in the string content from the csv file and converts it to a data frame object
def csvToDataFrame(csv):
    data = StringIO(csv)
    df = pd.read_csv(data, sep=",")
    return df

### component_id is a reference to the id specified in the layout above
### component_property is used to specify the property you would like to
### change (in the case of an Output) or take in as a paramater in the function
### below (in the case of an Input)
@app.callback(
    [Output(component_id = "x_feature", component_property='options'),
     Output(component_id = "y_feature", component_property='options')],
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def displayFeatureDropDowns(filename, contents):
    global df
    if contents:
        df = csvToDataFrame(readContent(filename, contents[0]))
        return df.columns, df.columns
    else:
        return [], [] # If a file hasn't been recieved neither dropdown has any options

@app.callback(
    Output(component_id = "Mygraph" , component_property = 'figure'),
    [Input("x_feature", component_property = "value"), Input("y_feature", component_property = "value")]
)
def displayChoice(value1, value2):
    global df
    if(value1 and value2):
        myfig = px.scatter(df, x=value1, y=value2) # This can be any plotly graph
        return myfig
    else:
        return px.scatter() # Return an empty graph if no features have been selected

    
if __name__ == "__main__":
    app.run_server(debug=True)
