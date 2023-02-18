import dash
from callbacks.SystemCallbacks import get_system_callbacks

"""
AUTHOR: Alfred Greenwood
DATE CREATED: 14/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

In order to seperate callbacks into multiple files for organisational 
purposes without circular dependencies this file creates the initial app 
'app', and once it is created it will pass the instance of the app to all 
files containing callbacks using the function 'get_system_callbacks' from 
class SystemCallbacks 
"""

app = dash.Dash(__name__)
get_system_callbacks(app)

    