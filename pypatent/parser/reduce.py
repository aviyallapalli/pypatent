del_roles = ["aux", "auxpass", "cop", "punct", "det", "predet", "cc", "quantmod", "tmod", "prep", "prt"]
attr_roles = ["arg", "acop", "mod", "amod", "nn", "neg", "expl", "poss", "possessive", "attr"]
append_roles = ["appos", "num", "number", "ref", "sdep"]
coord_roles = ["advcl", "comp", "acomp", "ccomp", "xcomp", "pcomp", "partmod", "advmod", "infmod", "mwe", "11mark",
               "rcmod", "npadvmod", "parataxis"]
i_roles = ["agent", "subj", "nsubj", "nsubjpass", "csubj", "csubjpass", "xsubj"]
ii_roles = ["obj", "dobj", "iobj", "pobj"]
conj_roles = ["conj", "preconj"]


def reduce_tree(tree):
    node = __find_del_node(tree)
    while node is not None:
        __remove_del_node(tree, node)
        node = __find_del_node(tree)

    for node in tree:
        if node.deprel in attr_roles:
            node.deprel = "ATTR"
        elif node.deprel in append_roles:
            node.deprel = "APPEND"
        elif node.deprel in coord_roles:
            node.deprel = "COORD"
        elif node.deprel in i_roles:
            node.deprel = "I"
        elif node.deprel in ii_roles:
            node.deprel = "II"
        elif node.deprel in conj_roles:
            node.deprel = "CONJ"
        # else:
        #     print("unknown role {}".format(node.deprel))
    return tree


def __find_del_node(tree):
    for node in tree:
        if node.deprel in del_roles:
            return node
    return None


def __remove_del_node(tree, node):
    id = node.id
    parent = node.head
    tree.remove(node)
    for n in tree:
        if n.head == id:
            n.head = parent
