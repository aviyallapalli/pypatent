required_verbs = ["VVN"]

verb_attr = ["cop", "neg"] + ["prep"]


def techfeatures_from_tree(tree):
    verbs = [n for n in tree if n.upostag[0] == "V"]

    # only for verb with parent=0
    for v in verbs:
        children = get_children(tree, v)
        i_children = [n for n in children if n.deprel == "I"]
        ii_children = [n for n in children if n.deprel == "II"]

        # dep_parent = [n for n in tree if n.id == v.head and n.deprel == "dep"]
        # dep_children = [n for n in children if n.deprel == "dep"]

        if not len(i_children) or not len(ii_children):
            continue

        svo = []
        svo.append(v)
        svo.extend(i_children)
        svo.extend(ii_children)

        for i in i_children + ii_children:
            svo += [n for n in get_children(tree, i) if n.deprel == "ATTR"]

        # x = [n for n in get_children(tree, i) if n.deprel == #IN COP NEG???]

        conj = []
        for i in ii_children:
            conj += [n for n in get_children(tree, i) if n.deprel == "CONJ"]

        svo += conj

        for i in conj:
            svo += [n for n in get_children(tree, i) if n.deprel == "ATTR"]

        svo.sort(key=lambda x: int(x.id))

    return svo


def get_children(tree, node):
    return [n for n in tree if n.head == node.id]
