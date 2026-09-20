import pytest

from keka.config import KekaConfig, derive_login_url


def test_derive_login_url_from_instance():
    assert derive_login_url("https://acme.keka.com") == "https://login.keka.com/connect/token"


def test_derive_login_url_keeps_explicit_override():
    explicit = "https://auth.onprem.example/connect/token"
    assert derive_login_url("https://acme.keka.com", explicit) == explicit


def test_derive_login_url_adds_scheme_when_missing():
    assert derive_login_url("acme.keka.com") == "https://login.keka.com/connect/token"


def test_config_strips_trailing_slash_and_exposes_token_url():
    config = KekaConfig(instance_url="https://acme.keka.com/")
    assert config.instance_url == "https://acme.keka.com"
    assert config.token_url == "https://login.keka.com/connect/token"


def test_config_requires_instance_url():
    with pytest.raises(ValueError):
        KekaConfig(instance_url="")
