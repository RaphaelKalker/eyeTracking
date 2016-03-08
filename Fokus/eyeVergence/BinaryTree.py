import csv

class Node():
    def __init__(self, *args):
        cutPredictor, cutPoint, isBranch, NodeClass, Parent = args[0] 
        self.cutPredictor = cutPredictor
        self.cutPoint = cutPoint
        self.isBranch = isBranch
        self.NodeClass = NodeClass
        self.Parent = Parent
        self.Index = args[1] 

        self.right = None
        self.left = None

class DecisionTree():
    def __init__(self,):
        self.root = None

    def importTree(self, file_path):
        with open(file_path, 'r') as f: 
            csvReader = csv.reader(f, delimiter=',')
            fields = next(csvReader)
            print fields

            i = 1;
            for r in csvReader:
                self.add(r, i)
                i += 1
        t = ""
        return t

    def add(self, *args):
        if self.root is None:
            self.root = Node(args[0], args[1])
        else:
            self._add(args[0], self.root, args[1])

    def _add(self, *args):
        cutPredictor, cutPoint, isBranch, NodeClass, Parent = args[0] 
        rootNode = args[1]
        Index = args[2]
        
#        if rootNode.Index == Parent:
#            if rootNode.left is None:
#                rootNode.left = Node(args[0], Index)
#            else:
#                self._add(args[0], rootNode, Index)
#            if rootNode.right is None:
#                rootNode.right = Node(args[0], Index)
#            else:
#                self._add(args[0], rootNode, Index)
#
#
#    def traverseTree(self, l_xy, r_xy):
#        ret = "READING" if res == 0 else "DISTANCE"
#        if 
#        return ret
