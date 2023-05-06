from dash import html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
from model_settings.ModelSettings import ClassifierSettings
from sklearn.svm import SVC
import dash_mantine_components as dmc
from utils.ToolTipUtil import ToolTip

"""
AUTHOR: Dominic Cripps
DATE CREATED: 22/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 22/02/2023

Child of 'ClassifierSettings' this class defines 
its attributes to be appropriate for the SVMClassifier

"""
class SVMClassifierSettings(ClassifierSettings):

    def __init__(self):
        
        # Array of supported parameters
        self.parameters = [
            "C",
            "kernel",
            "degree",
            "gamma",
            "coef0",
            "shrinking",
            "probability",
            "tol",
            "cache_size",
            "verbose",
            "max_iter",
            "decision_function_shape",          
            "break_ties",
            "random_state",  
        ]

        # Class Reference To Classifier Type
        self.classifier = SVC

        # HTML structure for classifier specific settings
        self.classifierLayout = [html.Div(id = "svm-classifier", children=[
            html.Div(id="hidden-div", style={"display": "none"}),
            html.H4("SVM Params", style = {"border-top" : "2px solid rgb(200,200,200)", "padding" : "4px", "padding-top" : "10px"}),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="C"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "C",
                              className = "paramCheckbox"),
            dbc.Input(
                id=dict(name="classifier-settings", idx="C"), 
                type = "number",
                min=0.0,
                value=1,
                step = 0.1,
                className="floatInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="C"), "C", self.C),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="kernel"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Kernel",
                              className = "paramCheckbox"),
            dcc.Dropdown(
                id=dict(name="classifier-settings", idx="kernel"), 
                options = ["linear", "poly", "rbf", "sigmoid", "precomputed"], 
                value = "rbf",
                className="dropdown"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="kernel"), "Kernel", self.kernel),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="degree"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Degree",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="degree"), 
                min=0,
                value=3,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="degree"), "Degree", self.degree),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="gamma"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Gamma",
                              className = "paramCheckbox"),
            dcc.Dropdown(
                id=dict(name="classifier-settings", idx="gamma"), 
                options = ["scale", "auto"], 
                value = "scale",
                className="dropdown"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="gamma"), "Gamma", self.gamma),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="coef0"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Coefficient 0",
                              className = "paramCheckbox"),
            dbc.Input(
                id=dict(name="classifier-settings", idx="coef0"), 
                type = "number",
                min=0.0,
                value=1,
                step = 0.1,
                className="floatInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="coef0"), "Coef0", self.coef0),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="shrinking"),
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Shrinking",
                              className = "paramCheckbox"),
            dcc.Dropdown(
                id=dict(name="classifier-settings", idx="shrinking"), 
                options = [True, False], 
                value = True,
                className="dropdown"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="shrinking"), "Shrinking", self.shrinking),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="probability"),
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Probability",
                              className = "paramCheckbox"),
            dcc.Dropdown(
                id=dict(name="classifier-settings", idx="probability"), 
                options = [True, False], 
                value = True,
                className="dropdown"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="probability"), "Probability", self.probability),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="tol"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Tolerance",
                              className = "paramCheckbox"),
            dbc.Input(
                id=dict(name="classifier-settings", idx="tol"), 
                type = "number",
                min=0.01,
                value=0.01,
                step = 0.01,
                className="floatInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="tol"), "Tolerance", self.tol),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="cache_size"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Cache Size",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="cache_size"), 
                min=0,
                value=200,
                max = 300,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="cache_size"), "Cache Size", self.cache_size),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="verbose"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Verbose",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="verbose"), 
                min=0,
                value=0,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="verbose"), "Verbose", self.verbose),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="max_iter"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Max Iterations",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="max_iter"), 
                min=-1,
                value=-1,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="max_iter"), "Max Iterations", self.max_iter),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="decision_function_shape"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Decision Function Shape",
                              className = "paramCheckbox"),
            dcc.Dropdown(
                id=dict(name="classifier-settings", idx="decision_function_shape"), 
                options = ["ovo", "ovr"], 
                value = "ovr",
                className="dropdown"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="decision_function_shape"), "Decision Function Shape", self.decision_function_shape),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="break_ties"),
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Break Ties",
                              className = "paramCheckbox"),
            dcc.Dropdown(
                id=dict(name="classifier-settings", idx="break_ties"), 
                options = [True, False], 
                value = False,
                className="dropdown"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="break_ties"), "Break Ties", self.break_ties),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="random_state"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Random State",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="random_state"), 
                min=0,
                value=0,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="random_state"), "Random State", self.random_state),

        ])]

        
