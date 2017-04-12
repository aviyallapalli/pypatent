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
        self.id = int(args[0])
        self.form = args[1]
        self.lemma = args[2]
        self.upostag = args[3]
        self.xpostag = args[4]
        self.feats = args[5]
        self.head = int(args[6])
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
                 str(self.head) + "\t" + \
                 self.deprel + "\t" + \
                 self.deps + "\t" + \
                 self.misc
        return string

    def __iter__(self):
        return iter([self.id, self.form, self.lemma, self.upostag, self.xpostag,
                     self.feats, self.head, self.deprel, self.deps, self.misc])


class ConllTree:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        self.children = []

    def add_child(self, value):
        if not isinstance(value, type(self.value)):
            raise TypeError

        child = ConllTree(value, self)
        self.children.append(child)
        return child

    def remove(self):
        if not self.parent:
            raise RemoveRootError
        self.parent.children.remove(self)
        for child in self.children:
            child.value.head = self.parent.value.id
            self.parent.children.append(child)

    def children_by_role(self, role):
        return [x for x in self.children if x.value.deprel == role]

    @staticmethod
    def from_list(data):
        root = next((x for x in data if x.head == 0))
        tree = ConllTree(root)
        tree.__parse_children(data)
        return tree

    @staticmethod
    def from_str(string):
        return ConllTree.from_list([Conll(x.split("\t")) for x in string.split("\n") if x])

    def __parse_children(self, data):
        children = [n for n in data if n.head == self.value.id]
        for child in children:
            # current_child = self.add_child(child)
            # current_child.__parse_children(data)
            self.add_child(child).__parse_children(data)

    def __iter__(self):
        from itertools import chain
        sequence = list(chain((self,), *map(iter, self.children)))
        sequence.sort(key=lambda x: x.value.id)
        return iter(sequence)

    def __str__(self):
        return "\n".join(str(x.value) for x in self.__iter__())


class RemoveRootError(Exception):
    pass


def text_to_forest(text):
    return [ConllTree.from_str(x) for x in text.split("\n\n") if x]


def forest_to_text(forest):
    return "\n\n".join("\n".join(str(n.value) for n in t) for t in forest)
