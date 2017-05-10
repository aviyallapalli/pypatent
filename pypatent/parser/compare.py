from .conll import ConllTree


def compare(tree1: ConllTree, tree2: ConllTree):
    if tree1.value.lemma != tree2.value.lemma:
        return 0

    tree1_i = tree1.children_by_role("I")
    tree1_ii = tree1.children_by_role("II") + [t for child in tree1.children for t in child.children if
                                               t.value.deprel == "CONJ"]

    tree2_i = tree2.children_by_role("I")
    tree2_ii = tree2.children_by_role("II") + [t for child in tree2.children for t in child.children if
                                               t.value.deprel == "CONJ"]

    k_action = __calc_attr_matches(tree1, tree2)
    k_subject = __calc_children(tree1_i, tree2_i)
    k_object = __calc_children(tree1_ii, tree2_ii)

    return (k_subject + k_action + k_object) / 5


def __calc_children(children1, children2):
    result = []
    for i in children1:
        max_k = 0
        match = 0
        for j in children2:
            if i.value.lemma == j.value.lemma:
                # TODO: Will not work correctly with duplicates
                match = 1
                k = __calc_attr_matches(i, j)
                max_k = max(k, max_k)
        result.append(max_k + match)

    return sum(result) / max(len(list(children1)), len(list(children2)))


def __calc_attr_matches(tree1: ConllTree, tree2: ConllTree):
    attr1 = [x.value.lemma for x in tree1.children_by_role("ATTR")]
    attr2 = [x.value.lemma for x in tree2.children_by_role("ATTR")]

    count = max(len(list(attr1)), len(list(attr2)))
    if not count:
        return 1

    # TODO: Will not work correctly with duplicates
    matches = [x for x in attr1 if x in attr2]

    return len(matches) / count
