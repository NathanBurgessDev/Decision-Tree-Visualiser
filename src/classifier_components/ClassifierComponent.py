from dash import html


"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

Parent class of all classifier components. 
As a result all classifier components e.g. "ClassifierInfoComponent"
will have attribute :
componentLayout : html structure of the settings

"""
class ClassifierComponent():

    def __init__(self):
        self.componentChildren = [] 
        self.componentTitle = ""