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
    
    load_css("styles.css")
    
    if not GEMINI_API_KEY:
        st.error("Lỗi: API Key của Gemini chưa được cấu hình. Vui lòng kiểm tra mục Secrets trên Streamlit Cloud hoặc file .env của bạn.")
        st.stop()

    try:
        initialize_session_state()
        display_sidebar()
        display_main_content()
    except Exception as e:
        st.error(f"Đã xảy ra lỗi không mong muốn. Vui lòng thử lại. Lỗi: {e}")

if __name__ == "__main__":
    main()
