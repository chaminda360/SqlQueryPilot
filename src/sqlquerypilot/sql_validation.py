import re
import sqlglot
from logger import get_logger

# Setup logger
logger = get_logger(__name__)

def validate_sql(sql_query):
    """Validate SQL query to ensure it only contains allowed operations."""
    allowed_operations = ["SELECT", "WHERE", "LIMIT", "OFFSET", "ORDER BY", "JOIN"]
    for operation in allowed_operations:
        if operation.lower() in sql_query.lower():
            logger.info("SQL query validated successfully.")
            return True
    logger.error("Invalid SQL Query: Only SELECT queries are allowed.")
    raise Exception("Invalid SQL Query: Only SELECT queries are allowed.")

def sanitize_input(input_string):
    """Sanitize user input to prevent SQL injection."""
    sanitized_input = re.sub(r"[;\\-\\-\\/*]", "", input_string)
    logger.info("User input sanitized.")
    return sanitized_input

def translate_sql(sql_query, dialect):
    """Translate SQL to the target database dialect."""
    try:
        translated_query = sqlglot.transpile(sql_query, read="mysql", write=dialect)[0]
        logger.info(f"SQL query translated to {dialect} dialect.")
        return translated_query
    except Exception as e:
        logger.error(f"SQL Translation Error: {e}")
        raise Exception(f"SQL Translation Error: {e}")
