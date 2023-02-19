from classifier_components.components.ClassifierInfoComponent import ClassifierInfoComponent
from classifier_components.ClassifierComponent import ClassifierComponent
from classifier_components.components.ClassifierTreeComponent import ClassifierTreeComponent
from classifier_components.components.ClassifierClassSplitComponent import ClassifierClassSplitComponent
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

    def Factory(modelInfo):
        components = {
            "DecisionTreeClassifier" : 
                                        [
                                            [ClassifierInfoComponent(modelInfo), ClassifierClassSplitComponent(modelInfo)],
                                            [ClassifierTreeComponent(modelInfo)],
                                        ],
            "GradientBoostingClassifier" : 
                                        [
                                            [ClassifierInfoComponent(modelInfo)],
                                            [ClassifierTreeComponent(modelInfo)]
                                        ],
            None : [ClassifierComponent()]
        }
        # For each 'ClassifierComponent' in components[classType] it will create an 
        # object of that component, the property 'componentLayout' of which
        # will be used to create an array in the structure of an html div child.
        # Return this array.
        rows = []
        for x in components[modelInfo["classifierType"]]:
            split = str(100 / len(x)) + "%"

            children = []
            for i in range (0, len(x)):
                modelComponent = x[i]
                if i + 1 == len(x):
                    compMargin = "4%"
                else:
                    margin = 4 / (len(x) - 1)
                    compMargin = str(margin) + "%"

                titleDiv = html.Div(children = modelComponent.componentTitle, className = "componentTitle")
                layout = html.Div(children = [titleDiv, modelComponent.componentChildren], className="classifierComponent")
                children.append(html.Div(children = layout, style = {"width" : split, "margin-right" : compMargin}))
            row = html.Div(children = children, className="classifierComponentRow")
            rows.append(row)
        return [rows]