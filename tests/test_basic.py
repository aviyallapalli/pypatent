from pypatent.format.uspto import get_claims_from_xml, segment, find_sentences_in_text

infile = "/home/john/sandbox/28837.xml"
text = get_claims_from_xml(infile)
segmented_text = segment(text)

sentences = segmented_text.split("\n")
coords = find_sentences_in_text(text, sentences)
