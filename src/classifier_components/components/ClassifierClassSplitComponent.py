from classifier_components.ClassifierComponent import ClassifierComponent
import plotly.graph_objects as go 
import plotly.express as px
from dash import dcc


"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Daniel Ferring
DATE LAST MODIFIED: 17/03/2023

Child of 'ClassifierComponent' this class defines 
an appropriate 'componentLayout' to represent the 
split between the classifications used to train the
model.

It does this in the form of a bar chart and can be used to
evaluate whether the training data was fair.

"""
class ClassifierClassSplitComponent(ClassifierComponent):
    
    def __init__(self, modelInfo):

        classifiers = modelInfo["trainingData"][1].to_frame()
        classInstances = classifiers.iloc[:, 0]

        colourKey = modelInfo["colourKey"]

        numInstances = []
        classNames = []
        classColours = []

        for key, value in colourKey.items():
            classNames.append(key)
            classColours.append(value)

            count = 0
            for instance in classInstances:
                if key == instance:
                    count += 1
            numInstances.append(count)

        fig = go.Bar(
            y = numInstances, 
            x = classNames,
            marker = dict(
                        color = classColours,
                        colorscale = 'sunset'
                        )
        )
        
        graph = go.Figure(data=fig)
        graph.update_layout(
            plot_bgcolor = '#232323',
            paper_bgcolor = '#232323',
            font_color = '#f5f5f5',
            autosize = True, 
            margin = {'t': 10,'l':10,'b':5,'r':10}
        )
        self.chart = dcc.Graph(figure = graph)

        self.componentTitle = "Training Data Class Split"

        self.componentChildren =self.chart
