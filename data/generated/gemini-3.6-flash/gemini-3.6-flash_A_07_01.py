import configparser
import os
import psycopg2
from psycopg2 import DatabaseError


def connect_to_db(config_file="config.ini", section="postgresql"):
    """Reads database configuration from a file and establishes a connection."""
    parser = configparser.ConfigParser()

    try:
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

        parser.read(config_file)

        db_params = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db_params[param[0]] = param[1]
        else:
            raise ValueError(
                f"Section '{section}' was not found in the '{config_file}' file."
            )

        connection = psycopg2.connect(**db_params)
        print("Database connection established successfully.")
        return connection

    except FileNotFoundError as e:
        print(f"File Error: {e}")
    except configparser.Error as e:
        print(f"Parse Error: Failed to parse '{config_file}': {e}")
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except DatabaseError as e:
        print(f"Database Connection Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None
