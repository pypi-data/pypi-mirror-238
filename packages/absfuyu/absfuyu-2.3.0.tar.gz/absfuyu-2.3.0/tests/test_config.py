import pytest
from absfuyu import config as cfg

def test_cfg():
    assert cfg

def test_load_cfg():
    assert cfg.__load_cfg()

def test_change_cfg():
    assert cfg.change_cfg("test", True) is None

def test_change_cfg_2():
    cfg.change_cfg("test", True)
    test = cfg.show_cfg("test", raw=True)
    assert test is True

def test_togg():
    assert cfg.toggle_setting("test") is None

def test_default():
    assert cfg.reset_cfg() is None

def test_default_2():
    cfg.toggle_setting("test")
    cfg.reset_cfg()
    conf = cfg.__load_cfg()
    conf_t = conf["setting"]["test"]["default"]
    test = cfg.show_cfg("test", raw=True)
    assert conf_t==test