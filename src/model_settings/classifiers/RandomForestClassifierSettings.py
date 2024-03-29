from dash import html, dcc
import dash_daq as daq
from model_settings.ModelSettings import ClassifierSettings
from sklearn.ensemble import RandomForestClassifier
import dash_mantine_components as dmc
from utils.ToolTipUtil import ToolTip

"""
AUTHOR: Dominic Cripps
DATE CREATED: 22/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 22/02/2023

Child of 'ClassifierSettings' this class defines 
its attributes to be appropriate for the RandomForestClassifier

"""
class RandomForestClassifierSettings(ClassifierSettings):

    def __init__(self):
        
        # Array of supported parameters
        self.parameters = [
            "n_estimators",
            "criterion",
            "max_depth",
            "min_samples_split",
            "min_samples_leaf",
            "min_weight_fraction_leaf",
            "max_features",
            "max_leaf_nodes",
            "min_impurity_decrease",
            "bootstrap",
            "random_state",          
            "max_samples",
        ]

        # Class Reference To Classifier Type
        self.classifier = RandomForestClassifier

        # HTML structure for classifier specific settings
        self.classifierLayout = [html.Div(id = "random-forest-classifier", children=[
            html.Div(id="hidden-div", style={"display": "none"}),
            html.H4("Random Forest Params", style = {"border-top" : "2px solid rgb(200,200,200)", "padding" : "4px", "padding-top" : "10px"}),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="n_estimators"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Number Of Estimators",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="n_estimators"), 
                min=1,
                value=10,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="n_estimators"), "Number Estimators", self.n_estimators),


            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="criterion"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Criterion",
                              className = "paramCheckbox"),
            dcc.Dropdown(
                id=dict(name="classifier-settings", idx="criterion"), 
                options = ["gini", "entropy", "log_loss"], 
                value = "gini",
                className="dropdown"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="criterion"), "Criterion", self.criterion),


            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="max_depth"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Max Depth",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="max_depth"), 
                min=1,
                value=5,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="max_depth"), "Max Depth", self.max_depth),


            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="min_samples_split"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Min Sample Split",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="min_samples_split"), 
                min=2,
                value=2,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="min_samples_split"), "Min Samples Split", self.min_samples_split),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="min_samples_leaf"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Min Sample Leaf",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="min_samples_leaf"), 
                min=1,
                value=1,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="min_samples_leaf"), "Min Samples Leaf", self.min_samples_leaf),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="min_weight_fraction_leaf"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Min Weight Fraction Leaf",
                              className = "paramCheckbox"),
            dcc.Slider(
                id=dict(name="classifier-settings", idx="min_weight_fraction_leaf"), 
                min = 0.0,
                max = 0.5,
                step = 0.05,
                value = 0.0,
                marks = {
                    0 : {"label": "0"},
                    0.25 : {"label": "0.25"},
                    0.5 : {"label": "0.5"},
                    0.75 : {"label": "0.75"},
                    1 : {"label": "1"}
                },
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="min_weight_fraction_leaf"), "Min Weight Fraction Leaf", self.min_weight_fraction_leaf),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="max_features"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Max Features To Split",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="max_features"), 
                min=1,
                value=1,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="max_features"), "Max Features", self.max_features),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="max_leaf_nodes"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Maximum Leaf Nodes",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="max_leaf_nodes"), 
                min=2,
                value=10,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="max_leaf_nodes"), "Max Leaf Nodes", self.max_leaf_nodes),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="min_impurity_decrease"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Min Impurity Decrease",
                              className = "paramCheckbox"),
            dcc.Slider(
                id=dict(name="classifier-settings", idx="min_impurity_decrease"), 
                min = 0.0,
                max = 1,
                step = 0.05,
                value = 0.0,
                marks = {
                    0 : {"label": "0"},
                    0.25 : {"label": "0.25"},
                    0.5 : {"label": "0.5"},
                    0.75 : {"label": "0.75"},
                    1 : {"label": "1"}
                },
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="min_impurity_decrease"), "Min Impurity Decrease", self.min_impurity_decrease),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="bootstrap"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Bootstrap",
                              className = "paramCheckbox"),
            dcc.Dropdown(
                id=dict(name="classifier-settings", idx="bootstrap"), 
                options = [
                    {'label': 'True', 'value': True},
                    {'label': 'False', 'value': False}],
                value = True,
                className="dropdown"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="bootstrap"), "Bootstrap", self.bootstrap),

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

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="max_samples"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Max Samples",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="max_samples"), 
                min=0.01,
                max=1,
                value=0.2,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="max_samples"), "Max Samples", self.max_samples),

        ])]

        
