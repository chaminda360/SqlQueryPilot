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
    - **SQLite**: `sqlite:///example.db`
    """)

    # User input for DB connection string
    db_url = st.text_input("Enter Database URL", "sqlite:///example.db")
    connect_button = st.button("Connect")

    if connect_button:
        try:
            conn, engine = create_connection(db_url)
            st.success("Connected to Database")

            # Dynamically fetch schema information
            schema_info = get_schema_info(engine)
            st.write("### Schema Information")
            st.code(schema_info)

            # Determine the database dialect from the connection URL
            if "postgresql" in db_url:
                dialect = "postgres"
            elif "mysql" in db_url:
                dialect = "mysql"
            elif "sqlite" in db_url:
                dialect = "sqlite"
            elif "oracle" in db_url:
                dialect = "oracle"
            elif "mssql" in db_url:
                dialect = "tsql"  # T-SQL for SQL Server
            else:
                st.error("Unsupported database type")
                dialect = None

            if dialect:
                # User input for natural language query
                nl_query = st.text_area("Enter your Natural Language Query")
                if st.button("Convert and Run Query"):
                    if nl_query.strip():
                        # Sanitize natural language input
                        nl_query = sanitize_input(nl_query)

                        # Generate SQL from natural language
                        sql_query = generate_sql(nl_query, schema_info)
                        if sql_query:
                            st.write("### Generated SQL Query (Generic)")
                            st.code(sql_query)

                            # Validate SQL query
                            if validate_sql(sql_query):
                                # Translate SQL to the target database dialect
                                translated_query = translate_sql(sql_query, dialect)
                                if translated_query:
                                    st.write(f"### Translated SQL Query ({dialect.capitalize()})")
                                    st.code(translated_query)

                                    # Execute the translated SQL safely
                                    result = run_query(engine, translated_query)
                                    if result is not None:
                                        st.write("### Query Result")
                                        st.dataframe(result)
                    else:
                        st.warning("Please enter a valid natural language query")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()