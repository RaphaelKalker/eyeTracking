import sys
import csv
from BinaryTree import DecisionTree

a = DecisionTree()
a.importTree('./trees/tree1.csv')

with open(sys.argv[1], 'r') as f: 
    csvReader = csv.reader(f, delimiter=',')
    fields = next(csvReader)

    for r in csvReader:
        x = [float(x) for x in r]
        test = {'x1':x[0], 'x2': x[1], 'x3': x[2],'x4':x[3]}
        ret = a.traverseTree(test, a.root)
        print ret
