del_roles = ["aux", "auxpass", "cop", "punct", "det", "predet", "cc", "quantmod", "tmod", "prep", "prt"]
attr_roles = ["arg", "acop", "mod", "amod", "nn", "neg", "expl", "poss", "possessive", "attr"]
append_roles = ["appos", "num", "number", "ref", "sdep"]
coord_roles = ["advcl", "comp", "acomp", "ccomp", "xcomp", "pcomp", "partmod", "advmod", "infmod", "mwe", "11mark",
               "rcmod", "npadvmod", "parataxis"]
i_roles = ["agent", "subj", "nsubj", "nsubjpass", "csubj", "csubjpass", "xsubj"]
# ii_roles = ["obj", "dobj", "iobj", "pobj", "dep"]
ii_roles = ["obj", "dobj", "iobj", "pobj"]
conj_roles = ["conj", "preconj"]


def convert_conll_tree(tree):
    node = find_del_node(tree)
    while node is not None:
        remove_del_node(tree, node)
        node = find_del_node(tree)

    for node in tree:
        if node[7] in attr_roles:
            node[7] = "ATTR"
        elif node[7] in append_roles:
            node[7] = "APPEND"
        elif node[7] in coord_roles:
            node[7] = "COORD"
        elif node[7] in i_roles:
            node[7] = "I"
        elif node[7] in ii_roles:
            node[7] = "II"
        elif node[7] in conj_roles:
            node[7] = "CONJ"
            # else:
            #     print("unknown role {}".format(node[7]))
    return tree


def find_del_node(tree):
    for node in tree:
        if node[7] in del_roles:
            return node
    return None


def remove_del_node(tree, node):
    id = node[0]
    parent = node[6]
    tree.remove(node)
    for n in tree:
        if n[6] == id:
            n[6] = parent


class SVO:
    def __init__(self, subject, verb, object):
        self.subject = subject
        self.verb = verb
        self.object = object

    def triplet(self):
        return [self.subject[2], self.verb[2], self.object[2]]


def extract_sao(tree):
    verbs = ["VBZ", "VVZ", "VHZ", "VVN"] + ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"] + ["VV"]

    action_nodes = []
    for node in tree:
        # if node[3] in verbs:
        if node[3][0] == "V":
            action_nodes.append(node)

    svo_list = []
    for verb in action_nodes:
        children = get_children(tree, verb)

        i_children = []
        ii_children = []
        for child in children:
            if child[7] is "I":
                i_children.append(child)
            elif child[7] is "II":
                ii_children.append(child)

        for subject in i_children:
            for object in ii_children:
                svo_list.append(SVO(subject, verb, object))

    return [svo.triplet() for svo in svo_list]


def get_children(tree, node):
    children = []
    for n in tree:
        if n[6] == node[0]:
            children.append(n)
    return children
