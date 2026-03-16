import streamlit as st
import google.generativeai as genai

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="AI Youtube Tool - Văn Thế Web", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { 
        width: 100%; background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%); 
        color: white !important; font-weight: bold; border-radius: 12px; height: 3.5em; border: none;
    }
    .header-title { color: #f1c40f; text-align: center; font-size: 32px; font-weight: bold; }
    .stTextInput>div>div>input, .stSelectbox>div>div>div { background-color: #1e2130 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="header-title">🖥️ Tool Tìm Key Youtube Quốc Tế - Văn Thế Web AI</p>', unsafe_allow_html=True)

# --- 2. THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.header("🔑 Cấu hình")
    api_key = st.text_input("Dán Gemini API Key:", type="password")
    st.info("Lấy key miễn phí tại aistudio.google.com")

# --- 3. BỘ LỌC TÙY CHỈNH (THÊM MỸ & CHÂU ÂU) ---
col1, col2 = st.columns(2)

with col1:
    chu_de = st.text_input("# Chủ Đề (Bắt buộc)", placeholder="vd: Minecraft, Relaxing Music, Cooking")
    tu_khoa = st.text_input("# Từ Khóa Phụ", placeholder="vd: ASMR, tutorial, challenge")

with col2:
    ngon_ngu = st.selectbox("🌐 Ngôn Ngữ", ["English", "Tiếng Việt", "Japanese", "German", "French"])
    # Thêm lựa chọn khu vực Mỹ và Châu Âu
    khu_vuc = st.selectbox("🌍 Khu Vực Server (Thị trường)", [
        "Mỹ (USA - High CPM)", 
        "Châu Âu (Europe)", 
        "Toàn Cầu (Global)", 
        "Việt Nam"
    ])
    so_luong = st.number_input("🔍 Số lượng từ khóa", min_value=5, max_value=50, value=15)

# --- 4. XỬ LÝ DỮ LIỆU ---
if st.button("🚀 PHÂN TÍCH THỊ TRƯỜNG QUỐC TẾ"):
    if not api_key:
        st.error("Vui lòng nhập API Key ở cột bên trái!")
    elif not chu_de:
        st.warning("Vui lòng nhập chủ đề!")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Tự động lấy model khả dụng
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            target_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
            
            model = genai.GenerativeModel(target_model)
            
            with st.spinner(f'Đang quét dữ liệu thị trường {khu_vuc}...'):
                # Prompt được tối ưu để AI tập trung vào Insight vùng miền
                prompt = f"""
                Bạn là chuyên gia Marketing YouTube hàng đầu. Phân tích chủ đề '{chu_de}' 
                tại thị trường '{khu_vuc}' với ngôn ngữ '{ngon_ngu}'.
                
                Yêu cầu:
                1. Tìm {so_luong} từ khóa/cụm từ khóa có CPC cao và độ cạnh tranh thấp tại {khu_vuc}.
                2. Trả về bảng Markdown: STT | Từ khóa | Độ khó (%) | Lượng tìm kiếm tháng | Tiềm năng CPM.
                3. Gợi ý 5 Tiêu đề (Title) chuẩn SEO cho thị trường này.
                4. Phân tích ngắn gọn hành vi khán giả tại {khu_vuc} đối với chủ đề này.
                """
                response = model.generate_content(prompt)
                
                st.success(f"✅ Đã phân tích xong thị trường {khu_vuc}!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Lỗi: {str(e)}")

st.markdown("---")
st.caption("© 2026 Developed for Van The Web Team - Global SEO Version")
