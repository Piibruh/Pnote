import streamlit as st
from core.services import rag_service

def display_main_content():
    """Vẽ nội dung chính của ứng dụng."""
    if not st.session_state.current_course:
        st.info("👈 Vui lòng chọn hoặc tạo một khóa học ở thanh bên để bắt đầu.")
        return

    st.header(f"Khóa học: {st.session_state.current_course}")
    chat_tab, notes_tab, translate_tab = st.tabs(["💬 Chat với PNote", "🗒️ Bảng Ghi Chú", "🌍 Dịch Thuật"])

    with chat_tab:
        if st.session_state.current_course not in st.session_state.messages:
            st.session_state.messages[st.session_state.current_course] = [{"role": "assistant", "content": "Xin chào! Tôi sẵn sàng trả lời các câu hỏi về tài liệu của bạn."}]

        for message in st.session_state.messages[st.session_state.current_course]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Hỏi PNote điều gì đó..."):
            st.session_state.messages[st.session_state.current_course].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("PNote đang suy nghĩ..."):
                    response = rag_service.get_answer(st.session_state.current_course, prompt)
                    st.markdown(response)
            
            st.session_state.messages[st.session_state.current_course].append({"role": "assistant", "content": response})

    with notes_tab:
        current_note = st.session_state.notes.get(st.session_state.current_course, "")
        note_content = st.text_area("Viết ghi chú tại đây...", value=current_note, height=500, label_visibility="collapsed")
        
        if note_content != current_note:
            st.session_state.notes[st.session_state.current_course] = note_content
            st.toast("Đã lưu ghi chú!", icon="✅")

    with translate_tab:
        st.subheader("Công cụ Dịch Thuật Nhanh")
        col1, col2 = st.columns(2)
        
        with col1:
            text_to_translate = st.text_area("Nhập văn bản cần dịch:", height=250, key="translator_input")
            
        with col2:
            target_language = st.selectbox(
                "Dịch sang ngôn ngữ:",
                ["Tiếng Việt (Vietnamese)", "Tiếng Anh (English)", "Tiếng Nhật (Japanese)", "Tiếng Hàn (Korean)"]
            )
            
            if st.button("Dịch", use_container_width=True):
                if text_to_translate:
                    with st.spinner("Đang dịch..."):
                        lang = target_language.split('(')[-1].replace(')', '')
                        translated_text = rag_service.translate_text(text_to_translate, lang)
                        st.text_area("Kết quả:", value=translated_text, height=250, key="translator_output")
                else:
                    st.warning("Vui lòng nhập văn bản để dịch.")
