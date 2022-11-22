from sklearn.tree import _tree
from sklearn import tree
import pickle
import pandas as pd
import Tree as myTree

loaded_model = pickle.load(open("finalized_model.sav", 'rb'))
df = pd.read_csv('iris.csv')
X = df.iloc[:, 0:4]

def parseTree(tree, featureNames):
    tree_ = tree.tree_
    featureNames = [
        featureNames[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    
    treeStruc = myTree.Tree()

    def recurse(node, depth, root):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            n = myTree.Node()
            name = featureNames[node]
            threshold = tree_.threshold[node]
            n.setData([name, threshold])

            if(root == False):
                treeStruc.setRoot(n)

            n.setLeft(recurse(tree_.children_left[node], depth + 1, True))

            n.setRight(recurse(tree_.children_right[node], depth + 1, True))


            return n
        else:
            n = myTree.Node()
            n.setData(tree_.value[node])
            return n

    recurse(0, 1, False)
    treeStruc.printTree()

f=[]
for i in X:
    f.append(i)

parseTree(loaded_model, f)

