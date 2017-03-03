from pypatent.parser import extract_forest
from pypatent.parser.reduce import reduce_tree
from pypatent.parser.svo import extract_svo

filepath = "/home/john/Projects/1.xml"

forest = extract_forest(filepath)
svo = []
for tree in forest:
    tree = reduce_tree(tree)
    svo += extract_svo(tree)

print(svo)
