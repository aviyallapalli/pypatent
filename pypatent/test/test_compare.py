from pypatent.parser import Parser
from pypatent.parser.sao import extract_sao
from pypatent.parser.reduce import reduce_tree
from pypatent.parser.compare import compare

config = {"tt_bin": "/home/john/Projects/libs/treetagger/tree-tagger",
          "tt_model": "/home/john/Projects/libs/treetagger/english-utf8.par",
          "mp_dir": "/home/john/Projects/libs/maltparser",
          "mp_jar": "maltparser-1.9.0.jar",
          "mp_model": "engmalt.linear-1.7.mco"}
p = Parser(**config)

sent1 = "the chamber having a first red port and a second valve"
sent2 = "the chamber not having a first blue port or a broken valve"

tree1 = p.semantic_analysis(sent1)[0]
tree2 = p.semantic_analysis(sent2)[0]

tree1 = reduce_tree(tree1)
tree2 = reduce_tree(tree2)

sao1 = extract_sao(tree1)[0]
sao2 = extract_sao(tree2)[0]

print(sao1)
print()
print(sao2)
k = compare(sao1, sao2)
print(k)
