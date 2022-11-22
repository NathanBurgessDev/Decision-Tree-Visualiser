import base64
import io
from io import StringIO
import pandas as pd
import plotly.express as px

"""
Contains functions that relate to the processsing of
data imports
"""
class ImportUtil:

    ### Converts base64 data to a string ###
    def readContent(file, content):
        content_type, content_string = content.split(',')
        contentBytes = base64.b64decode(content_string)
        stringContent = contentBytes.decode('utf-8')
        return stringContent

    ### Converts a string of csv data to a dataframe ###
    def csvToDataFrame(csv):
        data = StringIO(csv)
        df = pd.read_csv(data, sep=",")
        return df

"""
Contains functions that relate to the creation
of plotly scatter graphs
"""
class GraphUtil():

    ### Returns a 2d plotly scatter graph using the provided params ###
    def scatter2D(df, x, y, colour):
        if(colour == False):
            graph = px.scatter(df, x=x, y=y)
        else:
            graph = px.scatter(df, x=x, y=y, color=colour)
        return graph

    ### Returns a 3d plotly scatter graph using the provided params ###
    def scatter3D(df, x, y, z, colour):
        if(colour == False):
            graph = px.scatter_3d(df, x=x, y=y, z=z)
        else:
            graph = px.scatter_3d(df, x=x, y=y, z=z, color=colour)
        graph.update_traces(marker={'size': 4})
        return graph

    ### Returns a blank plottly scatter graph ###
    def getGraph():
        return px.scatter()

