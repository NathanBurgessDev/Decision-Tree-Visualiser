from dash.dependencies import Input, Output
from classifier_components.ClassifierComponentFactory import ClassifierComponentFactory
from UserSession import UserSession
from AppInstance import AppInstance
from flask import request

"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

Callback is triggered when the value of the 'trained-models'
dropdown is changed, this indicates the user has selected a new
model or trained a new model.

Callback output is the children of the html div 'model-components'

The function 'modelSelected' takes the selected model name, finds the corresponding
model data from 'models' in class 'SettingCallbacks'. It will then get the type
of classifier used to train the model.

It will pass the classifier type into the class 'ClassifierComponentFactory' to 
generate the necessary model components. e.g. info, tree, boundary etc.

"""
app = AppInstance().instance.app
@app.callback(
    [Output(component_id="model-components", component_property="children")],
    [Input("trained-models", component_property="value")],
    
)
def modelSelected(modelFilename):
    classifierComponents = [()]
    if(modelFilename):
        modelInfo = UserSession().instance.modelInformation[str(request.remote_addr)][modelFilename]
        classifierComponents = ClassifierComponentFactory.Factory(modelInfo)
        UserSession().instance.selectedModel[str(request.remote_addr)] = modelInfo["modelData"]
        
    return classifierComponents