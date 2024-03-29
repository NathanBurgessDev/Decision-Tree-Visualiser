from dash import html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
from model_settings.ModelSettings import ClassifierSettings
from sklearn.ensemble import GradientBoostingClassifier
import dash_mantine_components as dmc
from utils.ToolTipUtil import ToolTip

"""
AUTHOR: Dominic Cripps
DATE CREATED: 22/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 22/02/2023

Child of 'ClassifierSettings' this class defines 
its attributes to be appropriate for the GradientBoostingClassifier

"""
class GradientBoostingClassifierSettings(ClassifierSettings):

    def __init__(self):
        
        # Array of supported parameters
        self.parameters = [
            "loss",
            "learning_rate",
            "n_estimators",
            "subsample",
            "criterion",
            "min_samples_split",
            "min_samples_leaf",
            "min_weight_fraction_leaf",
            "max_depth",
            "min_impurity_decrease",
            "random_state",
            "max_features",
            "max_leaf_nodes",
            "validation_fraction",
            "n_iter_no_change",
            "tol",
        ]

        # Class Reference To Classifier Type
        self.classifier = GradientBoostingClassifier

        # HTML structure for classifier specific settings
        self.classifierLayout = [html.Div(id = "gradient-boosting-classifier", children=[
            html.Div(id="hidden-div", style={"display": "none"}),
            html.H4("Gradient Boosting Params", style = {"border-top" : "2px solid rgb(200,200,200)", "padding" : "4px", "padding-top" : "10px"}),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="loss"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Loss",
                              className = "paramCheckbox"),
            dcc.Dropdown(
                id=dict(name="classifier-settings", idx="loss"), 
                options = ["log_loss", "deviance", "exponential"], 
                value = "log_loss",
                className="dropdown"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="loss"), "Loss", self.loss),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="learning_rate"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Learning Rate",
                              className = "paramCheckbox"),
            dbc.Input(
                id=dict(name="classifier-settings", idx="learning_rate"), 
                type = "number",
                min=0.0,
                value=0.1,
                step = 0.1,
                className="floatInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="learning_rate"), "Learning Rate", self.learning_rate),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="n_estimators"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "N Estimators",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="n_estimators"), 
                min=1,
                value=100,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="n_estimators"), "N Estimators", self.n_estimators),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="subsample"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Subsample",
                              className = "paramCheckbox"),
            dcc.Slider(
                id=dict(name="classifier-settings", idx="subsample"), 
                min = 0.0,
                max = 1.0,
                step = 0.05,
                value = 1.0,
                marks = {
                    0 : {"label": "0"},
                    0.25 : {"label": "0.25"},
                    0.5 : {"label": "0.5"},
                    0.75 : {"label": "0.75"},
                    1 : {"label": "1"}
                },
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="subsample"), "Subsample", self.subsample),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="criterion"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Criterion",
                              className = "paramCheckbox"),
            dcc.Dropdown(
                id=dict(name="classifier-settings", idx="criterion"), 
                options = ["friedman_mse", "squared_error"], 
                value = "friedman_mse",
                className="dropdown"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="criterion"), "Criterion", self.criterion),

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

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="validation_fraction"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "Validation Fraction",
                              className = "paramCheckbox"),
            dcc.Slider(
                id=dict(name="classifier-settings", idx="validation_fraction"), 
                min = 0.0,
                max = 1.0,
                step = 0.05,
                value = 0.1,
                marks = {
                    0 : {"label": "0"},
                    0.25 : {"label": "0.25"},
                    0.5 : {"label": "0.5"},
                    0.75 : {"label": "0.75"},
                    1 : {"label": "1"}
                },
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="validation_fraction"), "Validation Fraction", self.validation_fraction),

            dmc.Checkbox(id = dict(name="classifier-settings-custom", idx="n_iter_no_change"), 
                              checked=False,
                              size = "xs",
                              color = "violet",
                              label = "N Iter No Change",
                              className = "paramCheckbox"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="n_iter_no_change"), 
                min=1,
                value=None,
                className="numericInput"
            ),
            ToolTip().generateToolTip(dict(name="classifier-settings-custom", idx="n_iter_no_change"), "N Iter No Change", self.n_iter_no_change),

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

        ])]

        
