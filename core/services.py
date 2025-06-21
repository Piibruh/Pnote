# Ghi chú: "Bộ não" của ứng dụng, chứa toàn bộ logic không liên quan đến giao diện.

# ==============================================================================
# ĐOẠN CODE "SILVER BULLET" ĐỂ SỬA LỖI SQLITE3 TRÊN STREAMLIT CLOUD
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# ==============================================================================

import google.generativeai as genai
import chromadb
# ... (các import khác không đổi)
from pypdf import PdfReader
import docx
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
import tiktoken
import time
from config import (
    GEMINI_API_KEY, GENERATIVE_MODEL_NAME, TEXT_CHUNK_SIZE,
    TEXT_CHUNK_OVERLAP, VECTOR_DB_SEARCH_RESULTS, CHROMA_DB_PATH
)

# --- Khởi tạo các dịch vụ toàn cục ---
# ... (phần này không đổi)
genai.configure(api_key=GEMINI_API_KEY)
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
generative_model = genai.GenerativeModel(GENERATIVE_MODEL_NAME)


class DocumentProcessor:
    """Xử lý việc trích xuất văn bản từ nhiều nguồn khác nhau."""
    def extract_text(self, source_type, source_data):
        try:
            # ... (toàn bộ nội dung class này không đổi, chỉ thêm case 'text' ở dưới)
            if source_type in ['pdf', 'docx'] and not source_data:
                return None, "Không có file nào được cung cấp."
            
            if source_type == 'pdf':
                reader = PdfReader(source_data)
                text = "".join(page.extract_text() + "\n" for page in reader.pages if page.extract_text())
                return text, source_data.name
            
            elif source_type == 'docx':
                doc = docx.Document(source_data)
                text = "\n".join([para.text for para in doc.paragraphs if para.text])
                return text, source_data.name
            
            # BỔ SUNG: Xử lý nguồn từ văn bản dán vào
            elif source_type == 'text':
                if not source_data: return None, "Không có văn bản nào được dán vào."
                return source_data, "Pasted Text"
                
            elif source_type == 'url':
                # ... (phần xử lý url và youtube không đổi)
                if not source_data: return None, "URL không được cung cấp."
                
                if "youtube.com/watch?v=" in source_data or "youtu.be/" in source_data:
                    video_id = source_data.split("v=")[-1].split('&')[0]
                    if "/" in video_id:
                        video_id = video_id.split("/")[-1]
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['vi', 'en'])
                    text = " ".join([item['text'] for item in transcript_list])
                    return text, f"YouTube Video ID: {video_id}"

                response = requests.get(source_data, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.content, 'html.parser')
                for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                    tag.decompose()
                text = ' '.join(t.get_text(separator=' ', strip=True) for t in soup.find_all(text=True))
                title = soup.title.string.strip() if soup.title else source_data
                return text, title
                
        except Exception as e:
            return None, f"Lỗi khi xử lý nguồn: {str(e)}"
        return None, "Loại nguồn không được hỗ trợ."

class CourseManager:
    # ... (Toàn bộ nội dung class này không thay đổi)
    def __init__(self, client):
        self.client = client
    # ...

class RAGService:
    """Dịch vụ thực hiện pipeline RAG và các tác vụ AI khác."""
    def __init__(self, course_manager):
        self.course_manager = course_manager

    def get_answer(self, course_id, question):
        # ... (nội dung hàm này không đổi)
        collection = self.course_manager.get_or_create_course_collection(course_id)
        
        if collection.count() == 0:
             return "Lỗi: Khóa học này chưa có tài liệu nào. Vui lòng thêm tài liệu trước khi đặt câu hỏi."

        # ...
        return # ...
    
    # BỔ SUNG: Chức năng dịch thuật
    def translate_text(self, text_to_translate, target_language="Tiếng Việt"):
        """Dịch văn bản bằng Gemini."""
        if not text_to_translate:
            return ""
        
        prompt = f"Translate the following text to {target_language}. Respond with only the translated text, no additional explanations:\n\n{text_to_translate}"
        try:
            response = generative_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Lỗi dịch thuật: {e}"

# Khởi tạo các instance của services để các module khác import
document_processor_service = DocumentProcessor()
course_manager_service = CourseManager(chroma_client)
rag_service = RAGService(course_manager_service)
