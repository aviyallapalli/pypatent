import configparser


class Config:
    """
    Config-file reader
    """
    @staticmethod
    def read(filepath):
        cfg = configparser.ConfigParser()
        cfg.read(filepath)

        Config.tt_dir = cfg.get("TreeTagger", "directory")
        Config.tt_bin = cfg.get("TreeTagger", "bin")
        Config.tt_model = cfg.get("TreeTagger", "model")

        Config.mp_dir = cfg.get("MaltParser", "directory")
        Config.mp_jar = cfg.get("MaltParser", "jar")
        Config.mp_model = cfg.get("MaltParser", "model")
