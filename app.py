import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="AI Youtube Keyword Tool", layout="wide")

# CSS tạo giao diện Dark Mode giống ảnh mẫu
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { 
        width: 100%; background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); 
        color: black !important; font-weight: bold; border-radius: 12px; height: 3.5em; border: none;
    }
    .header-title { color: #f1c40f; text-align: center; font-size: 35px; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #1e2130; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- PHẦN TIÊU ĐỀ ---
st.markdown('<p class="header-title">🖥️ Tool Tìm Key Youtube Văn Thế Web AI</p>', unsafe_allow_html=True)

# --- SIDEBAR (CỘT TRÁI) ---
with st.sidebar:
    st.header("🔑 Cấu hình")
    api_key = st.text_input("Dán Gemini API Key:", type="password")
    st.info("Lấy key tại: aistudio.google.com")

# --- LAYOUT NHẬP LIỆU ---
col1, col2 = st.columns(2)

with col1:
    chu_de = st.text_input("# Chủ Đề (Bắt buộc)", placeholder="vd: Hoạt hình, Sinh tồn")
    st.button("💡 Gợi ý chủ đề")
    tu_khoa = st.text_input("# Từ Khóa Chính (Tùy chọn)", placeholder="vd: tu tiên, rèn luyện")

with col2:
    ngon_ngu = st.selectbox("🌐 Ngôn Ngữ", ["Tiếng Việt", "English"])
    doi_tuong = st.selectbox("👥 Đối Tượng", ["View Việt", "View Quốc Tế"])
    so_luong = st.number_input("🔍 Số lượng", min_value=5, max_value=50, value=10)

# --- NÚT BẤM VÀ XỬ LÝ LỖI 404 ---
if st.button("🚀 TÌM KIẾM TỪ KHÓA NÂNG CAO"):
    if not api_key:
        st.error("Vui lòng dán API Key vào cột bên trái!")
    elif not chu_de:
        st.warning("Vui lòng nhập chủ đề!")
    else:
        try:
            # Cấu hình AI
            genai.configure(api_key=api_key)
            
            # SỬA LỖI 404: Thử dùng gemini-pro (ổn định nhất) 
            # Nếu muốn dùng 1.5 flash, đảm bảo thư viện đã được cập nhật
            model = genai.GenerativeModel('gemini-pro') 
            
            with st.spinner('AI đang phân tích...'):
                prompt = f"""
                Bạn là chuyên gia SEO Youtube. Hãy tìm {so_luong} từ khóa cho chủ đề '{chu_de}' 
                với từ khóa chính '{tu_khoa}'. Ngôn ngữ: {ngon_ngu}. 
                Trả về bảng gồm: STT, Từ khóa, Độ khó (%), Lượt tìm kiếm, Xu hướng.
                """
                response = model.generate_content(prompt)
                
                st.success("Hoàn tất!")
                st.markdown(response.text)
                
        except Exception as e:
            # Nếu lỗi 404 vẫn xảy ra, thông báo cách xử lý cho người dùng
            st.error(f"Lỗi: {str(e)}")
            st.info("Mẹo: Hãy đảm bảo bạn đã tạo file requirements.txt trên GitHub để cài đặt thư viện cần thiết.")

st.markdown("---")
st.caption("© 2026 Developed for Van The Web Team")
