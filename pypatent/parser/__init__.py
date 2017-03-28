def extract_forest(text):
    from docs.conf import Config
    from .segment import segment
    from .treetagger import TreeTagger
    from .conll import Conll, text_to_conll, tt_list_to_conll
    from .maltparser import MaltParser

    tt = TreeTagger(Config.tt_dir + Config.tt_bin, Config.tt_dir + Config.tt_model)
    mp = MaltParser(Config.mp_dir, Config.mp_jar, Config.mp_model)

    text = tt.tag(text)
    text = tt_list_to_conll(text)
    text = mp.parse(text)
    forest = text_to_conll(text)

    return forest


def reduce_forest(x):
    from .reduce import reduce_tree
    import copy

    forest = copy.deepcopy(x)
    for tree in forest:
        reduce_tree(tree)

    return forest
