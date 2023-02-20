from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html

"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

Child of 'ClassifierComponent' this class defines 
an appropriate 'componentLayout' based on the model
selected. It will show information regarding the model:
    - Model Class
    - Filename
    - Features used to train the model
    - Possible classifications of data from the model

"""
class ClassifierInfoComponent(ClassifierComponent):
    
    def __init__(self, model, classType, modelFilename):
        # Define array containing initial model info formatted as an
        # html child component
        modelInfo = [
            "Model Class : ", html.Br(), classType, html.Br(), html.Br(),
            "Filename : ", html.Br(), modelFilename, html.Br(), html.Br(), 
            "Features : ", html.Br()]

        # Iterate through the models feature names and add them to modelData
        for x in model.feature_names_in_:
            modelInfo.append(str(x))
            modelInfo.append(", ")
        modelInfo.pop(len(modelInfo) - 1)

        modelInfo += [html.Br(), html.Br(), "Classes : ", html.Br()]

        # Iterate through the models classifications and add them to modelData
        for x in model.classes_:
            modelInfo.append(str(x))
            modelInfo.append(", ")
        modelInfo.pop(len(modelInfo) - 1)

        modelInfo.append(html.Br())

        # Set component layout property to be a div containing modelData
        # Important : className of this div must be "classifierComponent" to format correctly
        self.componentLayout = html.Div(id = "model-info-component", children = html.P(modelInfo), className = "classifierComponent") 
