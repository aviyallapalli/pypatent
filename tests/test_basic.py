from docs.conf import Config

from pypatent.parser.xml_reader import read_element
from pypatent.parser.segment import segment
from pypatent.parser.treetagger import TreeTagger
from pypatent.parser.conll import conll_eng as conll
from pypatent.parser.maltparser import MaltParser

from pypatent.visualize import tree_to_png, parse_conll_text, build_graph

filepath = "/home/john/Projects/1.xml"

tt = TreeTagger(Config.tt_dir + Config.tt_bin, Config.tt_dir + Config.tt_model)
mp = MaltParser(Config.mp_dir, Config.mp_jar, Config.mp_model)

text = read_element(filepath, "claims")
text = segment(text)
text = tt.tag(text)
text = conll(text)
text = mp.parse(text)

tree = parse_conll_text(text)[0]
tree_to_png(tree, "/home/john/tree.png")
