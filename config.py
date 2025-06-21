import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# Ưu tiên đọc key từ st.secrets (cho deployment), nếu không có thì đọc từ .env (cho local)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

GENERATIVE_MODEL_NAME = 'gemini-pro'
EMBEDDING_MODEL_NAME = 'models/embedding-001'
TEXT_CHUNK_SIZE = 800
TEXT_CHUNK_OVERLAP = 100
VECTOR_DB_SEARCH_RESULTS = 5
CHROMA_DB_PATH = "./pnote_chroma_db"
