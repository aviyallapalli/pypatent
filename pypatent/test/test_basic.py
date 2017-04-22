from pypatent.format.uspto import get_claims_from_xml, segment, mark_up_text
from pypatent.parser import Parser

infile = "/home/john/28837.xml"
src_text = get_claims_from_xml(infile)
sentences = segment(src_text)
text = " .".join(sentences)

config = {"tt_bin": "/home/john/Projects/libs/treetagger/tree-tagger",
          "tt_model": "/home/john/Projects/libs/treetagger/english-utf8.par",
          "mp_dir": "/home/john/Projects/libs/maltparser",
          "mp_jar": "maltparser-1.9.0.jar",
          "mp_model": "engmalt.linear-1.7.mco"}
p = Parser(**config)

tags = p.morphological_analysis(text)
trees = p.semantic_analysis(text)

sao = p.extract_sao(trees)

text = mark_up_text(src_text, sentences, sao)
print(text)
