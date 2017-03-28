def extract_forest(text):
    from docs.conf import Config
    from .segment import segment
    from .treetagger import TreeTagger
    from .conll import Conll, parse_conll_text, conll_eng
    from .maltparser import MaltParser

    tt = TreeTagger(Config.tt_dir + Config.tt_bin, Config.tt_dir + Config.tt_model)
    mp = MaltParser(Config.mp_dir, Config.mp_jar, Config.mp_model)

    text = segment(text)
    text = tt.tag(text)
    text = conll_eng(text)
    text = mp.parse(text)
    forest = parse_conll_text(text)

    return forest


def reduce_forest(x):
    from .reduce import reduce_tree
    import copy

    forest = copy.deepcopy(x)
    for tree in forest:
        reduce_tree(tree)

    return forest
