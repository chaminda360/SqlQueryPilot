# sql_generation.py
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from llm_utils import  load_api_key
import streamlit as st


def generate_sql(nl_query, schema_info):
    """Generate SQL from natural language using LangChain."""
    try:
        # Define a prompt template for natural language to SQL conversion
        prompt_template = PromptTemplate(
            input_variables=["nl_query", "schema_info"],
            template="""
            You are a SQL expert. Given the following database schema:
            {schema_info}

            Convert the following natural language query into SQL:
            {nl_query}

            Return only the SQL query without any additional explanation.
            """
        )
        api_key = load_api_key()
        if not api_key:
                st.error("⚠️ OPENAI_API_KEY is missing. Check your .env file!")
                return None
        # Initialize the LLM (e.g., OpenAI GPT)
        llm = OpenAI(api_key=api_key)  # Replace with your OpenAI API key

        # Create a LangChain LLMChain
        chain = LLMChain(llm=llm, prompt=prompt_template)

        # Generate SQL
        sql_query = chain.run(nl_query=nl_query, schema_info=schema_info)
        return sql_query.strip()
    except Exception as e:
        raise Exception(f"SQL Generation Error: {e}")