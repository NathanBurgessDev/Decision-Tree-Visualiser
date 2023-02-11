from sklearn.tree import _tree

"""
AUTHOR: Ethan Temple-Betts
DATE CREATED: 04/02/2023
PREVIOUS MAINTAINER: Ethan Temple-Betts
DATE LAST MODIFIED: 04/02/2023

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
        
    '''
    AUTHOR: Ethan Temple-Betts
    PREVIOUS MAINTAINER: Ethan Temple-Betts

    Parses the decision tree classifier. The edges of the tree
    are put into the edges array. The verticies counter is
    incremented so as to store the total amount of verticies
    in the decision tree. annotations contains the annotation
    to be displayed on each node of the graph.

    INPUTS
    DecisionTreeClassifier tree : The model to be parsed
    '''
    def parseTree(self, tree):
        tree_ = tree.tree_
        # An array of feature names used to train the model
        featureName = tree.feature_names_in_
        
        # Creates an array of feature names, indexed by node,
        # that represent the feature used to split the data at
        # each node in the tree
        feature_Names = [
            featureName[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        '''
        AUTHOR: Ethan Temple-Betts
        PREVIOUS MAINTAINER: Ethan Temple-Betts

        A function to recurse over every node in the tree and
        calculate all the edges that exist between them.

        INPUTS
        int node: The id the next node in the sequence
        (0 for root node) 

        list[int] route: The edge represented as a list of ints
        (initially empty [])
        '''
        def recurse(node, route):
            # Increment thje shared ID variable to give each
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
                self.annotations.append(name + " <= " + str(round(threshold, 2)))
                
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
                self.annotations.append(str(tree_.value[node]))

        recurse(0, [])

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
