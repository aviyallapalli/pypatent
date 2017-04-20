from pypatent.format.uspto import get_claims_from_xml, segment, mark_up_text
from pypatent.parser import extract_forest, reduce_forest
from pypatent.parser.tf import tf_from_tree

infile = "/home/john/28837.xml"
text = get_claims_from_xml(infile)
sents = segment(text)
forest = extract_forest(sents)
rforest = reduce_forest(forest)
features = [tf_from_tree(t) for t in rforest]
text = mark_up_text(text, sents, features)
print(text)
