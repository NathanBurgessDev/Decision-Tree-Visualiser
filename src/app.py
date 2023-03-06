import dash
from utils.PageLayout import PageLayout
from callbacks.SystemCallbacks import get_system_callbacks
# from DashInstance import dash_app

"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

--THE MAIN FILE TO RUN--

Get a reference to the app instance from 'DashInstance' it will
then use the class 'PageLayout' to update the app layout and
run it.
"""

dash_app = dash.Dash(__name__, suppress_callback_exceptions=True)
get_system_callbacks(dash_app)
app = dash_app.server

pageLayout = PageLayout("Results visualisation", dash_app)

if __name__ == "__main__":
    pageLayout.runServer(True)
