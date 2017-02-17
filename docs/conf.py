import configparser


class Config:
    """
    Config-file reader
    """
    _cfg = configparser.ConfigParser()
    _cfg.read(__file__[:-7] + "main.cfg")

    tt_dir = _cfg.get("TreeTagger", "directory")
    tt_bin = _cfg.get("TreeTagger", "bin")
    tt_model = _cfg.get("TreeTagger", "model")

    mp_dir = _cfg.get("MaltParser", "directory")
    mp_jar = _cfg.get("MaltParser", "jar")
    mp_model = _cfg.get("MaltParser", "model")
