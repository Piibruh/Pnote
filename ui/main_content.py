import streamlit as st
from core.services import rag_service

def display_main_content():
    """Vẽ nội dung chính của ứng dụng với bố cục 3 phần ổn định."""
    if not st.session_state.current_course:
        st.info("👈 Vui lòng chọn hoặc tạo một khóa học ở thanh bên để bắt đầu.")
        return

    # Khởi tạo các state cần thiết cho khóa học hiện tại
    if st.session_state.current_course not in st.session_state.messages:
        st.session_state.messages[st.session_state.current_course] = [{"role": "assistant", "content": "Xin chào! Tôi sẵn sàng trả lời các câu hỏi về tài liệu của bạn."}]
    if st.session_state.current_course not in st.session_state.notes:
        st.session_state.notes[st.session_state.current_course] = ""

    # Tái cấu trúc giao diện thành 2 cột chính: Chat (rộng hơn) và Note/Tools
    chat_col, tools_col = st.columns([2, 1])

    # --- CỘT CHAT (BÊN TRÁI) ---
    with chat_col:
        st.header(f"💬 Chat: {st.session_state.current_course}", anchor=False, divider="gray")

        # Khung chứa tin nhắn, đặt chiều cao cố định để có thanh cuộn
        chat_container = st.container(height=600, border=False)
        with chat_container:
            for message in st.session_state.messages[st.session_state.current_course]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Khung nhập liệu nằm bên dưới
        if prompt := st.chat_input("Hỏi PNote điều gì đó..."):
            st.session_state.messages[st.session_state.current_course].append({"role": "user", "content": prompt})
            with chat_container: # Vẽ lại tin nhắn người dùng ngay lập tức
                with st.chat_message("user"):
                    st.markdown(prompt)
            
            # Xử lý và nhận câu trả lời từ bot
            with chat_container:
                 with st.chat_message("assistant"):
                    with st.spinner("PNote đang suy nghĩ..."):
                        response = rag_service.get_answer(st.session_state.current_course, prompt)
                        st.markdown(response)
            st.session_state.messages[st.session_state.current_course].append({"role": "assistant", "content": response})
            # Không cần rerun vì Streamlit tự xử lý state của chat_message

    # --- CỘT CÔNG CỤ (NOTE VÀ DỊCH THUẬT - BÊN PHẢI) ---
    with tools_col:
        st.header("🗒️ Ghi chú", anchor=False, divider="gray")
        
        note_content = st.text_area(
            "Viết các ghi chú, ý chính tại đây...",
            value=st.session_state.notes[st.session_state.current_course],
            height=300,
            label_visibility="collapsed"
        )
        if note_content != st.session_state.notes[st.session_state.current_course]:
            st.session_state.notes[st.session_state.current_course] = note_content
            st.toast("Đã lưu ghi chú!", icon="✅")

        st.markdown("---")
        st.header("🌍 Dịch Thuật", anchor=False, divider="gray")
        text_to_translate = st.text_area("Văn bản cần dịch:", height=100)
        target_language = st.selectbox("Dịch sang:", ["Tiếng Việt (Vietnamese)", "Tiếng Anh (English)", "Tiếng Nhật (Japanese)"])

        if st.button("Dịch", use_container_width=True):
            if text_to_translate:
                with st.spinner("Đang dịch..."):
                    lang = target_language.split('(')[-1].replace(')', '')
                    translated_text = rag_service.translate_text(text_to_translate, lang)
                    st.text_area("Kết quả:", value=translated_text, height=100, disabled=True)
            else:
                st.warning("Vui lòng nhập văn bản để dịch.")
