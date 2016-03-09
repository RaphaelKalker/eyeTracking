import csv

class Node():
    def __init__(self, *args):
        Index,CutPredictor,CutPoint,IsBranchNode,NodeClass,Parent,ChildL,ChildR = args[0] 
        self.index = Index
        self.cutPredictor = CutPredictor
        self.cutPoint = float(CutPoint)
        self.isBranch = IsBranchNode
        self.nodeClass = "reading" if NodeClass == str(0) else "distance"
        self.parent = Parent
        self.childL = int(ChildL)
        self.childR = int(ChildR)

        self.right = None
        self.left = None

class DecisionTree():
    def __init__(self,):
        self.root = None

    def importTree(self, file_path):
        with open(file_path, 'r') as f: 
            csvReader = csv.reader(f, delimiter=',')
            fields = next(csvReader)

            nodes = []
            for r in csvReader:
                n = Node(r)
                nodes.append(n)
            self.constructTree(nodes)
    
    def constructTree(self, nodes):
        self.root = nodes[0]
        for n in nodes:
            if n.childL != 0 and n.childR != 0:
                # minus one for silly matlab indexing
                n.left = nodes[n.childL-1]
                n.right = nodes[n.childR-1]

    def traverseTree(self, *args):
        x, node = args
        
        if not node.cutPredictor:
            return node.nodeClass

        if node.cutPoint < x[node.cutPredictor]:
            nextNode = node.left
        else:
            nextNode = node.right

        return self.traverseTree(x, nextNode)

#    def printTree(self):
#        if self.root is not None:
#            self._printTree(self.root)
#
#    def _printTree(self, node):
#        if node is not None:
#            self._printTree(node.left)
#            print node.index
#            self._printTree(node.right)

