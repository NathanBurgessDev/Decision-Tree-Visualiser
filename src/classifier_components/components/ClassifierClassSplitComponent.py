from classifier_components.ClassifierComponent import ClassifierComponent
import plotly.graph_objects as go 
import plotly.express as px
from dash import dcc


"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

Child of 'ClassifierComponent' this class defines 
an appropriate 'componentLayout' to represent the 
split between the classifications used to train the
model.

It does this in the form of a pie chart and can be used to
evaluate whether the training data was fair.

"""
class ClassifierClassSplitComponent(ClassifierComponent):
    
    def __init__(self, modelInfo):

        classifiers = modelInfo["trainingData"][1].to_frame()
        
        values = []
        for value in classifiers.values:
            values.append(value[0])

        numVals = []
        for classification in modelInfo["modelData"].classes_:
            count = 0
            for val in values:
                if classification == val:
                    count += 1
            numVals.append(count)

        fig = px.pie(values = numVals, names = modelInfo["modelData"].classes_)
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
            margin={'t': 10,'l':10,'b':5,'r':10}, 
            paper_bgcolor="#232323"
        )
        self.chart = dcc.Graph(figure = graph)

        self.componentTitle = "Training Data Class Split"

        self.componentChildren =self.chart
