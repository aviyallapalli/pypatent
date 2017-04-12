from .conll import ConllTree

del_roles = ["aux", "auxpass", "punct", "det", "predet", "cc", "quantmod", "tmod", "prep", "prt"]
attr_roles = ["arg", "acop", "mod", "amod", "nn", "neg", "expl", "poss", "possessive", "attr", "cop"]
append_roles = ["appos", "num", "number", "ref", "sdep"]
coord_roles = ["advcl", "comp", "acomp", "ccomp", "xcomp", "pcomp", "partmod", "advmod", "infmod", "mwe", "11mark",
               "rcmod", "npadvmod", "parataxis"]
i_roles = ["agent", "subj", "nsubj", "nsubjpass", "csubj", "csubjpass", "xsubj"]
ii_roles = ["obj", "dobj", "iobj", "pobj"]
conj_roles = ["conj", "preconj"]


def reduce_tree(tree: ConllTree):
    for i in tree:
        if i.value.deprel in del_roles:
            i.remove()

    for i in tree:
        value = i.value
        if value.deprel in attr_roles:
            value.deprel = "ATTR"
        elif value.deprel in append_roles:
            value.deprel = "APPEND"
        elif value.deprel in coord_roles:
            value.deprel = "COORD"
        elif value.deprel in i_roles:
            value.deprel = "I"
        elif value.deprel in ii_roles:
            value.deprel = "II"
        elif value.deprel in conj_roles:
            value.deprel = "CONJ"
