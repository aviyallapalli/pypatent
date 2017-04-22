class Parser:
    def __init__(Parser, **kwargs):
        Parser.tt_bin = kwargs["tt_bin"]
        Parser.tt_model = kwargs["tt_model"]
        Parser.mp_dir = kwargs["mp_dir"]
        Parser.mp_jar = kwargs["mp_jar"]
        Parser.mp_model = kwargs["mp_model"]

    def morphological_analysis(self, text):
        from .treetagger import TreeTagger

        tt = TreeTagger(self.tt_bin, self.tt_model)
        tags = tt.tag(text)
        return tags

    def semantic_analysis(self, text):
        from .treetagger import TreeTagger
        from .maltparser import MaltParser
        from .conll import text_to_forest

        tt = TreeTagger(self.tt_bin, self.tt_model)
        mp = MaltParser(self.mp_dir, self.mp_jar, self.mp_model)

        text = tt.tag(text)
        text = mp.parse(text)
        forest = text_to_forest(text)

        return forest

    @staticmethod
    def extract_sao(forest):
        from .reduce import reduce_tree
        from .tf import tf_from_tree

        reduced_forest = [reduce_tree(t) for t in forest]
        sao = [tf_from_tree(t) for t in reduced_forest]

        return sao
