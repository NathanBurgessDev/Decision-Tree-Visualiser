from dash import html


"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 19/02/2023

Parent class of all classifier components. 
As a result all classifier components e.g. "ClassifierInfoComponent"
will have attribute :
componentLayout : Contents of the component
componentTitle : A label that will be displayed along side the component.

"""
class ClassifierComponent():

    def __init__(self):
        self.componentChildren = [] 
        self.componentTitle = ""