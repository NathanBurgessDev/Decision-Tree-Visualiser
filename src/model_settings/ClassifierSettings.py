from dash import html

class ClassifierSettings():

    def __init__(self):
        self.classifierLayout = [html.Div(id = "empty-settings", children=[])]
        self.parameters = []
        self.classifier = None
