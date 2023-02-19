from classifier_components.components.ClassifierInfoComponent import ClassifierInfoComponent
from classifier_components.ClassifierComponent import ClassifierComponent
from classifier_components.components.ClassifierTreeComponent import ClassifierTreeComponent
from classifier_components.components.ClassifierDecisionBoundaryComponent import ClassifierDecisionBoundaryComponent
from dash import html


"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

Using the factory method, this class will return the
correct child components determined by the classifier type.

"""
class ClassifierComponentFactory():

    def Factory(model, classType, filename, trainingData):
        components = {
            "DecisionTreeClassifier" : 
                                        [
                                            ClassifierInfoComponent(model, classType, filename), 
                                            ClassifierDecisionBoundaryComponent(model, trainingData),
                                            ClassifierTreeComponent(model)
                                        ],
            "GradientBoostingClassifier" : 
                                        [
                                            ClassifierInfoComponent(model, classType, filename),
                                            ClassifierTreeComponent(model)
                                        ],
            None : [ClassifierComponent()]
        }
        # For each 'ClassifierComponent' in components[classType] it will create an 
        # object of that component, the property 'componentLayout' of which
        # will be used to create an array in the structure of an html div child.
        # Return this array.
        return [html.Div([component.componentLayout for component in components[classType]])]