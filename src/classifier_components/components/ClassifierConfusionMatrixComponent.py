from classifier_components.ClassifierComponent import ClassifierComponent
from dash import dcc
import plotly.graph_objs as go
import sklearn.metrics as metrics

"""
AUTHOR: Dominic Cripps
DATE CREATED: 20/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 20/02/2023

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
        confusion_matrix = metrics.confusion_matrix(trueY, predY)
    
        layout = {
        "xaxis": {"title": "Predicted value"}, 
        "yaxis": {"title": "Real value"}
        }
        
        fig = go.Figure(data=go.Heatmap(z=confusion_matrix,
                                    x=dataLabels,
                                    y=dataLabels,
                                    hoverongaps=False),
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
        self.componentChildren = self.matrix