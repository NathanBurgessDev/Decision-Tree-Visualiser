import dash
from callbacks.SystemCallbacks import get_system_callbacks

app = dash.Dash(__name__)
get_system_callbacks(app)

    