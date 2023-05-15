from classifier_components.ClassifierComponent import ClassifierComponent
from dash import dcc
import plotly.graph_objs as go
import sklearn.metrics as metrics
import numpy as np
from dash import html
from utils.ToolTipUtil import ToolTip

"""
AUTHOR: Dominic Cripps
DATE CREATED: 20/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 1/03/2023

Child of 'ClassifierComponent' this class defines 
an appropriate 'componentLayout' to represent a confusion
matrix, comparing True classifications to predicted 
classifications.

"""
class ClassifierConfusionMatrixComponent(ClassifierComponent):

    def __init__(self, modelInfo):
        
        testingData = modelInfo["testingData"]
        predY = modelInfo["modelData"].predict(testingData[0])
        trueY = testingData[1]
        dataLabels = modelInfo["modelData"].classes_
        confusion_matrix = metrics.confusion_matrix(predY, trueY, labels=np.flip(dataLabels, 0))
    
        layout = {
        "xaxis": {"title": "Predicted value"}, 
        "yaxis": {"title": "Real value"}
        }
        
        fig = go.Figure(data=go.Heatmap(z=np.flip(confusion_matrix, 0),
                                    x=dataLabels,
                                    y=np.flip(dataLabels, 0),
                                    texttemplate="%{text}",
                                    textfont={"size": 16},
                                    hoverongaps=False,
                                    text=np.flip(confusion_matrix, 0)),
                    layout=layout)
        
        fig.update_layout(
            {
            "plot_bgcolor" : "#232323",
            "paper_bgcolor" : "#232323",
            "font_color" : "#f5f5f5",
            }
        )
        
        graph = go.Figure(data=fig)
        graph.update_layout(
            autosize=True, 
            margin={'t': 60,'l':20,'b':5,'r':20}, 
            paper_bgcolor="#232323"
        )
        self.matrix = dcc.Graph(figure = graph)

        self.componentTitle = "Confusion Matrix"
        self.componentChildren = html.Div(id = "confusion-matrix-component", children = [
            self.matrix,
            ToolTip().generateToolTip("confusion-matrix-component", "Confusion Matrix", "A more in-depth visualisation of model performance. It compares the true values of each samples classification to values predicted by the model itself. A bright diagonal from the top left to the bottom right is an indication of an accurate model.")] )