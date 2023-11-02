import argparse
from sqlalchemy import create_engine, text
from application import get_sqlalchemy_db_url
from sqlalchemy.exc import SQLAlchemyError


def connection_db():
    try:
        db_url = get_sqlalchemy_db_url()
        engine = create_engine(db_url)
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        return None


def get_all_columns_by_query(table_name, connection):
    result = connection.execute(text(
        f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND column_name <> 'id'"
    ))
    return [row[0] for row in result]


def parse_data():
    connection = connection_db()
    parser = argparse.ArgumentParser(description='Script for deleting or masking data from a database')
    parser.add_argument('--action', choices=['delete', 'mask'], help='Operation to be performed')
    parser.add_argument('--table', help='Name of the table from which data will be deleted or masked')
    parser.add_argument('--percentage', type=float, default=0, help='Percentage of data to be deleted (default: 0)')
    parser.add_argument('--columns', nargs='+', default=[], help='Columns to be masked')

    parser.add_argument('--run_mode', default=None)

    command_line_args = parser.parse_args()

    return command_line_args, connection
