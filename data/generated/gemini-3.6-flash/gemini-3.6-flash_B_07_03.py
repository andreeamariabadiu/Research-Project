import configparser
import logging
import os
import psycopg2

logger = logging.getLogger(__name__)


class DatabaseConnectionError(Exception):
    """Custom exception raised when a database connection failure occurs."""

    pass


def connect_to_database(config_file_path: str):
    """Reads database configuration from a file and establishes a connection safely.

    Protects sensitive credentials and internal details from leaking in logs or
    exceptions.
    """
    if not os.path.exists(config_file_path):
        logger.error(
            "Configuration load failed: File not found at specified path."
        )
        raise DatabaseConnectionError("Configuration file missing.")

    config = configparser.ConfigParser()

    try:
        config.read(config_file_path)
    except Exception:
        logger.error("Configuration load failed: Unable to parse file.")
        raise DatabaseConnectionError(
            "Invalid configuration file format."
        ) from None

    if "database" not in config:
        logger.error(
            "Configuration load failed: Missing [database] section."
        )
        raise DatabaseConnectionError("Invalid configuration section.")

    db_config = config["database"]
    required_keys = ["host", "port", "dbname", "user", "password"]

    missing_keys = [key for key in required_keys if key not in db_config]
    if missing_keys:
        logger.error(
            "Configuration load failed: Missing required parameters."
        )
        raise DatabaseConnectionError(
            "Incomplete database configuration parameters."
        )

    try:
        connection = psycopg2.connect(
            host=db_config["host"],
            port=db_config["port"],
            dbname=db_config["dbname"],
            user=db_config["user"],
            password=db_config["password"],
            connect_timeout=10,
        )
        logger.info(
            "Database connection established successfully to host: %s, database: %s",
            db_config["host"],
            db_config["dbname"],
        )
        return connection

    except Exception:
        # Avoid logging the raw exception as it may contain connection URIs or credentials
        logger.error("Database connection failure occurred.")
        raise DatabaseConnectionError(
            "Failed to connect to the database. Verify network availability and credentials."
        ) from None
