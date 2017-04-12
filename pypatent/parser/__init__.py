def extract_forest(sents):
    from .conf import Config
    from .treetagger import TreeTagger
    from .maltparser import MaltParser
    from .conll import text_to_forest

    tt = TreeTagger(Config.tt_dir + Config.tt_bin, Config.tt_dir + Config.tt_model)
    mp = MaltParser(Config.mp_dir, Config.mp_jar, Config.mp_model)

    text = ". ".join(sents)
    text = tt.tag(text)
    # TODO: try multiprocessing
    # results = multiprocessing.Pool(number_of_processes).map(func, data)
    # outputs = [result[0] for result in results]
    text = mp.parse(text)
    forest = text_to_forest(text)

    return forest


def reduce_forest(x):
    from .reduce import reduce_tree
    import copy

    forest = copy.deepcopy(x)
    for tree in forest:
        reduce_tree(tree)

    return forest
