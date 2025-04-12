import sqlite3
from pydantic import BaseModel
from typing import Optional

import sys
from pathlib import Path

#
import pymongo
#
from bson import ObjectId
#
from loguru import logger
#
from pymongo import MongoClient
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database
#
#from customer_model import Customer
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

# Example Usage
def main():
    start_logging()

    msg = f'Python version: {get_python_version()}'
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

    """
    conn = sqlite3.connect(db_path)
    msg = f'connection: {conn=}'
    logger.debug(msg)
    logger.info(msg)
    """

    models = generate_all_models(db_path)

    # Display the generated models
    for table, model in models.items():
        print(f"✅ Pydantic Model for Table: {table}")
        print(model.model_json_schema(), "\n")


if __name__ == '__main__':
    main()