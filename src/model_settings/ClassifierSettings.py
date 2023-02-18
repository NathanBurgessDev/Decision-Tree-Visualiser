from dash import html


"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

Parent class of all classifier specific settings. 
As a result all classifier settings e.g. "DecisionTreeClassifierSettings"
will have attributes :
classifierLayout : html structure of the settings
parameters : An array of all accepted parameters
classifier : A class reference to the correct classifier

"""
class ClassifierSettings():

    def __init__(self):
        self.classifierLayout = [html.Div(id = "empty-settings", children=[])]
        self.parameters = []
        self.classifier = None
