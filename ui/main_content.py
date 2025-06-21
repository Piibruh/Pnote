import streamlit as st
from core.services import rag_service

def display_main_content():
    """Vẽ nội dung chính của ứng dụng với bố cục 3 phần."""
    if not st.session_state.current_course:
        st.info("👈 Vui lòng chọn hoặc tạo một khóa học ở thanh bên để bắt đầu.")
        return

    # Tái cấu trúc giao diện thành 2 cột chính: Chat (rộng hơn) và Note
    chat_col, note_col = st.columns([2, 1])

    # --- CỘT CHAT (BÊN TRÁI) ---
    with chat_col:
        st.header(f"💬 Chat: {st.session_state.current_course}", anchor=False, divider="gray")

        # Khung chứa tin nhắn, đặt chiều cao cố định để có thanh cuộn
        chat_container = st.container(height=600, border=False)
        with chat_container:
            if st.session_state.current_course not in st.session_state.messages:
                st.session_state.messages[st.session_state.current_course] = [{"role": "assistant", "content": "Xin chào! Tôi sẵn sàng trả lời các câu hỏi về tài liệu của bạn."}]

            for message in st.session_state.messages[st.session_state.current_course]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Khung nhập liệu nằm bên dưới
        if prompt := st.chat_input("Hỏi PNote điều gì đó..."):
            # Thêm tin nhắn vào state và rerender để hiển thị ngay lập tức
            st.session_state.messages[st.session_state.current_course].append({"role": "user", "content": prompt})
            st.rerun()

            # Xử lý và nhận câu trả lời từ bot (sẽ hiển thị ở lần rerun tiếp theo)
            # Dòng này sẽ không được thực thi ngay do st.rerun() ở trên
            # Chúng ta sẽ xử lý logic này một cách khác
    
    # Xử lý logic trả lời của bot sau khi tin nhắn người dùng đã được hiển thị
    last_message = st.session_state.messages[st.session_state.current_course][-1]
    if last_message["role"] == "user":
        with chat_container: # Vẽ lại trong cùng container
             with st.chat_message("assistant"):
                with st.spinner("PNote đang suy nghĩ..."):
                    response = rag_service.get_answer(st.session_state.current_course, last_message["content"])
                    st.markdown(response)
        st.session_state.messages[st.session_state.current_course].append({"role": "assistant", "content": response})
        st.rerun() # Rerun một lần nữa để lưu trạng thái cuối cùng


    # --- CỘT NOTE (BÊN PHẢI) ---
    with note_col:
        st.header("🗒️ Ghi chú", anchor=False, divider="gray")
        
        current_note = st.session_state.notes.get(st.session_state.current_course, "")
        note_content = st.text_area(
            "Viết các ghi chú, ý chính tại đây...",
            value=current_note,
            height=525,  # Chiều cao tương ứng với khung chat
            label_visibility="collapsed"
        )
        
        if note_content != current_note:
            st.session_state.notes[st.session_state.current_course] = note_content
            st.toast("Đã lưu ghi chú!", icon="✅")

        # Thêm Tab Dịch Thuật bên dưới phần Note
        st.markdown("---")
        st.subheader("🌍 Dịch Thuật Nhanh", anchor=False)
        text_to_translate = st.text_area("Văn bản cần dịch:", height=100)
        target_language = st.selectbox("Dịch sang:", ["Tiếng Việt (Vietnamese)", "Tiếng Anh (English)", "Tiếng Nhật (Japanese)"])

        if st.button("Dịch", use_container_width=True):
            if text_to_translate:
                with st.spinner("Đang dịch..."):
                    lang = target_language.split('(')[-1].replace(')', '')
                    translated_text = rag_service.translate_text(text_to_translate, lang)
                    st.text_area("Kết quả:", value=translated_text, height=100)
            else:
                st.warning("Vui lòng nhập văn bản để dịch.")
