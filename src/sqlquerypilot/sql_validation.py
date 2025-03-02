# sql_validation.py
import re
import sqlglot

def validate_sql(sql_query):
    """Validate SQL query to ensure it only contains allowed operations."""
    allowed_operations = ["SELECT", "WHERE", "LIMIT", "OFFSET", "ORDER BY", "JOIN"]
    for operation in allowed_operations:
        if operation.lower() in sql_query.lower():
            return True
    raise Exception("Invalid SQL Query: Only SELECT queries are allowed.")

def sanitize_input(input_string):
    """Sanitize user input to prevent SQL injection."""
    sanitized_input = re.sub(r"[;\\-\\-\\\/*]", "", input_string)
    return sanitized_input

def translate_sql(sql_query, dialect):
    """Translate SQL to the target database dialect."""
    try:
        translated_query = sqlglot.transpile(sql_query, read="sql", write=dialect)[0]
        return translated_query
    except Exception as e:
        raise Exception(f"SQL Translation Error: {e}")