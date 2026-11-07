import configparser
import logging
from typing import Optional
import psycopg2
from psycopg2 import Error as DBError

# Set up standard logger
logger = logging.getLogger(__name__)


def connect_to_database(config_path: str) -> Optional[psycopg2.extensions.connection]:
    """
    Reads database configuration from an INI file and establishes a database connection.
    Prevents leakage of sensitive info (passwords, connection strings, stack traces).
    """
    config = configparser.ConfigParser()

    try:
        read_files = config.read(config_path)
        if not read_files:
            logger.error("Configuration file could not be read or does not exist.")
            raise FileNotFoundError("Configuration file missing or unreadable.")

        db_section = config["database"]
        host = db_section.get("host")
        port = db_section.get("port", "5432")
        dbname = db_section.get("dbname")
        user = db_section.get("user")
        password = db_section.get("password")

        if not all([host, dbname, user, password]):
            logger.error("Missing required database configuration parameters.")
            raise ValueError("Incomplete database configuration.")

    except (configparser.Error, KeyError) as e:
        logger.error("Failed to parse database configuration file.")
        # Suppress exception chaining to avoid leaking config details in tracebacks
        raise ValueError("Invalid configuration file format.") from None
    except Exception as e:
        if not isinstance(e, (FileNotFoundError, ValueError)):
            logger.error("An error occurred while loading the configuration.")
        raise

    try:
        # Establish database connection
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            connect_timeout=10,
        )
        logger.info("Database connection established successfully.")
        return connection

    except DBError:
        # Intentionally do not log raw exception details as they may contain credentials or sensitive network info
        logger.error("Failed to connect to the database. Connection refused or invalid credentials.")
        raise ConnectionError("Unable to connect to the database.") from None
    except Exception:
        logger.error("An unexpected error occurred during database connection.")
        raise RuntimeError("Database connection failed due to an unexpected error.") from None
