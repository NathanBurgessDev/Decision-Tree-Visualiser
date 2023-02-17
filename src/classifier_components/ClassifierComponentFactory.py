from classifier_components.components.ClassifierInfoComponent import ClassifierInfoComponent
from classifier_components.ClassifierComponent import ClassifierComponent
from dash import html

class ClassifierComponentFactory():

    def Factory(model, classType, filename):
        components = {
            "DecisionTreeClassifier" : [ClassifierInfoComponent(model, classType, filename), ClassifierInfoComponent(model, classType, filename)],
            "GradientBoostingClassifier" : [ClassifierInfoComponent(model, classType, filename)],
            None : [ClassifierComponent()]
        }
        return [html.Div([component.componentLayout for component in components[classType]])]