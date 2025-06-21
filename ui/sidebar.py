# Ghi chú: File này chỉ chứa code để vẽ thanh sidebar.
import streamlit as st
import time
from core.services import course_manager_service, document_processor_service

def _safe_course_name(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_').lower()

def display_sidebar():
    """Vẽ toàn bộ nội dung của sidebar và xử lý logic của nó."""
    with st.sidebar:
        st.title("📝 PNote")
        st.markdown("---")
        st.header("📚 Quản lý Khóa học")
        
        new_course_name_input = st.text_input("Tên khóa học mới", placeholder="vd: Lịch sử Đảng")
        if st.button("Tạo Khóa học"):
            # ĐÃ SỬA: Logic kiểm tra lỗi được làm chặt chẽ hơn
            if not new_course_name_input:
                st.warning("Vui lòng nhập tên khóa học.")
            else:
                safe_name = _safe_course_name(new_course_name_input)
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

        # ... (phần chọn khóa học không đổi)
        if st.session_state.courses:
            # ...
        else:
            st.info("Tạo khóa học để bắt đầu.")

        st.markdown("---")

        if st.session_state.current_course:
            st.header(f"➕ Thêm tài liệu")
            uploaded_file = st.file_uploader("1. Tải file (PDF, DOCX)", type=["pdf", "docx"])
            url_input = st.text_input("2. Nhập URL (bài báo, YouTube)", placeholder="https://...")
            # BỔ SUNG: Thêm tùy chọn dán văn bản
            pasted_text = st.text_area("3. Dán văn bản vào đây")
            
            if st.button("Xử lý và Thêm"):
                with st.spinner("⏳ Đang xử lý..."):
                    source_type, source_data = (None, None)
                    # ĐÃ SỬA: Logic ưu tiên xử lý các nguồn
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

        # ... (phần Dark Mode không đổi)
