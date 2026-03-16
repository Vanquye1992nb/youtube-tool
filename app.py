import streamlit as st
import google.generativeai as genai

# --- GIAO DIỆN ---
st.set_page_config(page_title="Tool Youtube Văn Thế Web AI", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); color: black !important; font-weight: bold; border-radius: 12px; height: 3.5em; border: none; }
    .header-title { color: #f1c40f; text-align: center; font-size: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="header-title">🖥️ Tool Tìm Key Youtube Văn Thế Web AI</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🔑 Cấu hình")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")

chu_de = st.text_input("# Chủ Đề", placeholder="vd: Hoạt hình, Mukbang")
so_luong = st.number_input("🔍 Số lượng", min_value=5, max_value=30, value=10)

if st.button("🚀 TÌM KIẾM TỪ KHÓA NÂNG CAO"):
    if not api_key:
        st.error("Vui lòng nhập API Key!")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # --- ĐOẠN CODE QUAN TRỌNG NHẤT ĐỂ SỬA LỖI 404 ---
            # Tự động quét danh sách model mà Key của bạn được phép dùng
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # Ưu tiên chọn 1.5-flash, nếu không có thì lấy đại cái đầu tiên (thường là gemini-pro)
            selected_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models else models[0]
            
            model = genai.GenerativeModel(selected_model)
            
            with st.spinner(f'Đang phân tích bằng {selected_model}...'):
                prompt = f"Tìm {so_luong} từ khóa SEO Youtube cho chủ đề '{chu_de}'. Trả về bảng gồm: STT, Từ khóa, Độ khó, Lượt tìm kiếm."
                response = model.generate_content(prompt)
                st.success("Đã tìm thấy kết quả!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Lỗi: {str(e)}")
            st.info("Hãy thử tạo lại API Key mới tại aistudio.google.com nếu vẫn lỗi.")

st.caption("© 2026 Developed for Van The Web Team")
