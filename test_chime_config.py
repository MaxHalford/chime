import chime


def _write(path, text):
    path.write_text(text, encoding="utf-8")
    return path


def test_default_theme_corrupt_config_falls_back(tmp_path):
    """A malformed config file must not crash config loading (issue: raw
    configparser traceback on import-adjacent helpers)."""
    bad = _write(tmp_path / "chime.conf", "this is not an ini file {{{\n")
    assert chime._get_default_theme(bad, "chime") == "chime"


def test_default_run_args_corrupt_config_falls_back(tmp_path):
    bad = _write(tmp_path / "chime.conf", "this is not an ini file {{{\n")
    assert chime._get_default_run_args(bad) == ""


def test_default_theme_valid_config_still_respected(tmp_path):
    good = _write(tmp_path / "chime.conf", "[chime]\ntheme = big-sur\n")
    assert chime._get_default_theme(good, "chime") == "big-sur"


def test_default_run_args_valid_config_still_respected(tmp_path):
    good = _write(tmp_path / "chime.conf", "[chime]\ncli_args = --volume 5\n")
    assert chime._get_default_run_args(good) == "--volume 5"
