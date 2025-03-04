import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from logger import get_logger

# Setup logger
logger = get_logger(__name__)

load_dotenv()

def load_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OPENAI_API_KEY is missing. Check your .env file!")
        logger.error("OPENAI_API_KEY is missing.")
        return None
    logger.info("OPENAI_API_KEY loaded successfully.")
    return api_key
