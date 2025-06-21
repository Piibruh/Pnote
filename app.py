# Ghi chú: Điểm khởi chạy chính, rất gọn gàng.
import streamlit as st
from config import GEMINI_API_KEY
from utils.state import initialize_session_state
from ui.sidebar import display_sidebar
from ui.main_content import display_main_content

def main():
    """Hàm chính để chạy ứng dụng PNote."""
    st.set_page_config(
        page_title="PNote - Trợ lý học tập",
        page_icon="📝",
        layout="wide"
    )

    if not GEMINI_API_KEY or "YOUR_API_KEY" in GEMINI_API_KEY:
        st.error("Lỗi: API Key của Gemini chưa được cấu hình. Vui lòng kiểm tra file config.py.")
        st.stop()

    try:
        # Khởi tạo các thành phần cốt lõi
        initialize_session_state()
        
        # Vẽ giao diện người dùng
        display_sidebar()
        display_main_content()
    except Exception as e:
        st.error(f"Đã xảy ra lỗi không mong muốn. Vui lòng thử lại. Lỗi: {e}")

if __name__ == "__main__":
    main()
