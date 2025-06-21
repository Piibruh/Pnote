# Ghi chú: "Bộ não" của ứng dụng, chứa toàn bộ logic không liên quan đến giao diện.

# ==============================================================================
# ĐOẠN CODE "SILVER BULLET" ĐỂ SỬA LỖI SQLITE3 TRÊN STREAMLIT CLOUD
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# ==============================================================================

import google.generativeai as genai
import chromadb
from pypdf import PdfReader
# ... (các import khác không thay đổi)
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

# ... (Khởi tạo dịch vụ và class DocumentProcessor, CourseManager không thay đổi)
genai.configure(api_key=GEMINI_API_KEY)
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
generative_model = genai.GenerativeModel(GENERATIVE_MODEL_NAME)

class DocumentProcessor:
    # ... (Nội dung class này giữ nguyên)
    pass

class CourseManager:
    # ... (Nội dung class này giữ nguyên)
    pass

class RAGService:
    """Dịch vụ thực hiện pipeline RAG và các tác vụ AI khác."""
    def __init__(self, course_manager):
        self.course_manager = course_manager

    def get_answer(self, course_id, question):
        """Hàm trả lời câu hỏi đã được sửa lỗi logic."""
        try:
            # ĐÃ SỬA: Dùng get_collection thay vì get_or_create để đảm bảo collection đã tồn tại.
            # Điều này sẽ báo lỗi ngay nếu có vấn đề với tên khóa học.
            collection = self.course_manager.client.get_collection(name=course_id)
            
            # Kiểm tra số lượng tài liệu một lần nữa để chắc chắn
            if collection.count() == 0:
                return "Tài liệu đã được thêm, nhưng có vẻ như đang được xử lý. Vui lòng thử lại sau ít phút hoặc thêm lại tài liệu nếu sự cố vẫn tiếp diễn."
        
            results = collection.query(query_texts=[question], n_results=VECTOR_DB_SEARCH_RESULTS)
            context_chunks = results['documents'][0]
        
            if not context_chunks:
                return "Tôi không tìm thấy thông tin liên quan trong tài liệu để trả lời câu hỏi của bạn."
            
            context = "\n---\n".join(context_chunks)
            prompt = f"""Bạn là PNote, trợ lý AI chuyên gia. Trả lời câu hỏi DỰA HOÀN TOÀN vào "NGỮ CẢNH" sau. QUY TẮC: 1. CHỈ dùng thông tin từ "NGỮ CẢNH". Nếu không có, nói: "Tôi không tìm thấy thông tin này trong tài liệu." 2. Trả lời trực tiếp, súc tích, chuyên nghiệp. 3. Không đưa ra ý kiến cá nhân. NGỮ CẢNH: --- {context} --- CÂU HỎI: "{question}" """
            
            response = generative_model.generate_content(prompt)
            return response.text
        
        except ValueError:
            # Lỗi này xảy ra khi get_collection không tìm thấy khóa học.
            return "Lỗi: Không tìm thấy khóa học này. Có thể nó chưa được tạo hoặc chưa có tài liệu nào."
        except Exception as e:
            return f"Đã xảy ra một lỗi không mong muốn khi truy vấn: {str(e)}"

    def translate_text(self, text_to_translate, target_language="Tiếng Việt"):
        # ... (nội dung hàm này giữ nguyên)
        pass

# ... (Khởi tạo các instance không thay đổi)
document_processor_service = DocumentProcessor()
course_manager_service = CourseManager(chroma_client)
rag_service = RAGService(course_manager_service)
