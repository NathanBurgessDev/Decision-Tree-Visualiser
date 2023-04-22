from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dash_mantine_components as dmc
from dash import dcc
import numpy as np
import plotly.graph_objects as go

"""
AUTHOR: Ethan Temple-Betts
DATE CREATED: 22/02/2023
PREVIOUS MAINTAINER: Ethan Temple-Betts
DATE LAST MODIFIED: 04/03/2023

This class will create a parallel coordinates plot
using the testing data for the model. The colour of the lines
represents the predeicted classification.

Inputs
dict modelInfo :    {"modelData" : model, 
                    "trainingData" : [xTrain, yTrain],
                    "testingData" : [xTest, yTest],
                    "modelArguments" : arguments, 
                    "testTrainSplit" : split, 
                    "classifierType" : classType,
                    "modelName" : str(filename)}

"""
class ClassifierParallelCoordinatesComponent(ClassifierComponent):

    def __init__(self, modelInfo):

        # Extract xTest data, yTest data and the model
        xTest = modelInfo["testingData"][0]
        yTest = modelInfo["testingData"][1]
        model = modelInfo['modelData']

        # Predict the classes of xTest data and store result in
        # pred dataframe
        predictions = model.predict(xTest)
        yTestDF = yTest.to_frame()
        classifier = yTestDF.columns[0]
        pred = pd.DataFrame() 
        pred[classifier] = predictions

        # Add the true class and predicted class data
        # to the xTest data frame
        xTest["True Class"] = yTestDF[classifier].values
        classes = (np.unique(pred[classifier])).tolist()
        mapping = self.createClassMap(classes)
        pred[classifier] = pred[classifier].map(mapping)
        xTest[classifier] = pred[classifier].values

        # Map the true classes -> ints and store these
        # values in a 'dummy' column in xTest
        dfg = pd.DataFrame({"True Class":xTest["True Class"].unique()})
        dfg['dummy'] = dfg.index
        xTest = pd.merge(xTest, dfg, on = "True Class", how='left')

        # Create an array of feature names and remove
        # the true class, dummy and predicted columns
        features = xTest.columns.values.tolist()
        features.remove("True Class")
        features.remove('dummy')
        features.remove(classifier)

        # Create dimensions for the remaining features
        dimensions = self.createPlotDimensions(features, xTest)
        dropDownOrder = self.orderByCorrelation(features, xTest)

        # Order the dimensions based on correlation
        dimensions = self.orderDimensions(dimensions, dropDownOrder)

        # Create the 'True Class' dimension and plot data using
        # dummy values and label the axis with the true class
        dim = dict(range=[0, xTest['dummy'].max()],
                tickvals = dfg['dummy'], ticktext = dfg["True Class"],
                label="True Class", values=xTest['dummy'])
        dimensions.append(dim)

        # Create the plot and color using predicted class
        fig = go.Figure(data=go.Parcoords(
            line = dict(color = xTest[classifier],
                        colorscale = 'sunset'),
            dimensions=dimensions))
        
        # Customise the colours of the plot
        fig.update_layout(
            paper_bgcolor="#232323",
            font_color = "#f5f5f5",
            plot_bgcolor="#232323")

        self.componentTitle = html.Span(
            dmc.Tooltip(
                label = html.Div(children = [
                    html.Img(src='../../assets/parallelCoordinatesDemo.gif'),
                    html.P("Use the feature dropdown box to select a feature."),
                    html.P("The buttons either side can be used to add or remove this feature from the visualisation."),
                    html.P("Features are ordered based on their correlation to make the graph easier to interpret, "),
                    html.P("but you can drag them to any position you require."),
                    html.P("You can select sections of the feature space as demonstrated above."),
                    html.P("The colour of the lines reflects the classification predicted by the model, "),
                    html.P("and the 'true class' represents the true value of that data instance."),
                    html.P("This visualisation uses the models testing data.")
                    ]),
                children=[html.P("Parallel Coordinates")],
                id="pc-tooltip",
                className ="plotToolTip",
                withArrow = True,
            ))

        # Update the componentChildren property to be a html div
        # containing a seperate div for dimension controls;
        # div[('-' button), (feature dropdown), ('+' button)]
        # and below this the parallel coordinates plot
        self.componentChildren = html.Div(children = [
            html.Div(children=[
                html.Button(
                "-",
                id="pc_del_dim",
                className="pcButton"),

                dcc.Dropdown(
                options=dropDownOrder,
                value = dropDownOrder[0],
                id='pc_dim_select',
                className = "pcDimDropdown"),

                html.Button(
                "+",
                id="pc_add_dim",
                className="pcButton")],

            className = "pcControlContainer"),
                
            dcc.Graph(
            figure = fig,
            id="pc_plot")])
    
    ''' 
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Create a dictionary, which maps class names -> ints

    Inputs:
    list classes[str or int] : a list of unique class names

    Returns:
    dict mapping : A dictionary mapping class names -> int
    
    '''
    def createClassMap(self, classes):
        mapping = {}
        count = 0
        val = list(range(len(classes)))
        for c in classes:
            mapping[c] = val[count]
            count+=1

        return mapping
    

    ''' 
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Create a list, which contains valid paracoord dimensions

    Inputs:
    list[str] features : a list of feature names in data to be
    made into dimensions

    dataframe data : A dataframe containing the data to be
    plotted 

    Returns:
    list[dict] dimensions : Valid paracoord dimensions
    '''
    def createPlotDimensions(self, features, data):
        dimensions = []
        for i in features:
            dim = dict(range=[data[i].min(),data[i].max()],
                    label=i,
                    values=data[i],
                    visible=False)
            
            dimensions.append(dim)

        return dimensions
    

    ''' 
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Orders the features based on the next most correlated feature
    starting from features[0]. It doesn't calculate the optimal
    order but instead calculates the feature most correlated to
    its predecessor that has not already been placed in the list.

    Inputs:
    list[str] features : a list of feature names in data to be
    ordered

    dataframe data : A dataframe containing the data to be
    checked for correlation

    Returns:
    list[str] ordered : the features input in order of correlation
    '''
    def orderByCorrelation(self, features, data):
        ordered = [features[0]]

        for i in features:
            index = -1
            # Corelation is measured between -1..1
            # so a value of -2 ensures a feature is always chossen
            correlation = -2 

            for j in features:
                c = -2

                if(j not in ordered):
                    c = data[i].corr(data[j])

                if(c > correlation):
                    index = features.index(j)

            if(index != -1):
             ordered.append(features[index])

        return ordered
    

    ''' 
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Orders a list of paracoord dimensions based on the order
    that the feature names appear in the order list.

    Inputs:
    list[dict] dimensions : a list of paracoord dimensions

    list[str] order : A list of feature names, used in the
    dimensions array, that are ordered by correlation

    Returns:
    list[dict] dims : A list of paracoord dimensions in the order
    specified
    '''    
    def orderDimensions(self, dimensions, order):
        dims = []
        c = 0

        for c in range(len(dimensions)):
            for i in dimensions:
                if i['label'] == order[c]:
                    dims.append(i)
        
        return dims


            
                




    