import psycopg2
from configparser import ConfigParser
import os


def get_db_config():
    parser = ConfigParser()

    # build absolute path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "database.conf")

    parser.read(config_path)

    db = {}
    if parser.has_section("postgresql"):
        params = parser.items("postgresql")
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section 'postgresql' not found in config file")

    return db


def get_connection():
    db_config = get_db_config()

    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"],
    )

    return conn