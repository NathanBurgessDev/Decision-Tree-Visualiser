from dash import ctx
import dash
from dash.dependencies import Input, Output, State, ALL
from utils.Util import ImportUtil as ImportUtil
from model_settings.ModelSettingsFactory import ClassifierSettingsFactory
from sklearn.model_selection import train_test_split
from UserSession import UserSession
import pandas as pd
import numpy as np

df = []
selectedSettings = ClassifierSettingsFactory.Factory(None)
trainingData = []

def get_callbacks(app):

    """
    AUTHOR: Dominic Cripps
    DATE CREATED: 17/02/2023
    PREVIOUS MAINTAINER: Dominic Cripps
    DATE LAST MODIFIED: 18/02/2023

    Callback is triggered when the user has uploaded a file into 'upload-dataset'.

    Callback output will show appropriate error messages and update the 
    'classifer' and 'training-feature' checklists to contain the column titles 
    from the dataset.

    It will check for a correct file extension, and that the contents has been
    read properly.

    """
    @app.callback(
        [Output(component_id = "upload-df-alert", component_property="displayed"), 
        Output(component_id = "upload-df-alert", component_property = "message"),
        Output(component_id = "upload-dataset", component_property = "children"),
        Output(component_id = "training-features", component_property = "options"),
        Output(component_id = "classifier", component_property = "options"),
        Output(component_id = "training-features", component_property = "value"),
        Output(component_id = "classifier", component_property = "value")],
        [Input("upload-dataset", "filename"), Input("upload-dataset", "contents")]
    )
    def readDataframe(filename, contents):
        defaultUploadMessage = "Drag and drop or click to upload a dataset (.csv) "

        if(contents):
            if(str(filename[0]).endswith(".csv")):
                df.insert(0, ImportUtil.csvToDataFrame(ImportUtil.readContent(filename, contents[0])))
                return False, "", str(filename[0]), df[0].columns, df[0].columns, [], []
            else:
                return True, "Wrong File Type!", defaultUploadMessage, [], [], [], []
        else:
            return False, "No Contents!", defaultUploadMessage, [], [], [], []



    """
    AUTHOR: Dominic Cripps
    DATE CREATED: 17/02/2023
    PREVIOUS MAINTAINER: Dominic Cripps
    DATE LAST MODIFIED: 18/02/2023

    Callback is triggered when the user selected a training classifer.

    Callback output will set the children of 'classifier-settings' to be 
    appropriate html elements, each representing a parameter that could be 
    used to train the selected classifier.

    It will use the 'ClassifierSettingsFactory' to generate and return the 
    appropriate settings.

    """
    @app.callback(
            [Output(component_id="classifier-settings", component_property="children")],
            [Input("training-class", "value")]
    )
    def updateClassifierSettings(classifier):
        global selectedSettings
        selectedSettings = ClassifierSettingsFactory.Factory(classifier)
        settings = selectedSettings.classifierLayout

        return settings



    """
    AUTHOR: Dominic Cripps
    DATE CREATED: 17/02/2023
    PREVIOUS MAINTAINER: Daniel Ferring
    DATE LAST MODIFIED: 16/03/2023

    Callback is triggered when the user presses the train button.

    Callback output will show appropriate error alerts, and will update
    the dropdown component 'trained-models' options and current value if
    successfully trained.
    (Note : the update to 'trained-models' value will trigger the callback
    to display the model)

    Inputs : The value of all setting components

    It performs sanity checks using the selected settings, if it passes them
    all it will create the appropriate dataframes, train the data and fit 
    a model with all classifier specific settings as arguments.
    """
    @app.callback(
        [Output(component_id="training-alert", component_property="displayed"), 
        Output(component_id = "training-alert", component_property = "message"),
        Output(component_id = "trained-models", component_property="options"),
        Output(component_id = "trained-models", component_property="value")],
        [
        Input("train-button", "n_clicks"), 
        State(dict(name="classifier-settings", idx=ALL), "value"),
        State(dict(name="classifier-settings-custom", idx=ALL), "checked"),
        State("training-features", "value"),
        State("classifier", "value"),
        State("test-train-split", "value"),
        State("training-filename", "value"),
        State("training-class", "value")
        ] 
    )
    def train(clicks, classifierSettings, customParameters, features, classifier, split, filename, modelClass):
        errorMessage = ""
        error = False

        modelFilenames = [modelName for modelName in UserSession().instance.modelInformation]
        if "train-button" == ctx.triggered_id:

            if(len(df) == 0):
                return False, "", modelFilenames, dash.no_update

            if(modelClass == None):
                errorMessage += " \n Error : You Must Select A Model Class"
                error = True

            if(len(classifier) == 0 or len(features) == 0):
                errorMessage += " \n Error : You Must Select At Least One Classifier And Feature"
                error = True 
                return error, errorMessage, modelFilenames, dash.no_update

            if(len(classifier) > 1):
                errorMessage += " \n Error : You Cannot Select More Than One Classifier"
                error = True

            for x in features:
                if x in classifier:
                    errorMessage += " \n Error : The Classifier Cannot Be Used To Train The Model"
                    error = True

            if(filename == None):
                errorMessage += " \n Error : You Need To Provide A Filename"
                error = True
                return error, errorMessage, modelFilenames, dash.no_update
            

            '''
            if(isinstance(df[0][classifier[0]][0], float)):
                errorMessage += " \n We Do Not Currently Support Regression Problems, Use A Categorical or Integer Feature As The Classifier To Create A Classification Problem "
                error = True

            if(len(np.unique(df[0][classifier[0]])) > 50):
                errorMessage += " \n We Do Not Support The Training Of A Model With More Than 50 Classes"
                error = True
            '''

            if error == False:
                dfIn = pd.get_dummies(df[0].drop(df[0].columns.difference(features), axis = 1))
                dfOut = df[0][str(classifier[0])]
                xTrain, xTest, yTrain, yTest = train_test_split(dfIn, dfOut, test_size = split)
                
                arguments = {}
                for i in range (0, len(classifierSettings)):
                    if customParameters[i] == True:
                        if classifierSettings[i] != None:
                            arguments[selectedSettings.parameters[i]] = classifierSettings[i] 
                        else:
                            errorMessage += " \n Error : A Selected Parameter Has No Value"
                            error = True
                            return error, errorMessage, modelFilenames, dash.no_update


                model = selectedSettings.classifier(**arguments).fit(xTrain, yTrain)

                classType = str(type(model)).replace('>', '').replace("'", '').split('.')
                classType = classType[len(classType) - 1]

                #Dictionaries used to map class names to colours and shapes
                colourKey = {}
                shapeKey = {}

                #determines the colour of the class
                id = 0

                #used to select shapes from the plotly library
                symbolIndex = 0
                symbols = [0, 1, 2, 3, 4, 5, 13, 15, 17, 18, 19, 22]

                #Creates an entry in both dictionaries for each class, assigning a unique value for both
                for i in model.classes_:
                    colourKey[str(i)] = id
                    shapeKey[str(i)] = symbols[symbolIndex]
                    id += 1
                    symbolIndex += 1
                    if symbolIndex > 11:
                        symbolIndex = 0

                # The information that will be stored in the 'UserSession' singleton
                # this will be accessed when a model is selected, any information
                # needed for a classifier component should be stored here upon training.
                modelInfo = {
                    "modelData" : model, 
                    "trainingData" : [xTrain, yTrain],
                    "testingData" : [xTest, yTest],
                    "modelArguments" : arguments, 
                    "testTrainSplit" : split, 
                    "classifierType" : classType,
                    "modelName" : str(filename),
                    "selectedSettings" : selectedSettings,
                    "colourKey" : colourKey,
                    "shapeKey" : shapeKey
                    }

                UserSession().instance.modelInformation[str(filename)] = modelInfo

                modelFilenames = [modelName for modelName in UserSession().instance.modelInformation]

                return error, errorMessage, modelFilenames, filename
            
        return error, errorMessage, modelFilenames, dash.no_update
