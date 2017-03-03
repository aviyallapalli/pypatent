import re


def segment(text):
    phrase_del = [", and ", " if ", " else ", " thereby ", " such that ", " so that ", " where ", " whereby ",
                  " wherein ", " when ", " while ", " but "]

    for s in phrase_del:
        text = re.sub(s, ".\n" + s, text)

    phrase_im = ["which", "who", "what", "that"]
    phrase_im1 = ["on", "at", "in", "to"]

    for p1 in phrase_im:
        for p2 in phrase_im1:
            phrase = " " + p2 + " " + p1 + " "
            text = re.sub(phrase, ".\n" + phrase, text)

    text = re.sub("\?", ".\n", text)
    text = re.sub(":", ".\n", text)
    # text = re.sub(":", "", text)
    text = re.sub(";", ".\n", text)
    text = re.sub("\.", ".\n", text)

    text = re.sub("^", "\n", text)
    text = re.sub("\n([0-9]{1,4}|[a-zA-Z]{1,2})(\.|\)) *", "\n", text)

    text = re.sub("\n ", "\n", text)
    text = re.sub(",\.\n", ".\n", text)
    text = re.sub("\n, ", "\n", text)
    text = re.sub("\n{2,}", "\n", text)

    # =======================================================
    text = re.sub("\n\.\n", "\n", text)
    # text = re.sub("\nclaim [0-9]+\n", "\n", text)
    text = re.sub("\n[A-Za-z ]+\nclaim [0-9]+\n", "\n", text)

    text = re.sub("\nwherein ", "\n", text)
    # =======================================================

    if text[0] is "\n":
        text = text[1:]

    return text
