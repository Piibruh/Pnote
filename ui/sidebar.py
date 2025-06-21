import streamlit as st
import time
from core.services import course_manager_service, document_processor_service

def _safe_course_name(name):
    """Tạo tên hợp lệ cho collection, loại bỏ ký tự đặc biệt."""
    return "".join(c for c in name if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_').lower()

def display_sidebar():
    """Vẽ toàn bộ nội dung của sidebar và xử lý logic của nó."""
    with st.sidebar:
        st.title("📝 PNote")
        st.markdown("---")
        st.header("📚 Quản lý Khóa học", anchor=False)
        
        new_course_name_input = st.text_input("Tên khóa học mới", placeholder="vd: Lập trình Python")
        if st.button("Tạo Khóa học"):
            if not new_course_name_input:
                st.warning("Vui lòng nhập tên khóa học.")
            else:
                safe_name = _safe_course_name(new_course_name_input)
                if len(safe_name) < 3:
                    st.error("Lỗi: Tên khóa học phải có ít nhất 3 ký tự (chữ hoặc số).")
                elif safe_name in st.session_state.courses:
                    st.warning(f"Khóa học '{safe_name}' đã tồn tại.")
                else:
                    # Tạo collection rỗng trước để đăng ký tên
                    course_manager_service.get_or_create_course_collection(safe_name)
                    st.session_state.courses.append(safe_name)
                    st.session_state.current_course = safe_name
                    st.success(f"Đã tạo '{safe_name}'!")
                    time.sleep(1)
                    st.rerun()

        if st.session_state.courses:
            try:
                current_index = st.session_state.courses.index(st.session_state.current_course)
            except (ValueError, TypeError):
                current_index = 0
            
            selected_course = st.selectbox("Chọn khóa học", options=st.session_state.courses, index=current_index, label_visibility="collapsed")
            if selected_course != st.session_state.current_course:
                st.session_state.current_course = selected_course
                st.rerun()
        else:
            st.info("Tạo một khóa học để bắt đầu.")

        st.markdown("---")

        if st.session_state.current_course:
            st.header(f"➕ Thêm tài liệu", anchor=False)
            uploaded_file = st.file_uploader("1. Tải file (PDF, DOCX)", type=["pdf", "docx"])
            url_input = st.text_input("2. Nhập URL (bài báo, YouTube)", placeholder="https://...")
            pasted_text = st.text_area("3. Dán văn bản vào đây")
            
            if st.button("Xử lý và Thêm"):
                with st.spinner("⏳ Đang xử lý..."):
                    source_type, source_data = (None, None)
                    if uploaded_file:
                        source_type, source_data = uploaded_file.name.split('.')[-1], uploaded_file
                    elif url_input:
                        source_type, source_data = 'url', url_input
                    elif pasted_text:
                        source_type, source_data = 'text', pasted_text
                    
                    if source_type and source_data:
                        text, source_name = document_processor_service.extract_text(source_type, source_data)
                        if text:
                            chunks_added = course_manager_service.add_document(st.session_state.current_course, text, source_name)
                            st.success(f"Đã thêm {chunks_added} kiến thức từ '{source_name}'.")
                            st.toast("Tải lại trang nếu cần để cập nhật bộ nhớ chat.", icon="🔄")
                        else: st.error(f"Lỗi: {source_name}")
                    else:
                        st.warning("Vui lòng cung cấp tài liệu.")
        
        st.markdown("---")
        st.header("🎨 Giao diện", anchor=False)

        if 'theme' not in st.session_state:
            st.session_state.theme = 'dark'

        is_dark = st.toggle("Chế độ Tối", value=(st.session_state.theme == 'dark'))
        
        js_code = f'<script>document.body.classList.{"add" if is_dark else "remove"}("dark-mode");</script>'
        st.markdown(js_code, unsafe_allow_html=True)
        st.session_state.theme = 'dark' if is_dark else 'light'
