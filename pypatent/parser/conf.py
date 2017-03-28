import configparser, os


class Config:
    """
    Config-file reader
    """
    _cfg = configparser.ConfigParser()
    # TODO: add custom exception
    _cfg.read(os.getenv("PYPATENT_CFG"))

    tt_dir = _cfg.get("TreeTagger", "directory")
    tt_bin = _cfg.get("TreeTagger", "bin")
    tt_model = _cfg.get("TreeTagger", "model")

    mp_dir = _cfg.get("MaltParser", "directory")
    mp_jar = _cfg.get("MaltParser", "jar")
    mp_model = _cfg.get("MaltParser", "model")
