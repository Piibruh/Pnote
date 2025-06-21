import streamlit as st
import time
from core.services import course_manager_service, document_processor_service

def _safe_course_name(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_').lower()

def display_sidebar():
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
                    course_manager_service.get_or_create_course_collection(safe_name)
                    st.session_state.courses.append(safe_name)
                    st.session_state.current_course = safe_name
                    st.success(f"Đã tạo '{safe_name}'!")
                    time.sleep(0.5); st.rerun()

        if st.session_state.courses:
            try:
                current_index = st.session_state.courses.index(st.session_state.current_course)
            except (ValueError, TypeError): current_index = 0
            selected_course = st.selectbox("Chọn khóa học", options=st.session_state.courses, index=current_index, label_visibility="collapsed")
            if selected_course != st.session_state.current_course:
                st.session_state.current_course = selected_course
                st.rerun()
        else:
            st.info("Tạo một khóa học để bắt đầu.")

        st.markdown("---")

        if st.session_state.current_course:
            st.header(f"➕ Thêm tài liệu", anchor=False)
            # ĐÃ SỬA: Cho phép upload nhiều file
            uploaded_files = st.file_uploader("1. Tải file (PDF, DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
            url_input = st.text_input("2. Nhập URL (bài báo, YouTube)", placeholder="https://...")
            pasted_text = st.text_area("3. Dán văn bản vào đây", placeholder="Dán nội dung từ clipboard...")
            
            if st.button("Xử lý và Thêm", use_container_width=True):
                with st.spinner("⏳ Đang xử lý..."):
                    processed_count = 0
                    # ĐÃ SỬA: Logic xử lý nhiều file và các nguồn khác
                    if uploaded_files:
                        for file in uploaded_files:
                            file_type = file.name.split('.')[-1]
                            text, source_name = document_processor_service.extract_text(file_type, file)
                            if text:
                                course_manager_service.add_document(st.session_state.current_course, text, source_name)
                                processed_count += 1
                    if url_input:
                        text, source_name = document_processor_service.extract_text('url', url_input)
                        if text:
                            course_manager_service.add_document(st.session_state.current_course, text, source_name)
                            processed_count += 1
                    if pasted_text:
                        text, source_name = document_processor_service.extract_text('text', pasted_text)
                        if text:
                            course_manager_service.add_document(st.session_state.current_course, text, source_name)
                            processed_count += 1
                    
                    if processed_count > 0:
                        st.success(f"Hoàn tất! Đã thêm thành công {processed_count} nguồn tài liệu.")
                        # ĐÃ SỬA: Thêm sleep và rerun để giải quyết dứt điểm lỗi state
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.warning("Không có tài liệu nào hợp lệ để xử lý.")
        
        # ... (Phần Giao diện / Dark Mode giữ nguyên)
