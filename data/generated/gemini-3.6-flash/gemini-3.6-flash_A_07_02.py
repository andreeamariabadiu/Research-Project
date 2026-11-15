import configparser
import os
import sqlite3
from typing import Optional


def connect_to_db(
    config_path: str, section: str = "database"
) -> Optional[sqlite3.Connection]:
    """Reads a configuration file and establishes a connection to a database.

    :param config_path: Path to the configuration file (.ini format).
    :param section: Section in the config file containing database settings.
    :return: A sqlite3 Connection object, or None if the connection fails.
    """
    if not os.path.exists(config_path):
        print(f"Error: Configuration file '{config_path}' not found.")
        return None

    config = configparser.ConfigParser()

    try:
        config.read(config_path)
    except configparser.Error as e:
        print(f"Error parsing configuration file: {e}")
        return None

    if not config.has_section(section):
        print(
            f"Error: Section '{section}' not found in configuration file '{config_path}'."
        )
        return None

    db_config = dict(config.items(section))
    db_name = db_config.get("database") or db_config.get("db_name")

    if not db_name:
        print("Error: Database name/path not specified in configuration.")
        return None

    try:
        conn = sqlite3.connect(db_name)
        print(f"Successfully connected to database: {db_name}")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")
        return None
