def extract_forest(filepath):
    from docs.conf import Config

    from .xml_reader import read_element
    from .segment import segment
    from .treetagger import TreeTagger
    from .conll import Conll, parse_conll_text, conll_eng
    from .maltparser import MaltParser

    import time
    from datetime import timedelta

    start_time = time.time()

    tt = TreeTagger(Config.tt_dir + Config.tt_bin, Config.tt_dir + Config.tt_model)
    mp = MaltParser(Config.mp_dir, Config.mp_jar, Config.mp_model)

    text = read_element(filepath, "claims")
    text = segment(text)
    text = tt.tag(text)
    text = conll_eng(text)
    text = mp.parse(text)
    forest = parse_conll_text(text)

    end_time = time.time() - start_time
    print("{} parsed in {} seconds.".format(filepath, str(timedelta(seconds=end_time))))

    return forest
