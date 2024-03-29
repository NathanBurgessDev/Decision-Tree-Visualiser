from callbacks.callbacks.SettingCallbacks import get_callbacks as get_setting_callbacks
from callbacks.callbacks.DisplayCallbacks import get_callbacks as get_display_callbacks
from callbacks.callbacks.PredictCallbacks import get_callbacks as get_predict_callbacks
from callbacks.callbacks.BoundaryCallbacks import get_callbacks as get_boundary_callbacks

from callbacks.callbacks.ParallelCoordinatesCallbacks import get_callbacks as get_parallelCoordinates_callbacks

from callbacks.callbacks.TreeLoopCallbacks import get_callbacks as get_tree_callbacks


"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Ethan Temple-Betts
DATE LAST MODIFIED: 04/03/2023


This is necessary as getting a reference to the app
after the callbacks have been defined will hold a None
object as the app has not launched yet.

Function called by the class 'DashInstance' once the app
has been initialised, it passes a reference of the app to 
all files containing callbacks. 

To create a new file that contains callbacks : 
    - Create file with the structure

        def get_callbacks(app):
            @app.callback( ... )
            def exampleCallbackFunction():
        
            .
            .
            .
    
    - Import the get_callbacks function of this file and name it 
        something specific as I have done above.
    
    - Call the imported function and pass 'app' to it
"""


def get_system_callbacks(app):
    
    get_setting_callbacks(app)
    get_display_callbacks(app)
    get_predict_callbacks(app)
    get_parallelCoordinates_callbacks(app)
    get_tree_callbacks(app)
    get_boundary_callbacks(app)

    
