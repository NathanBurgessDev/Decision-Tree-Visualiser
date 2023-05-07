import dash
from utils.PageLayout import PageLayout
from AppInstance import AppInstance
# from DashInstance import dash_app

"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Ethan Temple-Betts
DATE LAST MODIFIED: 23/03/2023

--THE MAIN FILE TO RUN--

Get a reference to the app instance from 'DashInstance' it will
then use the class 'PageLayout' to update the app layout and
run it.
"""

dash_app = dash.Dash(__name__, suppress_callback_exceptions=True)
app = dash_app.server
AppInstance().instance.app = dash_app
import callbacks.callbacks.DisplayCallbacks
import callbacks.callbacks.PredictCallbacks
import callbacks.callbacks.SettingCallbacks
import callbacks.callbacks.ParallelCoordinatesCallbacks
import callbacks.callbacks.TreeLoopCallbacks
import callbacks.callbacks.BoundaryCallbacks
import callbacks.callbacks.FeatureSpaceCallbacks


pageLayout = PageLayout("Results visualisation", dash_app)

if __name__ == "__main__":
    pageLayout.runServer(True)
