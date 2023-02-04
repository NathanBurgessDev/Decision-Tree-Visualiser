import igraph as ig
from igraph import Graph, EdgeSeq
from sklearn.tree import _tree
from sklearn import tree
import pickle
import pandas as pd
import plotly.graph_objects as go

class TreeUtil():
    
    def __init__(self):
        self.ID = -1
        self.cache = []
        self.verticies = -1
        self.nodeInfo = []
        
    # parses a decision tree classifier when give an array of the feature names
    # and the model. The edges of the tree are put into the cache array.
    # The verticies counter is incremented as it is needed to generate the iGraph.
    # nodeInfo contains the annotation to be shown for each node in the graph
    def parseTree(self, tree):
        tree_ = tree.tree_
        featureName = tree.feature_names_in_
            
        feature_Names = [
            featureName[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        def recurse(node, depth, route):
            self.ID += 1
            localID = self.ID

            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_Names[node]
                threshold = tree_.threshold[node]

                route+=[localID]
                self.nodeInfo.append(name + " <= " + str(round(threshold, 2)))
                
                if(len(route) > 1):
                    self.cache.append(tuple(route))

                if localID > self.verticies:
                    self.verticies = localID
                
                recurse(tree_.children_left[node], depth + 1, [localID])
                recurse(tree_.children_right[node], depth + 1, [localID])
            else:
                route += [localID]
                if(len(route) > 1):
                    self.cache.append(tuple(route))

                if localID > self.verticies:
                    self.verticies = localID
                    
                tree_. n_node_samples[node]
                self.nodeInfo.append(str(tree_.value[node]))

        recurse(0, 1, [])

    def getVerticies(self):
        return self.verticies + 1

    def getEdges(self):
        return self.cache

    def getAnnotations(self):
        return self.nodeInfo
