class Tree:
    
    def __init__(self):
        self.root = None

    def setRoot(self, node):
        self.root = node

    def getRoot(self):
        return self.root

    def printTree(self):
        start = self.root
        def recurse(start):
            if start != None:
                print(str(start.getData()))
                if(start.getLeft != None):
                    print("left of node ")
                    recurse(start.getLeft())
                if(start.getRight != None):
                    print("right of node ")
                    recurse(start.getRight())
            else:
                print("End\n")
        
        recurse(start)

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None

    def setRight(self, node):
        self.right = node

    def setLeft(self, node):
        self.left = node

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right
