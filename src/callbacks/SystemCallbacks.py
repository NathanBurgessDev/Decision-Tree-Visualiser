from callbacks.callbacks.SettingCallbacks import get_callbacks as get_setting_callbacks
from callbacks.callbacks.DisplayCallbacks import get_callbacks as get_display_callbacks


def get_system_callbacks(app):
    get_setting_callbacks(app)
    get_display_callbacks(app)