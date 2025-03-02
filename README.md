# SqlQueryPilot -Natural Language to SQL Query Interface

## Overview
The SqlQueryPilot application allows users to interact with SQL databases using natural language queries. It converts natural language inputs into SQL queries, executes them on the specified database, and returns the results. The application supports multiple database types, including **PostgreSQL**, **MySQL**, **SQLite**, **Oracle**, and **Microsoft SQL Server**. It also includes features to prevent SQL injection and ensure secure query execution.

---

## Features
1. **Natural Language to SQL Conversion**:
   - Converts natural language queries (e.g., "Show me all customers from New York") into SQL queries using a Large Language Model (LLM) via LangChain.

2. **Multi-Database Support**:
   - Works with the following databases:
     - **PostgreSQL**
     - **MySQL**
     - **SQLite**
     - **Oracle**
     - **Microsoft SQL Server**

3. **Dynamic Schema Handling**:
   - Automatically fetches schema information (tables, columns, and data types) from the connected database.

4. **SQL Dialect Translation**:
   - Translates generated SQL queries into the appropriate dialect for the target database.

5. **SQL Validation and Sanitization**:
   - Validates SQL queries to ensure they only contain allowed operations (e.g., `SELECT`, `WHERE`, `LIMIT`).
   - Sanitizes user inputs to prevent SQL injection attacks.

6. **Streamlit User Interface**:
   - Provides an intuitive web interface for users to input natural language queries and view results.

---

## How It Works
1. **User Input**:
   - The user provides a database connection URL and a natural language query.

2. **Schema Fetching**:
   - The application dynamically fetches the schema information from the connected database.

3. **SQL Generation**:
   - The natural language query is converted into SQL using an LLM (e.g., OpenAI GPT).

4. **SQL Validation**:
   - The generated SQL is validated to ensure it only contains allowed operations.

5. **SQL Translation**:
   - The SQL query is translated into the appropriate dialect for the target database.

6. **Query Execution**:
   - The translated SQL query is executed on the database, and the results are displayed to the user.

---

## Supported Databases
The application supports the following databases:
- **PostgreSQL**: `postgresql://user:password@host:port/database`
- **MySQL**: `mysql+pymysql://user:password@host:port/database`
- **SQLite**: `sqlite:///example.db`
- **Oracle**: `oracle+cx_oracle://user:password@host:port/service_name`
- **Microsoft SQL Server**: `mssql+pyodbc://user:password@host:port/database?driver=ODBC Driver 17 for SQL Server`

---

## Future Tasks
1. **Fine-Tune Validation Rules**:
   - Adjust the whitelist of allowed SQL operations based on the application's requirements.

2. **Logging and Monitoring**:
   - Log all SQL queries and errors for auditing and debugging purposes.

3. **User Permissions**:
   - Ensure the database user account used by the application has limited permissions (e.g., read-only access).

4. **Testing**:
   - Test the application with various inputs to ensure SQL injection is prevented and the application behaves as expected.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/natural-language-to-sql.git
   cd natural-language-to-sql
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   - Rename the `.env.example` file to `.env`.
   - Add your OpenAI API key to the `.env` file:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

# Usage

## Steps to Use the Application

1. **Open the Application**:
   - Open the application in your web browser.

2. **Enter the Database Connection URL**:
   - Provide the connection URL for your database (e.g., `sqlite:///data/example.db`).

3. **Connect to the Database**:
   - Click **Connect** to establish a connection to the database.

4. **Enter a Natural Language Query**:
   - In the text area provided, enter a natural language query (e.g., "Show me all customers from New York").

5. **Convert and Run the Query**:
   - Click **Convert and Run Query** to generate and execute the SQL query.

6. **View the Results**:
   - The results of the query will be displayed in the application.

---

## Example

### Input:
- **Database URL**: `sqlite:///data/example.db`
- **Natural Language Query**: "Show me all customers from New York"

### Output:
#### Generated SQL (Generic):
```sql
SELECT * FROM customers WHERE city = 'New York';
````

# Query Result Example

## Example Output
| id  | name       | city      |
|-----|------------|-----------|
| 1   | John Doe   | New York  |
| 2   | Jane Smith | New York  |
