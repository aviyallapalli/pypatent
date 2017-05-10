__required_verbs = ["VVN"]

__verb_attr = ["cop", "neg"] + ["prep"]


def extract_sao(tree):
    from .conll import ConllTree
    from copy import copy

    features = []

    verbs = [x for x in tree if x.value.upostag[0] == "V"]

    for verb in verbs:
        i_children = verb.children_by_role("I")
        ii_children = verb.children_by_role("II")

        if not len(i_children) or not len(ii_children):
            continue

        feature = []
        feature.append(verb)
        feature.extend(i_children)
        feature.extend(ii_children)

        for i in i_children + ii_children + [tree]:
            feature += i.children_by_role("ATTR")

        conj = []
        for i in ii_children:
            conj += i.children_by_role("CONJ")

        feature += conj

        for i in conj:
            feature += i.children_by_role("ATTR")

        feature = [copy(x.value) for x in feature]
        feature[0].head = 0  # verb now is root
        feature.sort(key=lambda x: int(x.id))
        feature = ConllTree.from_list(feature)
        features.append(feature)

    return features
