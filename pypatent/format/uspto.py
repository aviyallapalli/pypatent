import re
import xml.etree.ElementTree as etree
from pypatent.parser.tokenize import simple_word_tokenize as tokenize

__sep_phrase = [", wherein", ", said", ", and", "; and", ", thereby"] + ["if", "else", "thereby", "such that",
                                                                         "so that", "wherein",
                                                                         "whereby",
                                                                         "where", "when", "while", "but"]


# wtf

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


def mark_up_text(text, subsents, svo):
    coords = __find_sentences_coordinates(text, subsents)

    total_shift = 0
    tf_index = 1
    for coord, tfs in zip(coords, svo):
        if not tfs:
            continue

        sentence_start_index, sentence_end_index = coord
        sent = text[sentence_start_index + total_shift:sentence_end_index + total_shift]

        # TODO: temporary there is only 1 svo per subsent
        words_coords = __find_words_coordinates(sent, tfs)[0]

        if len(tfs[0]) != len(words_coords):
            # TODO: raise Exception
            print("ahtung")

        shift = 0
        sent_sub = sent
        for i in words_coords:
            start_index, end_index = i[0], i[1]
            word = sent[start_index: end_index]
            word_sub = "<div>{}</div>".format(word)
            sent_sub = sent_sub[:start_index + shift] + word_sub + sent_sub[end_index + shift:]
            shift += len(word_sub) - len(word)

        sent_sub = "<div class=\"tf{}\">{}</div>".format(tf_index, sent_sub)
        text = text[:sentence_start_index + total_shift] + sent_sub + text[sentence_end_index + total_shift:]
        tf_index += 1
        total_shift += len(sent_sub) - len(sent)

    text = text.replace("\n", "<br>")
    return text


def __find_sentences_coordinates(text, sentences):
    shift = 0
    coords = []
    for s in sentences:
        pattern = ".*?".join([t.replace(".", "") for t in tokenize(s)])
        result = re.search(pattern, text[shift:])

        new_coord = []
        if result:
            start, end = result.span()
            result = re.search(pattern, text[start + shift + 1: end + shift])
            while result:
                start += result.span()[0] + 1
                result = re.search(pattern, text[start + shift + 1: end + shift])

            new_coord = [start + shift, end + shift]
            shift += end
        coords.append(new_coord)

    return coords


def __find_words_coordinates(text, svo):
    shift = 0
    total_coords = []
    for tf in svo:
        coords = []
        for word in [n.form for n in tf]:
            result = re.search(word, text[shift:])

            if result:
                start, end = result.span()
                coords.append([start + shift, end + shift])
                shift += end
            else:
                # TODO: raise exception
                pass
        total_coords.append(coords)
    return total_coords