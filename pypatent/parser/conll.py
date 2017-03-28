class Conll:
    """
    http://universaldependencies.org/format.html
    1. ID: Word index, integer starting at 1 for each new sentence;
    may be a range for multiword tokens; may be a decimal number for empty nodes.
    2. FORM: Word form or punctuation symbol.
    3. LEMMA: Lemma or stem of word form.
    4. UPOSTAG: Universal part-of-speech tag.
    5. XPOSTAG: Language-specific part-of-speech tag; underscore if not available.
    6. FEATS: List of morphological features from the universal feature inventory or
    from a defined language-specific extension; underscore if not available.
    7. HEAD: Head of the current word, which is either a value of ID or zero (0).
    8. DEPREL: Universal dependency relation to the HEAD (root iff HEAD = 0)
    or a defined language-specific subtype of one.
    9. DEPS: Enhanced dependency graph in the form of a list of head-deprel pairs.
    10. MISC: Any other annotation.
    """

    def __init__(self, args):
        self.id = args[0]
        self.form = args[1]
        self.lemma = args[2]
        self.upostag = args[3]
        self.xpostag = args[4]
        self.feats = args[5]
        self.head = args[6]
        self.deprel = args[7]
        self.deps = args[8]
        self.misc = args[9]

    def __str__(self):
        string = str(self.id) + "\t" + \
                 self.form + "\t" + \
                 self.lemma + "\t" + \
                 self.upostag + "\t" + \
                 self.xpostag + "\t" + \
                 self.feats + "\t" + \
                 self.head + "\t" + \
                 self.deprel + "\t" + \
                 self.deps + "\t" + \
                 self.misc
        return string

    def __iter__(self):
        return iter([self.id, self.form, self.lemma, self.upostag, self.xpostag,
                     self.feats, self.head, self.deprel, self.deps, self.misc])


def tt_list_to_conll(tagged_text_list):
    conll_text = ""
    for word in tagged_text_list:

        if str.lower(word[1]) == "sent":
            conll_text += "\n"
            continue

        conll_text += "1" + "\t" + word[0] + "\t" + word[2] + "\t" + word[1] + "\t" + word[1] + "\t" + "_" + "\n"
        conll_text += "\n" if str.lower(word[1]) == "sent" else ""

    return conll_text


def text_to_conll(text):
    text = text.split("\n")
    tree = []
    forest = []
    for line in text:
        node = line.split("\t")
        if len(node) != 1:
            tree.append(Conll(node))
        else:
            if len(tree) != 0:
                forest.append(tree)
                tree = []
    if len(tree) != 0:
        forest.append(tree)

    return forest
