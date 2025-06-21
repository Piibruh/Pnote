# Ghi chú: File này chứa tất cả các hằng số và cấu hình của ứng dụng.
import os
import streamlit as st # Bổ sung import streamlit

# Dòng load_dotenv không còn cần thiết trên server, nhưng giữ lại cũng không sao
# vì nó giúp app vẫn chạy được ở local.
from dotenv import load_dotenv
load_dotenv()

# --- Cấu hình API và Model ---
# ĐÃ SỬA: Ưu tiên đọc key từ st.secrets của Streamlit Cloud,
# nếu không có thì mới đọc từ file .env (dành cho local).
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

GENERATIVE_MODEL_NAME = 'gemini-pro'
EMBEDDING_MODEL_NAME = 'models/embedding-001'

# --- Cấu hình xử lý văn bản (RAG) ---
TEXT_CHUNK_SIZE = 800
TEXT_CHUNK_OVERLAP = 100
VECTOR_DB_SEARCH_RESULTS = 5

# --- Cấu hình ứng dụng ---
CHROMA_DB_PATH = "./pnote_chroma_db"
