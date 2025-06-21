# Ghi chú: Điểm khởi chạy chính, rất gọn gàng.
import streamlit as st
from config import GEMINI_API_KEY
from utils.state import initialize_session_state
from ui.sidebar import display_sidebar
from ui.main_content import display_main_content

def load_css(file_name):
    """Hàm để đọc file CSS và inject vào app."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    """Hàm chính để chạy ứng dụng PNote."""
    st.set_page_config(
        page_title="PNote - Trợ lý học tập",
        page_icon="📝",
        layout="wide"
    )
    
    # BỔ SUNG: Gọi hàm load_css
    load_css("styles.css")
    
    # Kiểm tra API Key
    if not GEMINI_API_KEY or "YOUR_API_KEY" in GEMINI_API_KEY:
        st.error("Lỗi: API Key của Gemini chưa được cấu hình. Vui lòng kiểm tra file .env của bạn.")
        st.stop()

    try:
        initialize_session_state()
        display_sidebar()
        display_main_content()
    except Exception as e:
        st.error(f"Đã xảy ra lỗi không mong muốn. Vui lòng thử lại. Lỗi: {e}")

if __name__ == "__main__":
    main()
