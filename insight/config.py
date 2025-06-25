import os
from configparser import ConfigParser
from typing import Literal
from pathlib import Path
from importlib.metadata import version

from pydantic import BaseModel

PACKAGE_NAME = "insight"
PACKAGE_VERSION = version(PACKAGE_NAME)
CONFIG_INI_FILE_PATH = os.getenv("CONFIG_INI_FILE_PATH")
LOG_DIR = Path(os.getenv("LOG_DIR", Path(__file__).parent.parent.resolve()))


class Config(BaseModel):
    mode: Literal["dev", "prod"]
    db_host: str
    db_database_name: str
    db_port: str
    db_user: str
    db_password: str


def load_config(section: Literal["dev", "prod"]) -> Config:
    """
    Load configuration from the database ini file.

    This function reads the configuration from the specified ini file and returns
    a dictionary containing the parsed configuration parameters.

    Attributes:
        section (Literal[dev, prod]): The Section which defines what database needs to be loaded.
    Returns:
        Config: A config containing the loaded configuration parameters.

    Raises:
        ValueError: If the environment variable 'CONFIG_INI_FILE_PATH' is not set.
        ValueError: If the specified section is not found in the ini file.
    """

    if not CONFIG_INI_FILE_PATH:
        raise ValueError("Environment Variable 'CONFIG_INI_FILE_PATH' is not set")

    parser = ConfigParser()
    parser.read(CONFIG_INI_FILE_PATH)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise ValueError(
            f"Section {section!r} not found in the {CONFIG_INI_FILE_PATH} file"
        )

    config["mode"] = section
    return Config(**config)
