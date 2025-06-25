import pytest

import insight.config
from insight.config import load_config, Config


def test_config_env_variable_not_set(monkeypatch):
    monkeypatch.setattr(insight.config, "CONFIG_INI_FILE_PATH", None)

    with pytest.raises(ValueError):
        _ = load_config(section="dev")


@pytest.mark.parametrize(
    "section", ["dev", "prod"], ids=["Dev Section", "Prod Section"]
)
def test_valid_config_files(monkeypatch, data_root, section):
    ini_file_path = data_root / "valid_configs.ini"

    monkeypatch.setattr(insight.config, "CONFIG_INI_FILE_PATH", ini_file_path)

    expected_config = Config(
        mode=section,
        db_database_name="name",
        db_host="host",
        db_password="password",
        db_port="1234",
        db_user="username",
    )

    actual_config = load_config(section=section)

    assert actual_config == expected_config


@pytest.mark.parametrize(
    "section",
    ["dev", "server", "non_existing_section"],
    ids=[
        "Dev Section But Incorrect Field value",
        "Incorrect Section",
        "This Section doesnt even exist in 'ini' file",
    ],
)
def test_invalid_config_files(monkeypatch, data_root, section):
    ini_file_path = data_root / "invalid_configs.ini"

    monkeypatch.setattr(insight.config, "CONFIG_INI_FILE_PATH", ini_file_path)

    with pytest.raises(ValueError):
        _ = load_config(section=section)
