from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html

class ClassifierInfoComponent(ClassifierComponent):

    def __init__(self, model, classType, modelFilename):
        modelInfo = [
            "Model Class : ", html.Br(), classType, html.Br(), html.Br(),
            "Filename : ", html.Br(), modelFilename, html.Br(), html.Br(), 
            "Features : ", html.Br()]

        for x in model.feature_names_in_:
            modelInfo.append(str(x))
            modelInfo.append(", ")
        modelInfo.pop(len(modelInfo) - 1)

        modelInfo += [html.Br(), html.Br(), "Classes : ", html.Br()]

        for x in model.classes_:
            modelInfo.append(str(x))
            modelInfo.append(", ")
        modelInfo.pop(len(modelInfo) - 1)

        modelInfo.append(html.Br())

        self.componentLayout = html.Div(id = "model-info-component", children = html.P(modelInfo), className = "classifierComponent") 
