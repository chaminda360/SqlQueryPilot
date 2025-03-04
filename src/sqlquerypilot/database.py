import sqlalchemy
from sqlalchemy import inspect
import pandas as pd
import os
from logger import get_logger

# Setup logger
logger = get_logger(__name__)

def create_connection(db_url):
    """Create a database connection."""
    try:
        # If the database URL is for SQLite, ensure the ./data directory exists
        if db_url.startswith("sqlite:///"):
            db_path = db_url.replace("sqlite:///", "")
            data_dir = os.path.dirname(db_path)
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir)  # Create the ./data directory if it doesn't exist

        engine = sqlalchemy.create_engine(db_url, connect_args={})
        conn = engine.connect()
        logger.info(f"Connected to database: {db_url}")
        return conn, engine
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise Exception(f"Error connecting to database: {e}")

def get_schema_info(engine):
    """Fetch schema information from the database."""
    try:
        inspector = inspect(engine)
        schema_info = ""
        for table_name in inspector.get_table_names():
            schema_info += f"Table: {table_name}\n"
            for column in inspector.get_columns(table_name):
                schema_info += f"- Column: {column['name']} ({column['type']})\n"
            schema_info += "\n"
        logger.info("Fetched schema information successfully.")
        return schema_info
    except Exception as e:
        logger.error(f"Schema Inspection Error: {e}")
        raise Exception(f"Schema Inspection Error: {e}")

def run_query(engine, query, params=None):
    """Execute a SQL query safely using parameterized queries."""
    try:
        with engine.connect() as conn:
            if params:
                result = pd.read_sql(sqlalchemy.text(query), conn, params=params)
            else:
                result = pd.read_sql(query, conn)
            logger.info("Query executed successfully.")
            return result
    except Exception as e:
        logger.error(f"Query Execution Error: {e}")
        raise Exception(f"Query Execution Error: {e}")
