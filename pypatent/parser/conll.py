def conll_eng(tagged_text_list):
    conll_text = ""
    for word in tagged_text_list:

        if str.lower(word[1]) == "sent":
            conll_text += "\n"
            continue

        conll_text += "1" + "\t" + word[0] + "\t" + word[2] + "\t" + word[1] + "\t" + word[1] + "\t" + "_" + "\n"
        conll_text += "\n" if str.lower(word[1]) == "sent" else ""

    return conll_text
