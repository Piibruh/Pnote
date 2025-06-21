# Ghi chú: "Bộ não" của ứng dụng, chứa toàn bộ logic xử lý dữ liệu và AI.
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import google.generativeai as genai
import chromadb
from pypdf import PdfReader
import docx
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
import tiktoken
import time
import re
from unicodedata import normalize
from config import (
    GEMINI_API_KEY, GENERATIVE_MODEL_NAME, TEXT_CHUNK_SIZE,
    TEXT_CHUNK_OVERLAP, VECTOR_DB_SEARCH_RESULTS, CHROMA_DB_PATH
)

# BỔ SUNG: Hàm xử lý tên file Tiếng Việt và các ký tự đặc biệt
def slugify(value):
    """
    Chuyển đổi chuỗi Unicode (bao gồm Tiếng Việt) thành một chuỗi an toàn
    để dùng làm ID hoặc tên file.
    """
    value = normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value

# --- Khởi tạo các dịch vụ toàn cục ---
genai.configure(api_key=GEMINI_API_KEY)
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
generative_model = genai.GenerativeModel(GENERATIVE_MODEL_NAME)

class DocumentProcessor:
    def extract_text(self, source_type, source_data):
        try:
            safe_name = "unknown_source"
            if source_type in ['pdf', 'docx']:
                if not source_data: return None, "Không có file nào được cung cấp."
                # ĐÃ SỬA: Xử lý tên file Tiếng Việt
                safe_name = slugify(source_data.name)
                if source_type == 'pdf':
                    reader = PdfReader(source_data)
                    text = "".join(page.extract_text() + "\n" for page in reader.pages if page.extract_text())
                    return text, safe_name
                elif source_type == 'docx':
                    doc = docx.Document(source_data)
                    text = "\n".join([para.text for para in doc.paragraphs if para.text])
                    return text, safe_name
            elif source_type == 'text':
                if not source_data: return None, "Không có văn bản nào được dán vào."
                return source_data, "pasted-text"
            elif source_type == 'url':
                # ... (phần xử lý url và youtube không đổi)
                pass # Giữ nguyên logic cũ
        except Exception as e:
            return None, f"Lỗi khi xử lý nguồn: {str(e)}"
        return None, "Loại nguồn không được hỗ trợ."

class CourseManager:
    # ... (Nội dung class này giữ nguyên)
    pass

class RAGService:
    def __init__(self, course_manager):
        self.course_manager = course_manager

    def get_answer(self, course_id, question):
        try:
            # ĐÃ SỬA: Logic kiểm tra mạnh mẽ hơn
            collection = self.course_manager.client.get_collection(name=course_id)
            if collection.count() == 0:
                # Đây là lỗi state, không phải lỗi người dùng.
                return "Hệ thống đang xử lý dữ liệu. Vui lòng đợi trong giây lát và thử lại."
            results = collection.query(query_texts=[question], n_results=VECTOR_DB_SEARCH_RESULTS)
            # ... (phần còn lại của hàm không đổi)
        except ValueError:
            return "Lỗi: Không tìm thấy khóa học này. Có thể nó đã bị xóa hoặc chưa được tạo."
        except Exception as e:
            return f"Đã xảy ra một lỗi không mong muốn khi truy vấn: {str(e)}"
            
    def translate_text(self, text_to_translate, target_language="Tiếng Việt"):
        # ... (nội dung hàm này giữ nguyên)
        pass

# ... (Khởi tạo các instance không thay đổi)
document_processor_service = DocumentProcessor()
course_manager_service = CourseManager(chroma_client)
rag_service = RAGService(course_manager_service)
