from pypatent.format.uspto import get_claims_from_xml, segment, find_sentences_in_text
from pypatent.parser import extract_forest

infile = "/home/john/sandbox/28837.xml"
text = get_claims_from_xml(infile)
segmented_text = segment(text)

sentences = segmented_text.split(". ")

coords = find_sentences_in_text(text, sentences)

for i, j in zip(sentences, coords):
    x, y = j
    print(i)
    print(text[x:y])
    print()
