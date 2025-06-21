# Ghi chú: File này chỉ chứa code để vẽ nội dung chính (tabs).
import streamlit as st
from core.services import rag_service

def display_main_content():
    """Vẽ nội dung chính của ứng dụng."""
    if not st.session_state.current_course:
        st.info("👈 Vui lòng chọn hoặc tạo một khóa học ở thanh bên để bắt đầu.")
        return

    st.header(f"Khóa học: {st.session_state.current_course}")
    # ĐÃ SỬA: Thêm tab Dịch Thuật
    chat_tab, notes_tab, translate_tab = st.tabs(["💬 Chat với PNote", "🗒️ Bảng Ghi Chú", "🌍 Dịch Thuật"])

    with chat_tab:
        # ... (nội dung tab này không đổi)
        if st.session_state.current_course not in st.session_state.messages:
            #...
        # ...

    with notes_tab:
        # ... (nội dung tab này không đổi)
        current_note = st.session_state.notes.get(st.session_state.current_course, "")
        # ...

    # BỔ SUNG: Logic cho tab Dịch Thuật
    with translate_tab:
        st.subheader("Công cụ Dịch Thuật Nhanh")
        col1, col2 = st.columns(2)
        
        with col1:
            text_to_translate = st.text_area("Nhập văn bản cần dịch:", height=250)
            
        with col2:
            target_language = st.selectbox("Dịch sang ngôn ngữ:", ["Tiếng Việt (Vietnamese)", "Tiếng Anh (English)", "Tiếng Nhật (Japanese)", "Tiếng Hàn (Korean)"])
            
            if st.button("Dịch", use_container_width=True):
                if text_to_translate:
                    with st.spinner("Đang dịch..."):
                        # Lấy đúng tên ngôn ngữ để gửi cho API
                        lang = target_language.split('(')[-1].replace(')', '')
                        translated_text = rag_service.translate_text(text_to_translate, lang)
                        st.text_area("Kết quả:", value=translated_text, height=250, disabled=True)
                else:
                    st.warning("Vui lòng nhập văn bản để dịch.")
