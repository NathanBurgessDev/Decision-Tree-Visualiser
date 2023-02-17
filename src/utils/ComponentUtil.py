import utils.TreeUtil as T
from dash import dcc
from igraph import Graph
from utils.Util import GraphUtil as gu
from dash import html
import utils.DecisionBoundaryUtil as dbu

class ComponentUtil():
    
    def generateModelInfo(self, model, classType, modelFilename):
        modelInfo = [
            "Model Class : ", html.Br(), classType, html.Br(), html.Br(),
            "Filename : ", html.Br(), modelFilename, html.Br(), html.Br(), 
            "Features : ", html.Br()]

        for x in model.feature_names_in_:
            modelInfo.append(str(x))
            modelInfo.append(", ")
        modelInfo.pop(len(modelInfo) - 1)

        modelInfo += [html.Br(), html.Br(), "Classes : ", html.Br()]

        for x in model.classes_:
            modelInfo.append(str(x))
            modelInfo.append(", ")
        modelInfo.pop(len(modelInfo) - 1)

        modelInfo.append(html.Br())
        return html.Div(id = "model-info-component",children = html.P(modelInfo))        


    def generateDecisionTree(self, model):
        tree = []
        tu = T.TreeUtil()
        tu.parseTree(model)
        graphComp = Graph(directed = "T")
        graphComp.add_vertices(tu.getVerticies())
        graphComp.add_edges(tu.getEdges())
        graphComp.vs["info"] = tu.getAnnotations()
        fig = gu.generateTreeGraph(graphComp, tu.getVerticies())
        
        tree.append(dcc.Graph(figure = fig))

        return html.Div(id = "decision-tree-component",children = tree)


    def generateDecisionBoundary(self, model):
        decisionBoundaryUtil = dbu.DecisionBoundaryUtil()

        divisions = []
        for i in range (0, model.tree_.node_count):
            if not model.tree_.feature[i] in divisions and model.tree_.feature[i] >= 0:
                divisions.append(model.tree_.feature[i])

        print(divisions)

        if(len(divisions) == 1):
            return html.Div(id = "decision-boundary-component", children = dcc.Graph(id="decision-boundary-1d", figure = decisionBoundaryUtil.decisionBoundaries1D(model, divisions[0])))
        elif(len(divisions) == 2):
            return html.Div(id = "decision-boundary-component", children = dcc.Graph(id="decision-boundary-2d", figure = decisionBoundaryUtil.decisionBoundaries2D(model, divisions)))
        else:
            return html.Div(id = "decision-boundary-component", children = [dcc.Graph(id="decision-boundary-higher"), dcc.Dropdown(id="x-feature", placeholder = "X Feature", options = model.feature_names_in_), dcc.Dropdown(id="y-feature", placeholder = "Y Feature ", options = model.feature_names_in_)], style={"font-size" : 16, "font-weight": "bold"})