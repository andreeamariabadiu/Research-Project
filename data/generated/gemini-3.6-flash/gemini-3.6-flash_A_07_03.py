import configparser
import psycopg2
from psycopg2 import Error


def connect_to_database(config_file="database.ini", section="postgresql"):
    """Reads database configuration from a file and establishes a connection.

    :param config_file: Path to the configuration file (e.g., .ini format)
    :param section: Section in the config file containing DB parameters
    :return: psycopg2 connection object or None if connection fails
    """
    config = configparser.ConfigParser()
    connection = None

    try:
        # Load the configuration file
        read_files = config.read(config_file)
        if not read_files:
            raise FileNotFoundError(
                f"Configuration file '{config_file}' not found or is empty."
            )

        # Check if section exists
        if not config.has_section(section):
            raise KeyError(
                f"Section '{section}' not found in '{config_file}'."
            )

        # Extract connection parameters
        db_params = dict(config.items(section))

        # Connect to the database
        print(f"Connecting to the database using section [{section}]...")
        connection = psycopg2.connect(**db_params)
        print("Database connection successful.")
        return connection

    except FileNotFoundError as err:
        print(f"[File Error]: {err}")
    except KeyError as err:
        print(f"[Config Error]: {err}")
    except Error as err:
        print(f"[Database Error]: Failed to connect to database - {err}")
    except Exception as err:
        print(f"[Unexpected Error]: {err}")

    return None
