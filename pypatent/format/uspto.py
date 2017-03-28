import re
import xml.etree.ElementTree as etree
from pypatent.parser.tokenize import simple_word_tokenize as tokenize

__sep_phrase = [", wherein", ", said", ", and", "; and"] + ["if", "else", "thereby", "such that", "so that", "where",
                                                            "whereby",
                                                            "wherein", "when", "while", "but"]


def get_claims_from_xml(filepath):
    """
    Get field "claims" from xml-file
    :param filepath: path to the xml-file
    :return: text of the "claims" field, each claim separated by "\n"
    """

    # TODO: validate input file, it may be in another format
    claims = etree.parse(filepath).getroot().find("claims")
    text = "\n".join(" ".join(claim.itertext()).strip() for claim in claims)
    text = text.replace(" ,", ",")
    text = text.replace("  ", " ")

    return text


def segment(text):
    """
    Separate input text on sub-sentences and remove junk words
    :param text: The string containing the text, each paragraph separated by "\n"
    :return: The string containing sub-sentences separated by "\n"
    """
    paragraphs = text.split("\n")
    x = []
    for paragraph in paragraphs:
        # нумерация
        sub_sent = re.sub("^(\d{1,4}|[a-zA-Z]{1,2})(\.|\))\s", "", paragraph)
        # ссылка на другой claim
        sub_sent = re.sub("^.+(of|in|to) claim \d+(, )?", "", sub_sent)

        # слова-разделители
        for phrase in __sep_phrase:
            sub_sent = re.sub(",?\s?{}\s?".format(phrase), "\n", sub_sent)

        # знаки пунктуации
        sub_sent = re.sub("(\.|!|\?|:|;)\s?", "\n", sub_sent)

        sub_sent = sub_sent.split("\n")

        # отбрасываем предложения короче 2-х слов
        sub_sent = [x.strip() for x in sub_sent if len(tokenize(x)) > 2]

        x.append(sub_sent)

    x = ". ".join([j for i in x for j in i])
    return x


def find_sentences_in_text(text, sentences):
    # TODO: tmp
    shift = 0
    coords = []
    for s in sentences:
        pattern = ".*?".join([t.replace(".", "") for t in tokenize(s)])
        result = re.search(pattern, text[shift:])

        new_coord = []
        if result:
            start, end = result.span()
            new_coord = [start + shift, end + shift]
            shift += end
        coords.append(new_coord)

    return coords
