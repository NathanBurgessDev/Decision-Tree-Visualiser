from dash import html, dcc
import dash_daq as daq
from model_settings.ClassifierSettings import ClassifierSettings
from sklearn.tree import DecisionTreeClassifier


class DecisionTreeClassifierSettings(ClassifierSettings):


    def __init__(self):

        self.parameters = [
            "criterion",
            "splitter",
            "max_depth",
            "min_samples_split",
            "min_samples_leaf",
            "max_features",
            "random_state",
            "max_leaf_nodes",
            "min_impurity_decrease",
        ]

        self.classifier = DecisionTreeClassifier

        self.classifierLayout = [html.Div(id = "decision-tree-classifier", children=[
            html.Div(id="hidden-div", style={"display": "none"}),
            html.H4("Decision Tree Params", style = {"border-top" : "2px solid rgb(200,200,200)", "padding" : "4px", "padding-top" : "10px"}),

            html.H4("Criterion"),
            dcc.Dropdown(
                id=dict(name="classifier-settings", idx="criterion"), 
                options = ["gini", "entropy", "log_loss"], 
                value = "gini",
                className="dropdown"
            ),
                            
            html.H4("Splitter"),
            dcc.Dropdown(
                id=dict(name="classifier-settings", idx="splitter"), 
                options = ["best", "random"], 
                value = "best",
                className="dropdown"
            ),
            
            html.H4("Max Depth"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="max_depth"), 
                min=1,
                value=5,
                className="numericInput"
            ),

            html.H4("Minimum Sample Split"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="min_samples_split"), 
                min=1,
                value=2,
                className="numericInput"
            ),

            html.H4("Minimum Sample Leaf"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="min_samples_leaf"), 
                min=1,
                value=1,
                className="numericInput"
            ),

            html.H4("Max Features To Split"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="max_features"), 
                min=1,
                value=1,
                className="numericInput"
            ),

            html.H4("Random State"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="random_state"), 
                min=0,
                value=0,
                className="numericInput"
            ),

            html.H4("Maximum Leaf Nodes"),
            daq.NumericInput(
                id=dict(name="classifier-settings", idx="max_leaf_nodes"), 
                min=2,
                value=10,
                className="numericInput"
            ),

            html.H4("Minimum Impurity Decrease"),
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
        ])]

        
