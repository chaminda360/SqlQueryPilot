# app.py
import streamlit as st
from database import create_connection, get_schema_info, run_query
from sql_generation import generate_sql
from sql_validation import validate_sql, sanitize_input, translate_sql

def main():
    """Main function to run the Streamlit app."""
    st.title("Natural Language to SQL Query Interface")

    st.write("""
    ### Supported Databases:
    - **PostgreSQL**: `postgresql://user:password@host:port/database`
    - **MySQL**: `mysql+pymysql://user:password@host:port/database`
    - **SQL Server**: `mssql+pyodbc://user:password@host:port/database?driver=ODBC Driver 17 for SQL Server`
    - **Oracle**: `oracle+cx_oracle://user:password@host:port/service_name`
    - **SQLite**: `sqlite:///data/example.db`
    """)

    # User input for DB connection string
    db_url = st.text_input("Enter Database URL", "sqlite:///data/example.db")
    connect_button = st.button("Connect")

    # Initialize session state for connection and schema info
    if "conn" not in st.session_state:
        st.session_state.conn = None
    if "engine" not in st.session_state:
        st.session_state.engine = None
    if "schema_info" not in st.session_state:
        st.session_state.schema_info = None
    if "dialect" not in st.session_state:
        st.session_state.dialect = None

    if connect_button:
        try:
            st.session_state.conn, st.session_state.engine = create_connection(db_url)
            st.success("Connected to Database")

            # Dynamically fetch schema information
            st.session_state.schema_info = get_schema_info(st.session_state.engine)
            st.write("### Schema Information")
            st.code(st.session_state.schema_info)

            # Determine the database dialect from the connection URL
            if "postgresql" in db_url:
                st.session_state.dialect = "postgres"
            elif "mysql" in db_url:
                st.session_state.dialect = "mysql"
            elif "sqlite" in db_url:
                st.session_state.dialect = "sqlite"
            elif "oracle" in db_url:
                st.session_state.dialect = "oracle"
            elif "mssql" in db_url:
                st.session_state.dialect = "tsql"  # T-SQL for SQL Server
            else:
                st.error("Unsupported database type")
                st.session_state.dialect = None

        except Exception as e:
            st.error(f"Error: {e}")

    # Always show the "Convert and Run Query" section
    if st.session_state.conn and st.session_state.engine and st.session_state.schema_info:
        # User input for natural language query
        nl_query = st.text_area("Enter your Natural Language Query")
        if st.button("Convert and Run Query"):
            if nl_query.strip():
                # Sanitize natural language input
                nl_query = sanitize_input(nl_query)

                # Generate SQL from natural language
                sql_query = generate_sql(nl_query, st.session_state.schema_info)
                if sql_query:
                    st.write("### Generated SQL Query (Generic)")
                    st.code(sql_query)

                    # Validate SQL query
                    if validate_sql(sql_query):
                        # Translate SQL to the target database dialect
                        translated_query = translate_sql(sql_query, st.session_state.dialect)
                        if translated_query:
                            st.write(f"### Translated SQL Query ({st.session_state.dialect.capitalize()})")
                            st.code(translated_query)

                            # Execute the translated SQL safely
                            result = run_query(st.session_state.engine, translated_query)
                            if result is not None:
                                st.write("### Query Result")
                                st.dataframe(result)
            else:
                st.warning("Please enter a valid natural language query")

if __name__ == "__main__":
    main()