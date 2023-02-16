import dash
from layoutUtils import pageLayout as pl
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

if __name__ == "__main__":
    app = pl("Results visualisation")
    app.runServer(True)