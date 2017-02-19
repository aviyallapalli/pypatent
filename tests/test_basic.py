from pypatent.parser import extract_tree
from pypatent.visualize import parse_conll_text, tree_to_png
from pypatent.parser.sao import convert_conll_tree, extract_sao

filepath = "/home/john/Projects/1.xml"

text = extract_tree(filepath)
tree = parse_conll_text(text)[3]
tree = convert_conll_tree(tree)
svo = extract_sao(tree)
print(svo)

# tree_to_png(tree, "/home/john/tree.png")