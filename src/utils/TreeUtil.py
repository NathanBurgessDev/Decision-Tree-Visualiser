from igraph import Graph
from sklearn.tree import _tree
from dash import dcc
from utils.Util import GraphUtil as GraphUtil
from igraph import Graph, EdgeSeq
from igraph import Vertex
import plotly.graph_objs as go


"""
AUTHOR: Ethan Temple-Betts
DATE CREATED: 04/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

Used to parse a given sklearn DecisionTreeClassifier in order to
obtain the relational edges between verticies and the decision
thresholds. This information is stored in the appropriate member
variables and can then be utilised for the creation of igraph
Graph objects, which are used to store the structure of
decsion trees.
"""

class TreeUtil():
    
    def __init__(self):
        # Used to give each node a unique ID
        self.ID = -1
        # Stores a list of tuple, which represent the edges
        # between nodes
        self.edges = []
        # Stores the total amount of verticies in the tree
        self.verticies = -1
        # A list of strings, one for each node in the form
        # "[fetaure name] <= [threshhold]" if the node is a
        # classification then the string will contain the number
        # of samples at that node
        self.annotations = []
        # A dictionary that stores the calculated Gini values
        # for each node and its key is the ID of the node in the decision tree.
        self.gini_dict = {}

    '''
    AUTHOR: Ethan Temple-Betts
    DATE CREATED: UNKNOWN
    PREVIOUS MAINTAINER: Kieran Patel and Dominic Cripps
    DATE LAST MODIFIED: 6/03/2023

    A function to generate the decision tree figure
    using the utility functions from this class.

    Inputs: 
    DecisionTreeClassifier model : The model to be parsed.
    '''
    def generateDecisionTree(self, classifier, model, tree):
        tree_ = []
        """ 
        The parseTree function changes several member variables
        within the TreeUtil object.

        verticies : int - represents the number of verticies in
        the tree graph.

        edges : list[tuple] - list of tuples representing the
        undirected and unweighted edges between all vertices.
        Each vertex has an ID (0..n), therefore a tuple (0,1)
        represents an edge between the root node and node 1.

        annotations : list[str] - list of strings that contain
        the feature and threshhold used at each node in the tree.

        These variables can then be accessed through calls to:
        getVerticies()
        getEdges()
        getAnnotations()
        """
        self.parseTree(classifier, model, tree)
        #Create graph component
        graphComp = Graph(directed = "T")
        #Assign properties (edges, vertices, annotations) 
        graphComp.add_vertices(self.getVerticies())
        graphComp.add_edges(self.getEdges())
        graphComp.vs["info"] = self.getAnnotations()
        #Generate graph for the tree.
        #if tree depth is < certain number then call the generateTreeGraph function
        if (self.getVerticies() <= 20):
            fig = self.generateTreeGraph(graphComp, self.getVerticies())
        #else call the generateTreeGraphLarge function
        elif (self.getVerticies() > 20):
            fig = self.generateTreeGraphLarge(graphComp, self.getVerticies())
        else:
            print("Error")
        #Append this object to an array to be used as a child component
        tree_.append(dcc.Graph(figure = fig))
        return tree_
    
    '''
    AUTHOR: Dominic Cripps
    DATE CREATED: 17/02/2023
    PREVIOUS MAINTAINER: Dominic Cripps
    DATE LAST MODIFIED: 18/02/2023

    Getter for the current leaf nodes classification.

    Inputs: 
    DecisionTreeClassifier model : The model to be parsed.
    Tree tree : The tree being evaluated.
    Integer nodeIndex : The index of the current leaf node.
    '''
    def getClassificiation(self, model, tree, nodeIndex):
        #An array of possible classifications.
        classes = model.classes_
        #Array representing how many of each classification
        #was used in training the current leaf.
        weights = tree.value[nodeIndex][0].tolist()
        largestID = 0
        currVal = 0
        #For loop to determine which weight is the largest
        for i in range (0, len(weights)):
            temp = int(weights[i])
            if (temp > currVal):
                currVal = temp
                largestID = i
        #Return the classification type
        return str(classes[largestID])

    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts and Kieran Patel

    Parses the decision tree classifier. The edges of the tree
    are put into the edges array. The verticies counter is
    incremented so as to store the total amount of verticies
    in the decision tree. annotations contains the annotation
    to be displayed on each node of the graph.

    INPUTS
    DecisionTreeClassifier tree : The model to be parsed
    '''
    def parseTree(self, classifier, model, tree_):
        # An array of feature names used to train the model
        featureName = classifier.feature_names_in_
            
        # Creates an array of feature names, indexed by node,
        # that represent the feature used to split the data at
        # each node in the tree
        feature_Names = [
            featureName[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        
        
        '''
        AUTHOR: Kieran Patel

        Date Created: 26/02/2023

        A recursive function that calculates and stores the Gini impurity
        values for each node in the decision tree.

        INPUTS:
        - node (int): The ID of the next node in the sequence,
        starting from the root node (ID = 0).

        RETURNS:
        None
        '''

        def calcAndStoreGini(node):
            # Checks if the current node is a leaf node, 
            # in which case the Gini impurity value is stored directly
            # from the tree object into the gini_dict.
            if tree_.children_left[node] == _tree.TREE_LEAF:
                self.gini_dict[node] = tree_.impurity[node]
            else:
                # This part recursively calls calcAndStoreGini for the left and right child nodes
                # and calculates the total number of samples in both child nodes.
                # The Gini impurity value for the current node is then calculated as a
                # weighted average of the impurity values of the left and right child nodes,
                # based on the number of samples in each child node.
                # Finally, the Gini impurity value is stored in the gini_dict for the current node.
                left = calcAndStoreGini(tree_.children_left[node])
                right = calcAndStoreGini(tree_.children_right[node])
                total_samples = tree_.n_node_samples[tree_.children_left[node]] + tree_.n_node_samples[tree_.children_right[node]]
                self.gini_dict[node] = (tree_.n_node_samples[tree_.children_left[node]] / total_samples) * tree_.impurity[tree_.children_left[node]] + (tree_.n_node_samples[tree_.children_right[node]] / total_samples) * tree_.impurity[tree_.children_right[node]]

        # Calls calcAndStoreGini starting from the root node
        calcAndStoreGini(0)


        # Creates an array of feature names, indexed by node,
        # that represent the feature used to split the data at
        # each node in the tree
        feature_Names = [
            featureName[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        '''
        AUTHOR: Ethan Temple-Betts
        PREVIOUS MAINTAINER: Dominic Cripps

        A function to recurse over every node in the tree and
        calculate all the edges that exist between them.

        INPUTS
        int node: The id the next node in the sequence
        (0 for root node) 

        list[int] route: The edge represented as a list of ints
        (initially empty [])
        '''
        def recurse(node, route):
            # Increment the shared ID variable to give each
            # node a unique ID
            self.ID += 1
            # Stores the ID of the node being parsed in each
            # function call
            localID = self.ID

            # If the node is a decsion node and not a
            # classification then continue else, The base case
            # is reached
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                # The feature name used for the current
                # decisiion node
                name = feature_Names[node]
                # The decision threshhold at the current node
                threshold = tree_.threshold[node]

                # Add this nodes ID to the array containing the
                # ID of the previous node
                route+=[localID]
                # Add the decision that relates to this node
                # "[feature name] <= [threshold]" to the
                # annotations list
                self.annotations.append(name + "<br> <= " + str(round(threshold, 2)))

                # If there are 2 items in the route array, then
                # this is a complete edge and the tuple is
                # added to the edges array
                if(len(route) > 1):
                    self.edges.append(tuple(route))

                # Sanity check to ensure nodes can't have an ID
                # which is greater than the number of nodes that
                # exist
                if localID > self.verticies:
                    self.verticies = localID


                # Recurse over the left and right children 
                recurse(tree_.children_left[node], [localID])
                recurse(tree_.children_right[node], [localID])
            else:
                # Add this nodes ID to the array containing the
                # ID of the previous node
                route += [localID]

                # If there are 2 items in the route array, then
                # this is a complete edge and the tuple is added
                # to the edges array
                if(len(route) > 1):
                    self.edges.append(tuple(route))


                # Sanity check to ensure nodes can't have an ID
                # which is greater than the number of nodes
                # that exist
                if localID > self.verticies:
                    self.verticies = localID
                

                # As this node is a classification, the
                # annotation is instead an array, which contains
                # the amount of samples from each class, which
                # have made it to this leaf node
                # Addition : The classification of each node will be 
                # returned by getClassification and shown on the label.
                self.annotations.append(self.getClassificiation(model, tree_, node))

        recurse(0, [])


    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    When given an igraph Graph this function will return
    a plotly graph, which represents the graphs structure.
    Most of code comes from https://plotly.com/python/tree-plots/.

    INPUTS
    igraph.Graph G: The Graph object to be displayed
    int nr_vertices: The number of verticies in the graph
    '''
    def generateTreeGraph(self, G, nr_vertices):
        lay = G.layout('rt')
        hover_information = []
        for i in range(nr_vertices):
            gini_value = round(self.gini_dict[i], 2)
            gini_str = "Gini: " + str(gini_value)
            hover_information.append(gini_str)
        position = {k: lay[k] for k in range(nr_vertices)}
        Y = [lay[k][1] for k in range(nr_vertices)]
        M = max(Y)

        es = EdgeSeq(G)
        E = [e.tuple for e in G.es]

        L = len(position)
        Xn = [position[k][0] for k in range(L)]
        Yn = [2*M-position[k][1] for k in range(L)]
        Xe = []
        Ye = []
        for edge in E:
            Xe+=[position[edge[0]][0],position[edge[1]][0], None]
            Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

        '''
        AUTHOR: Ethan Temple-Betts
        PREVIOUS MAINTAINER: Kieran Patel
        DATE LAST MODIFIED: 27/03/2023

        Used to assign annotations to nodes on the graph.

        Additions:
        - Hover information (Gini value so far) is now displayed on each node.
        - Markers are now bigger to fit the text.
        - The colour of leaf nodes is now different to the colour of decision nodes.

        INPUTS
        dict pos: 
        list[int] text:

        '''
        def make_annotations(pos, text, font_size=int(12-nr_vertices/30), font_color="#f5f5f5"):
            L=len(pos)
            if len(text)!=L:
                raise ValueError('The lists pos and text must have the same len')
            annotations = []
            for k in range(L):
                annotations.append(
                    dict(
                        # G.vs.info is assigned in the readMLM function #
                        text=G.vs["info"][k],
                        x=pos[k][0], y=2*M-position[k][1],
                        xref='x1', yref='y1',
                        font=dict(color=font_color, size=font_size),
                        showarrow=False)
                )
            return annotations

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Xe,
                        y=Ye,
                        mode='lines',
                        line=dict(color='rgb(210,210,210)', width=1),
                        hoverinfo='none'
                        ))
        fig.add_trace(go.Scatter(x=Xn,
                        y=Yn,
                        mode='markers',
                        name='bla',
                        marker=dict(symbol='diamond-wide',
                            size = 90 - nr_vertices / 5, #This can change according to the tree size
                            color=[color if node_degree == 1 else '#6175c1' for node_degree, color in zip(G.degree(), ['#06c258'] * nr_vertices)],
                            line=dict(color='Black', width=2)
                            ),
                        text=hover_information,
                        hoverinfo='text',
                        opacity=0.9
                        ))

        axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    )

        fig.update_layout(annotations=make_annotations(position, hover_information),
                    showlegend=False,
                    xaxis=axis,
                    yaxis=axis,
                    hovermode='closest',
                    plot_bgcolor="#232323",
                    paper_bgcolor = "#232323",
                    font_color = "#f5f5f5",
                    autosize=True, 
                    margin={'t': 10,'l':10,'b':5,'r':10},
                    )
        
        return fig

    '''
    AUTHOR: Kieran Patel
    DATE LAST MODIFIED: 5/03/2023

    When given an igraph Graph this function will return
    a plotly graph, which represents a large graphs structure.

    TODO: 
    - Try create a probability distribution using this,
    if it's not made then this can be removed and
    the calculation of the font and marker sizes
    can be adjusted in the generateTreeGraph function instead to make it more efficient


    INPUTS
    igraph.Graph G: The Graph object to be displayed
    int nr_vertices: The number of verticies in the graph
    '''
    def generateTreeGraphLarge(self, G, nr_vertices):
        
        lay = G.layout('rt')
        hover_information = []
        for i in range(nr_vertices):
            gini_value = round(self.gini_dict[i], 2)
            gini_str = "Gini: " + str(gini_value)
            hover_information.append(gini_str)
        position = {k: lay[k] for k in range(nr_vertices)}
        Y = [lay[k][1] for k in range(nr_vertices)]
        M = max(Y)

        es = EdgeSeq(G)
        E = [e.tuple for e in G.es]

        L = len(position)
        Xn = [position[k][0] for k in range(L)]
        Yn = [2*M-position[k][1] for k in range(L)]
        Xe = []
        Ye = []
        for edge in E:
            Xe+=[position[edge[0]][0],position[edge[1]][0], None]
            Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]


        '''
        AUTHOR: Ethan Temple-Betts
        PREVIOUS MAINTAINER: Kieran Patel
        DATE LAST MODIFIED: 21/03/2023

        Used to assign annotations to nodes on the graph.

        Additions:
        - Hover information (Gini value so far) is now displayed on each node.
        - Markers are now bigger to fit the text.
        - The colour of leaf nodes is now different to the colour of decision nodes.
        - Markers and text size are now dependent on the number of nodes in the graph.

        TODO:
        - When using the built in zoom function the markers and text
        will remain the same size, which is makes it difficult to read
        when the markers and text are small.

        INPUTS
        dict pos: 
        list[int] text:

        '''

        #Calculates the size of the marker and font for the tree
        if (9-nr_vertices/20) <= 0:
            fontS = 5
            markerS = 10
        else:
            fontS = (9-nr_vertices/20)
            markerS = 60 - (nr_vertices / 4)


        def make_annotations(pos, text, font_size=int(fontS), font_color="#f5f5f5"):
            L=len(pos)
            if len(text)!=L:
                raise ValueError('The lists pos and text must have the same len')
            annotations = []
            for k in range(L):
                annotations.append(
                    dict(
                        # G.vs.info is assigned in the readMLM function #
                        text=G.vs["info"][k],
                        x=pos[k][0], y=2*M-position[k][1],
                        xref='x1', yref='y1',
                        font=dict(color=font_color, size=font_size),
                        showarrow=False)
                )
            return annotations

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Xe,
                        y=Ye,
                        mode='lines',
                        line=dict(color='rgb(210,210,210)', width=1),
                        hoverinfo='none'
                        ))
        fig.add_trace(go.Scatter(x=Xn,
                        y=Yn,
                        mode='markers',
                        name='bla',
                        marker=dict(symbol='diamond-wide',
                            size= markerS,
                            color=[color if node_degree == 1 else '#6175c1' for node_degree, color in zip(G.degree(), ['#06c258'] * nr_vertices)],
                            line=dict(color='Black', width=2)
                            ),
                        text=hover_information,
                        hoverinfo='text',
                        opacity=0.9
                        ))

        axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    )

        fig.update_layout(annotations=make_annotations(position, hover_information),
                    showlegend=False,
                    xaxis=axis,
                    yaxis=axis,
                    hovermode='closest',
                    plot_bgcolor="#232323",
                    paper_bgcolor = "#232323",
                    font_color = "#f5f5f5",
                    autosize=True, 
                    margin={'t': 10,'l':10,'b':5,'r':10},
                    )
        

        return fig

    """
    AUTHOR: Kieran Patel
    PREVIOUS MAINTAINER: Kieran Patel
    DATE LAST MODIFIED: 8/03/2021
    
    Calculates the average depth of a tree represented as a graph.

    INPUTS:
    - G: the graph representing the tree
    - nr_vertices: the number of vertices in the graph

    """
    def calculateAverageDepth(self, G, nr_vertices):
        depth = 0
        for i in range(nr_vertices):
            depth += G.shortest_paths_dijkstra(source=i, target=nr_vertices-1)[0][0]
        return depth / nr_vertices

    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Getter for the verticies variable, which contains the
    amount  of verticies in the tree. If the parseTree function
    has not yet been run, then the value returned is 0.
    '''
    def getVerticies(self):
        return self.verticies + 1
    
    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Getter for the edges variable, which contains a list of
    tuples representing the edges between all nodes in the tree.
    If the parseTree function has not yet been run, then the
    empty list is returned.
    '''
    def getEdges(self):
        return self.edges

    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Getter for the annotations variable, which contains a list
    of the annotations for each node in the tree. If the
    parseTree function has not yet been run, then the empty list
    is returned.
    '''
    def getAnnotations(self):
        return self.annotations

    
