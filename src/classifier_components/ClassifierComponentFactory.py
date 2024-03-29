from classifier_components.components.ClassifierEnsembleModelsComponent import ClassifierEnsembleModelsComponent
from classifier_components.components.ClassifierInfoComponent import ClassifierInfoComponent
from classifier_components.ClassifierComponent import ClassifierComponent
from classifier_components.components.ClassifierTreeComponent import ClassifierTreeComponent
from classifier_components.components.ClassifierClassSplitComponent import ClassifierClassSplitComponent
from classifier_components.components.ClassifierDecisionBoundaryComponent import ClassifierDecisionBoundaryComponent
from classifier_components.components.ClassifierConfusionMatrixComponent import ClassifierConfusionMatrixComponent
from classifier_components.components.ClassifierParallelCoordinatesComponent import ClassifierParallelCoordinatesComponent
from classifier_components.components.ClassifierUserInputComponent import ClassifierUserInputComponent
from classifier_components.components.ClassifierSVMDecisionBoundaryComponent import ClassifierSVMDecisionBoundaryComponent
from classifier_components.components.ClassifierFeatureSpaceComponent import ClassifierFeatureSpaceComponent
from dash import html


"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 19/02/2023

Using the factory method, this class will return the
correct child components determined by the classifier type.

"""
class ClassifierComponentFactory():

    def Factory(modelInfo, sessionID):

        # The value of each dictionary entry represents all rows containing components,
        # if you want multiple components on a row, place them within the same array as
        # shown below.
        components = {
            "DecisionTreeClassifier" : 
                                        [
                                            [ClassifierInfoComponent, ClassifierUserInputComponent],
                                            [ClassifierClassSplitComponent, ClassifierConfusionMatrixComponent],
                                            [ClassifierDecisionBoundaryComponent],
                                            [ClassifierTreeComponent],
                                            [ClassifierParallelCoordinatesComponent],
                                            [ClassifierFeatureSpaceComponent]
                                        ],
            "GradientBoostingClassifier" : 
                                        [
                                            [ClassifierInfoComponent, ClassifierUserInputComponent],
                                            [ClassifierClassSplitComponent, ClassifierConfusionMatrixComponent],
                                            [ClassifierEnsembleModelsComponent],
                                            [ClassifierParallelCoordinatesComponent],
                                            [ClassifierFeatureSpaceComponent]
                                        ],
            "RandomForestClassifier" : 
                                        [
                                            [ClassifierInfoComponent, ClassifierUserInputComponent],
                                            [ClassifierClassSplitComponent, ClassifierConfusionMatrixComponent],
                                            [ClassifierEnsembleModelsComponent],
                                            [ClassifierParallelCoordinatesComponent],
                                            [ClassifierFeatureSpaceComponent]
                                        ],
            "SVC":
                                        [
                                            [ClassifierInfoComponent, ClassifierUserInputComponent],
                                            [ClassifierClassSplitComponent, ClassifierConfusionMatrixComponent],
                                            [ClassifierSVMDecisionBoundaryComponent],
                                            [ClassifierParallelCoordinatesComponent],
                                            [ClassifierFeatureSpaceComponent]
                                        ], 
            "SVR":
                                        [
                                            [ClassifierInfoComponent],
                                            [ClassifierSVMDecisionBoundaryComponent],
                                            [ClassifierParallelCoordinatesComponent],
                                            [ClassifierFeatureSpaceComponent]
                                        ], 
                                                           
            None : [ClassifierComponent()]
        }
        # It will iterate through each row one component at a time, work out the correct 
        # margins in order to space the components correctly and will assign both the 
        # correct title and component layout to a 'ClasifierComponent' div.
        # Rows are then added to an array which is returned to be the child of
        # 'model-components' div.
        rows = []
        for x in components[modelInfo["classifierType"]]:
            split = str(100 / len(x)) + "%"

            children = []
            for i in range (0, len(x)):
                if x[i] == ClassifierTreeComponent or x[i] == ClassifierDecisionBoundaryComponent:
                    modelComponent = x[i](modelInfo, sessionID)
                else:
                    modelComponent = x[i](modelInfo)
                titleDiv = html.Div(children = modelComponent.componentTitle, className = "componentTitle")
                layout = html.Div(children = [titleDiv, modelComponent.componentChildren], className="classifierComponent")
                children.append(html.Div(children = layout, style = {"width" : split, "margin-right" : "25px", "overflow": "hidden", "position": "relative"}))
            row = html.Div(children = children, className="classifierComponentRow")
            rows.append(row)
        return [rows]