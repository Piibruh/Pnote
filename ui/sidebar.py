# Ghi chú: File này chỉ chứa code để vẽ thanh sidebar.
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
        st.header("📚 Quản lý Khóa học")
        
        new_course_name_input = st.text_input("Tên khóa học mới", placeholder="vd: Lịch sử Đảng")
        if st.button("Tạo Khóa học"):
            if not new_course_name_input:
                st.warning("Vui lòng nhập tên khóa học.")
            else:
                safe_name = _safe_course_name(new_course_name_input)
                # Kiểm tra nếu tên sau khi xử lý bị rỗng
                if not safe_name:
                    st.error("Tên khóa học không hợp lệ. Vui lòng dùng chữ cái hoặc số.")
                elif safe_name in st.session_state.courses:
                    st.warning(f"Khóa học '{safe_name}' đã tồn tại.")
                else:
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
            
            selected_course = st.selectbox("Chọn khóa học", options=st.session_state.courses, index=current_index)
            if selected_course != st.session_state.current_course:
                st.session_state.current_course = selected_course
                st.rerun()
        else:
            st.info("Tạo khóa học để bắt đầu.")

        st.markdown("---")

        if st.session_state.current_course:
            st.header(f"➕ Thêm tài liệu")
            uploaded_file = st.file_uploader("1. Tải file (PDF, DOCX)", type=["pdf", "docx"])
            url_input = st.text_input("2. Nhập URL (bài báo, YouTube)", placeholder="https://...")
            pasted_text = st.text_area("3. Dán văn bản vào đây")
            
            if st.button("Xử lý và Thêm"):
                with st.spinner("⏳ Đang xử lý..."):
                    source_type, source_data = (None, None)
                    # Ưu tiên xử lý theo thứ tự: file -> url -> text
                    if uploaded_file:
                        source_type = uploaded_file.name.split('.')[-1]
                        source_data = uploaded_file
                    elif url_input:
                        source_type = 'url'
                        source_data = url_input
                    elif pasted_text:
                        source_type = 'text'
                        source_data = pasted_text
                    
                    if source_type and source_data:
                        text, source_name = document_processor_service.extract_text(source_type, source_data)
                        if text:
                            chunks_added = course_manager_service.add_document(st.session_state.current_course, text, source_name)
                            st.success(f"Đã thêm {chunks_added} kiến thức từ '{source_name}'.")
                        else:
                            st.error(f"Lỗi: {source_name}")
                    else:
                        st.warning("Vui lòng cung cấp tài liệu.")

        # Phần Dark Mode, được đặt ở cuối sidebar
        st.markdown("---")
        st.header("🎨 Giao diện")

        if 'theme' not in st.session_state:
            st.session_state.theme = 'light'

        is_dark = st.toggle("Bật Chế độ Tối", value=(st.session_state.theme == 'dark'))
        
        if is_dark:
            st.session_state.theme = 'dark'
            st.markdown('<script>document.body.classList.add("dark-mode");</script>', unsafe_allow_html=True)
        else:
            st.session_state.theme = 'light'
            st.markdown('<script>document.body.classList.remove("dark-mode");</script>', unsafe_allow_html=True)
