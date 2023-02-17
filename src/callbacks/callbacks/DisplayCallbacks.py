from dash.dependencies import Input, Output, State, MATCH, ALL
import html
import utils.ComponentUtil as cu
from callbacks.callbacks.SettingCallbacks import modelFilenames, models
from classifier_components.ClassifierComponentFactory import ClassifierComponentFactory


def get_callbacks(app):

    @app.callback(
        [Output(component_id="model-components", component_property="children")],
        [Input("trained-models", component_property="value")]
    )
    def modelSelected(modelFilename):
        classifierComponents = []
        print("here")
        if(modelFilename):
            modelIndex = modelFilenames.index(modelFilename)
            modelData = models[modelIndex]
            classType = str(type(modelData)).replace('>', '').replace("'", '').split('.')
            classType = classType[len(classType) - 1]
            classifierComponents = ClassifierComponentFactory.Factory(modelData, classType, modelFilename)
            
        return classifierComponents