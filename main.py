import sqlite3
import sys
from pathlib import Path
from typing import Optional

import loguru
import pydantic
#
#
#
from loguru import logger
from pydantic import BaseModel

from models.countries import Countries
#
#
# from customer_model import Customer
from program_settings import ProgramSettings


def get_all_tables(db_path: str):
    """Fetch all table names from the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return tables


def get_table_schema(db_path: str, table_name: str):
    """Fetch the schema of a specific table."""
    msg = f'getting table schema for {table_name}'
    logger.debug(msg)
    logger.info(msg)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    schema = cursor.fetchall()  # Returns column details

    cursor.close()
    conn.close()

    return schema


def generate_pydantic_model(table_name: str, schema):
    """Generate a Pydantic model based on the SQLite table schema."""
    msg = f'generating Pydantic model for {table_name} using schema {schema}'
    logger.debug(msg)
    logger.info(msg)

    class_attrs = {}

    for col in schema:
        col_name = col[1]
        if col_name is None:
            continue
        msg = f'Examining column {col_name}'
        logger.debug(msg)
        logger.info(msg)

        col_type = col[2].upper()

        # Map SQLite types to Python types
        if "INT" in col_type:
            field_type = int
        elif "CHAR" in col_type or "TEXT" in col_type:
            field_type = str
        elif "REAL" in col_type or "DOUBLE" in col_type or "FLOAT" in col_type:
            field_type = float
        elif "BLOB" in col_type:
            field_type = bytes
        else:
            field_type = Optional[str]  # Default fallback

        class_attrs[col_name] = (field_type, None)

    return type(table_name.capitalize(), (BaseModel,), class_attrs)


def generate_all_models(db_path: str):
    """Generate Pydantic models for all tables in a SQLite database."""
    tables = get_all_tables(db_path)
    models = {}

    for table in tables:
        msg = f"Generating Pydantic models for {table}"
        logger.debug(msg)
        logger.info(msg)
        schema = get_table_schema(db_path, table)
        models[table] = generate_pydantic_model(table, schema)

    return models


def get_python_version() -> str:
    return f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'


def start_logging():
    log_format: str = '{time} - {name} - {level} - {function} - {message}'
    logger.remove()
    logger.add('formatted_log.txt', format = log_format, rotation = '10 MB', retention = '5 days')
    # Add a handler that logs only DEBUG messages to stdout
    logger.add(sys.stdout, level = "DEBUG", filter = lambda record: record["level"].name == "DEBUG")


def find_file(filename: str, search_path: str = '.'):
    msg = f'Searching for file {filename} starts at directory: {search_path}'
    return next(Path(search_path).rglob(filename), None)


def sqlite_to_pydantic(db_path: str):
    # Example
    # print("from pydantic import BaseModel\nfrom typing import Any\n")
    # sqlite_to_pydantic("your_database.db")

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for (table_name,) in tables:
            print(f"\nclass {table_name.capitalize()}(BaseModel):")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                name, type_ = col[1], col[2]
                py_type = sqlite_type_to_python(type_)
                print(f"    {name}: {py_type}")


def sqlite_type_to_python(sqlite_type: str) -> str:
    mapping = {
        "INTEGER": "int",
        "REAL": "float",
        "TEXT": "str",
        "BLOB": "bytes",
        "NUMERIC": "float",
    }
    return mapping.get(sqlite_type.upper(), "Any")


def display_all_countries(db_path):

    with sqlite3.connect(db_path) as conn:

        # Make rows accessible by column name
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Execute query
        cursor.execute("SELECT * FROM countries")
        rows = cursor.fetchall()

        # Iterate and create Pydantic models
        for row in rows:
            # Convert sqlite3.Row to dict
            country_data = dict(row)

            # Load into Pydantic model
            country = Countries(**country_data)

            msg = str(country)
            logger.debug(msg)
            logger.info(msg)


def main():
    start_logging()

    msg = f'Python version: {get_python_version()}'
    logger.debug(msg)
    logger.info(msg)

    msg = f'Pydantic version: {pydantic.__version__}'
    logger.debug(msg)
    logger.info(msg)

    msg = f'Loguru version: {loguru.__version__}'
    logger.debug(msg)
    logger.info(msg)

    db_file_name = ProgramSettings.get_setting('SQLITE_DATABASE_FILE_NAME')
    msg = f'Database file: {db_file_name}'
    logger.debug(msg)
    logger.info(msg)

    db_path = find_file(db_file_name, '.')
    msg = f'Database path: {db_path}'
    logger.debug(msg)
    logger.info(msg)

    #ONE TIME: sqlite_to_pydantic(db_path)
    display_all_countries(db_path)


"""    
    models = generate_all_models(db_path)

    # Display the generated models
    for table, model in models.items():
        print(f"✅ Pydantic Model for Table: {table}")
        print(model.model_json_schema(), "\n")
"""

if __name__ == '__main__':
    main()
