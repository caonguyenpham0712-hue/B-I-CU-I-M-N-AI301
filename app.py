"""
DATALENS STUDIO · SENIOR BA DATA ANALYTICS AGENT
Giao diện Cao cấp (Luxury Modern Glassmorphism & Editorial Typography)
ĐỒNG BỘ 100% PHÔNG CHỮ: PLUS JAKARTA SANS (CHUẨN TIẾNG VIỆT UNICODE TOÀN HỆ THỐNG)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import io
from datetime import datetime

from core.agent_pipeline import EnterpriseAnalyticsAgent
from database.memory_store import AgentMemoryStore

# ==============================================================
# 1. CẤU HÌNH TRANG & ĐỒNG BỘ 100% PHÔNG CHỮ (PLUS JAKARTA SANS)
# ==============================================================
st.set_page_config(
    page_title="DataLens Studio · Phân tích dữ liệu doanh nghiệp",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Đồng bộ tuyệt đối font Plus Jakarta Sans trên toàn bộ giao diện
st.markdown("""
<style>
    /* Nạp font chữ Plus Jakarta Sans chuẩn tiếng Việt đa dạng trọng lượng 300 - 800 */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap');

    /* Ép đồng bộ font chữ trên MỌI phần tử của Streamlit */
    *, html, body, [class*="st-"], [class*="css-"], button, input, select, textarea, p, span, h1, h2, h3, h4, h5, h6, div, label, table, th, td, .stMarkdown, .stSelectbox, .stTextInput, .stTextArea, .stRadio, .stButton, .stDownloadButton, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        text-rendering: optimizeLegibility !important;
    }

    /* Bảng màu chủ đạo Luxury Pastel & Warm Minimalist */
    :root {
        --bg-main: #FAF5F5;
        --text-dark: #2A1D23;
        --text-muted: #6B5560;
        --text-light: #8E7883;
        --rose-primary: #C86D7F;
        --rose-deep: #A74C5E;
        --rose-soft: #FDE8ED;
        --rose-pill: #ECC9D2;
        --champagne: #F5E5D8;
        --card-bg: rgba(255, 255, 255, 0.95);
        --card-border: rgba(240, 218, 224, 0.85);
        --glass-shadow: 0 16px 40px -12px rgba(180, 115, 130, 0.14);
    }

    /* Toàn bộ app */
    .stApp {
        background: radial-gradient(circle at 12% 8%, #FDF0F3 0%, transparent 45%),
                    radial-gradient(circle at 90% 12%, #FAF0E8 0%, transparent 40%),
                    radial-gradient(circle at 50% 90%, #F8EBF0 0%, transparent 55%),
                    #FAF5F5;
        color: var(--text-dark);
    }

    /* Ẩn header mặc định streamlit */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Thanh Sidebar phong cách Warm Minimalist */
    section[data-testid="stSidebar"] {
        background: rgba(255, 252, 252, 0.92) !important;
        border-right: 1px solid rgba(235, 215, 220, 0.8) !important;
        backdrop-filter: blur(20px);
    }

    /* Floating Pill Header */
    .floating-nav {
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 235, 240, 0.9);
        border-radius: 9999px;
        padding: 10px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 8px 30px rgba(185, 130, 145, 0.1);
        margin-bottom: 25px;
    }
    .brand-title {
        font-size: 21px;
        font-weight: 800;
        color: var(--text-dark);
        letter-spacing: -0.03em;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .brand-pill-tag {
        background: linear-gradient(135deg, #FDE8ED, #FCE0E7);
        color: var(--rose-deep);
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 9999px;
        border: 1px solid #F5C6D2;
    }

    /* Hero Section kiểu Editorial hiện đại */
    .editorial-hero {
        text-align: center;
        padding: 18px 20px 28px 20px;
        max-width: 840px;
        margin: 0 auto;
    }
    .hero-kicker {
        font-size: 11.5px;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--rose-deep);
        margin-bottom: 8px;
    }
    .hero-heading {
        font-size: clamp(32px, 4.2vw, 46px);
        font-weight: 800;
        color: var(--text-dark);
        line-height: 1.18;
        letter-spacing: -0.03em;
        margin-bottom: 12px;
    }
    .hero-sub {
        font-size: 15px;
        font-weight: 400;
        color: var(--text-muted);
        line-height: 1.65;
        margin-bottom: 0px;
    }

    /* Thẻ quy trình Step Pills Navigation */
    .step-stepper {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 28px;
        flex-wrap: wrap;
    }
    .step-pill {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(235, 215, 222, 0.85);
        border-radius: 9999px;
        padding: 8px 20px;
        font-size: 12.5px;
        font-weight: 650;
        color: var(--text-muted);
        display: inline-flex;
        align-items: center;
        gap: 7px;
        transition: all 0.25s ease;
        box-shadow: 0 4px 12px rgba(180, 130, 145, 0.05);
    }
    .step-pill.active {
        background: linear-gradient(135deg, var(--rose-primary), var(--rose-deep));
        color: #FFFFFF !important;
        border-color: var(--rose-deep);
        box-shadow: 0 6px 18px rgba(167, 76, 94, 0.3);
    }
    .step-pill.done {
        background: #FDF1F4;
        color: var(--rose-deep);
        border-color: #F8CAD5;
    }

    /* Thẻ Card Trắng Mượt (Luxury Glass Cards) */
    .lux-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        box-shadow: var(--glass-shadow);
        padding: 26px 28px;
        margin-bottom: 22px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .lux-card:hover {
        box-shadow: 0 20px 45px -12px rgba(180, 110, 130, 0.18);
    }
    .lux-card-title {
        font-size: 19px;
        font-weight: 750;
        color: var(--text-dark);
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }
    .lux-card-desc {
        font-size: 13.5px;
        color: var(--text-muted);
        line-height: 1.6;
        margin-bottom: 16px;
    }

    /* Metric Luxury Card */
    .lux-metric {
        background: #FFFFFF;
        border: 1px solid #F4E2E6;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 6px 20px rgba(190, 140, 155, 0.07);
        text-align: center;
    }
    .lux-metric-label {
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--text-light);
        margin-bottom: 6px;
    }
    .lux-metric-val {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.025em;
        color: var(--text-dark);
        margin-bottom: 4px;
    }
    .lux-metric-delta {
        font-size: 12px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 9999px;
        display: inline-block;
    }
    .delta-neg { background: #FDE8ED; color: #BE185D; }
    .delta-pos { background: #EDFBF4; color: #047857; }

    /* Nút bấm Pill Button */
    .stButton>button {
        border-radius: 9999px !important;
        font-weight: 650 !important;
        font-size: 13.5px !important;
        padding: 9px 24px !important;
        letter-spacing: 0.01em !important;
        border: 1px solid #E5CBD2 !important;
        transition: all 0.25s ease !important;
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #C86D7F, #A74C5E) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(167, 76, 94, 0.28) !important;
    }
    .stButton>button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(167, 76, 94, 0.38) !important;
    }

    /* Ô nhập liệu */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 12px !important;
        border: 1px solid #E5CBD2 !important;
        font-size: 14px !important;
        color: var(--text-dark) !important;
    }

    /* Hộp cảnh báo kiểu sang trọng */
    .lux-alert-crit {
        background: #FFF2F4;
        border: 1px solid #F9CBD4;
        border-left: 5px solid #BE185D;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 15px;
    }
    .lux-alert-warn {
        background: #FFFBF2;
        border: 1px solid #FBE8C4;
        border-left: 5px solid #D97706;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================
# 2. KHỞI TẠO SERVICES & CACHE STATE
# ==============================================================
@st.cache_resource
def get_agent():
    return EnterpriseAnalyticsAgent()

@st.cache_resource
def get_memory():
    return AgentMemoryStore()

agent = get_agent()
memory = get_memory()

# Quản lý Trạng thái Session
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "approved_step" not in st.session_state:
    st.session_state.approved_step = 0
if "role" not in st.session_state:
    st.session_state.role = "CEO"
if "business_context" not in st.session_state:
    st.session_state.business_context = {
        "industry": "Bán lẻ Thực phẩm & Đồ uống (Chuỗi Nova Mart)",
        "background": "Chuỗi 8 siêu thị toàn quốc. Vừa qua ghi nhận sụt giảm nghiêm trọng doanh số tại TP.HCM (Khu vực Miền Nam).",
        "questions": "Tại sao doanh thu Miền Nam tuần qua sụt giảm mạnh?\nCửa hàng nào kéo tụt doanh số nhiều nhất?\nYếu tố thời tiết mưa ngập và đứt hàng ảnh hưởng ra sao?"
    }
if "cleaning_config" not in st.session_state:
    st.session_state.cleaning_config = {
        "trim": True,
        "empty": True,
        "duplicates": True,
        "incomplete": True
    }

# Nạp dữ liệu phân tích mặc định
if "analysis_data" not in st.session_state:
    with st.spinner("Đang kích hoạt quy trình phân tích dữ liệu 6 bước..."):
        st.session_state.analysis_data = agent.run(
            user_query=st.session_state.business_context["questions"].split("\n")[0],
            user_role=st.session_state.role
        )

data = st.session_state.analysis_data

# ==============================================================
# 3. SIDEBAR TINH TẾ (LUXURY MINIMALIST NAVIGATION)
# ==============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 15px 0 20px 0;">
        <div style="font-size:23px; font-weight:800; color:#2A1D23; letter-spacing:-0.03em;">DataLens</div>
        <div style="font-size:11px; font-weight:800; letter-spacing:0.18em; text-transform:uppercase; color:#A74C5E;">STUDIO · ANALYTICS</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style="font-size:11px; font-weight:750; color:#8E7883; letter-spacing:0.12em; margin-bottom:10px;">QUY TRÌNH PHÂN TÍCH</div>""", unsafe_allow_html=True)
    
    steps_meta = [
        {"idx": 0, "title": "1. Kết nối & Bối cảnh", "sub": "Xác định mục tiêu", "icon": "🌸"},
        {"idx": 1, "title": "2. Làm sạch & Cách ly", "sub": "Kiểm định chất lượng", "icon": "✨"},
        {"idx": 2, "title": "3. Phân tích & Gốc rễ", "sub": "Bóc tách nguyên nhân", "icon": "💎"},
        {"idx": 3, "title": "4. Báo cáo & Xuất tệp", "sub": "Tóm tắt & Chiến lược", "icon": "🎀"}
    ]

    for s in steps_meta:
        is_cur = (st.session_state.current_step == s["idx"])
        is_done = (s["idx"] < st.session_state.approved_step)
        btn_type = "primary" if is_cur else "secondary"
        tag = "🟢 Đang xem" if is_cur else ("✅ Đã duyệt" if is_done else "")
        btn_text = f"{s['icon']} {s['title']} {tag}"
        
        if st.button(btn_text, key=f"side_step_{s['idx']}", use_container_width=True, type=btn_type):
            st.session_state.current_step = s["idx"]
            st.rerun()

    st.markdown("---")
    st.markdown("""<div style="font-size:11px; font-weight:750; color:#8E7883; letter-spacing:0.12em; margin-bottom:8px;">BẢO MẬT & PHÂN QUYỀN (RBAC)</div>""", unsafe_allow_html=True)
    role_map = {
        "CEO": "👑 CEO (Toàn quyền, Masked PII)",
        "REGIONAL_DIRECTOR_SOUTH": "📍 Giám đốc Miền Nam",
        "REGIONAL_DIRECTOR_NORTH": "📍 Giám đốc Miền Bắc",
        "DATA_ADMIN": "🛡️ Data Admin (Toàn quyền + PII)"
    }
    sel_role = st.selectbox(
        "Vai trò truy cập:",
        options=list(role_map.keys()),
        format_func=lambda x: role_map[x],
        index=list(role_map.keys()).index(st.session_state.role)
    )
    if sel_role != st.session_state.role:
        st.session_state.role = sel_role
        st.session_state.analysis_data = agent.run(
            user_query=st.session_state.business_context["questions"].split("\n")[0],
            user_role=sel_role
        )
        st.rerun()

    st.markdown("---")
    if st.button("🔄 Phiên Phân Tích Mới", use_container_width=True):
        st.session_state.current_step = 0
        st.session_state.approved_step = 0
        st.rerun()

# ==============================================================
# 4. HEADER CHÍNH (FLOATING GLASS PILL & EDITORIAL HERO)
# ==============================================================

# Floating Glass Navbar
st.markdown("""
<div class="floating-nav">
    <div class="brand-title">
        <span>✨ DataLens <span style="font-weight:400; color:#C86D7F;">Studio</span></span>
        <span class="brand-pill-tag">Bản Quyền AI301</span>
    </div>
    <div style="display:flex; align-items:center; gap:16px;">
        <span style="font-size:12.5px; color:#6B5560; font-weight:550;">
            🛡️ Dữ liệu bảo mật & Cách ly an toàn
        </span>
        <span style="width:8px; height:8px; border-radius:50%; background:#10B981; display:inline-block;"></span>
    </div>
</div>
""", unsafe_allow_html=True)

# Editorial Hero Section
st.markdown("""
<div class="editorial-hero">
    <div class="hero-kicker">Enterprise Business Intelligence & Root-Cause AI Agent</div>
    <h1 class="hero-heading">Khám phá thấu đáo dữ liệu kinh doanh của bạn.</h1>
    <p class="hero-sub">
        Quy trình chuẩn hóa 6 bước hỗ trợ ban lãnh đạo bóc tách nguyên nhân sụt giảm, kiểm định dữ liệu sạch và đề xuất chiến lược thực thi.
    </p>
</div>
""", unsafe_allow_html=True)

# Stepper Navigation Bar
step_names = ["1. Kết nối & Bối cảnh", "2. Làm sạch & Cách ly", "3. Phân tích & Gốc rễ", "4. Báo cáo & Xuất tệp"]
step_pills_html = '<div class="step-stepper">'
for i, name in enumerate(step_names):
    cls = "step-pill"
    if i == st.session_state.current_step:
        cls += " active"
    elif i < st.session_state.approved_step:
        cls += " done"
    step_pills_html += f'<div class="{cls}">{name}</div>'
step_pills_html += '</div>'
st.markdown(step_pills_html, unsafe_allow_html=True)

# ==============================================================
# 5. CHI TIẾT TỪNG BƯỚC QUY TRÌNH (STEP WORKSPACE)
# ==============================================================

# -------------------------------------------------------------
# BƯỚC 1: KẾT NỐI (Bối Cảnh & Semantic Layer)
# -------------------------------------------------------------
if st.session_state.current_step == 0:
    st.markdown("""
    <div class="lux-card">
        <div class="lux-card-title">1. Bối cảnh Doanh nghiệp & Bài toán Nghiệp vụ</div>
        <div class="lux-card-desc">Thiết lập ngữ cảnh kinh doanh để AI Agent lựa chọn chính xác chỉ số KPI và bảng dữ liệu tương ứng.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        ind = st.text_input("Loại hình doanh nghiệp / Ngành hàng:", value=st.session_state.business_context["industry"])
        bg = st.text_area("Bối cảnh vận hành (Thông tin bổ sung):", value=st.session_state.business_context["background"], height=80)
    with col2:
        ques = st.text_area("Câu hỏi / Vấn đề cần giải đáp (Mỗi câu một dòng):", value=st.session_state.business_context["questions"], height=160)

    st.session_state.business_context["industry"] = ind
    st.session_state.business_context["background"] = bg
    st.session_state.business_context["questions"] = ques

    st.markdown("""
    <div class="lux-card">
        <div class="lux-card-title">2. Hiểu Ý định & Ánh Xạ Semantic Layer (AI Reasoning)</div>
        <div class="lux-card-desc">AI Agent tự động phân tích thực thể, công thức tính toán và cấu trúc bảo mật.</div>
    </div>
    """, unsafe_allow_html=True)

    p1 = data["step1_parsed_context"]
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lux-metric-label">LOẠI Ý ĐỊNH (INTENT)</div>
            <div style="font-size:16px; font-weight:750; color:#A74C5E;">{p1['intent_type']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lux-metric-label">VÙNG MIỀN BÓC TÁCH</div>
            <div style="font-size:16px; font-weight:750; color:#2A1D23;">{p1.get('region', 'Toàn quốc')}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lux-metric-label">CHỈ SỐ KPI MỤC TIÊU</div>
            <div style="font-size:16px; font-weight:750; color:#2A1D23;">{p1['metric_info']['display_name']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Công thức tính chuẩn theo Semantic Catalog:")
    st.code(p1['metric_info']['formula_sql'], language="sql")

    st.markdown("""
    <div class="lux-card">
        <div class="lux-card-title">3. Xem trước Nguồn Dữ liệu (Enterprise DW)</div>
        <div class="lux-card-desc">Kho dữ liệu SQLite giả lập hơn 14,000 giao dịch. Toàn bộ thông tin cá nhân (PII) đã được che bảo mật.</div>
    </div>
    """, unsafe_allow_html=True)

    clean_preview = data["step3_clean_df"]
    st.dataframe(clean_preview[["transaction_id", "order_date", "store_name", "region", "customer_name", "phone_number", "sku_code", "quantity", "net_revenue"]].head(6), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_c1, col_c2 = st.columns([2, 3])
    with col_c1:
        if st.button("Xác Nhận Nguồn Và Tiếp Tục ➔", type="primary", use_container_width=True):
            st.session_state.approved_step = max(st.session_state.approved_step, 1)
            st.session_state.current_step = 1
            st.rerun()

# -------------------------------------------------------------
# BƯỚC 2: LÀM SẠCH (Data Profiling & Quarantine Sandbox)
# -------------------------------------------------------------
elif st.session_state.current_step == 1:
    st.markdown("""
    <div class="lux-card">
        <div class="lux-card-title">Quy Chuẩn Kiểm Định & Cách Ly Dữ Liệu Bẩn (Data Quarantine)</div>
        <div class="lux-card-desc">Dữ liệu được đưa qua Python Sandbox để phát hiện doanh thu âm bất thường, trùng lặp ID, hoặc thiếu khóa ngoại và cách ly an toàn.</div>
    </div>
    """, unsafe_allow_html=True)

    dq = data["step3_dq_metrics"]
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lux-metric-label">TỔNG BẢN GHI NGUỒN</div>
            <div class="lux-metric-val">{dq['total_records']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lux-metric-label">DÒNG SẠCH HỢP LỆ</div>
            <div class="lux-metric-val" style="color:#047857;">{dq['clean_records']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lux-metric-label">DÒNG BỊ CÁCH LY</div>
            <div class="lux-metric-val" style="color:#BE185D;">{dq['dirty_records']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lux-metric-label">ĐIỂM CHẤT LƯỢNG DQ</div>
            <div class="lux-metric-val" style="color:#A74C5E;">{dq['quality_score']}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    t_clean, t_dirty = st.tabs(["✅ Tập Dữ Liệu Sạch (Clean Dataset)", "⚠️ Kho Cách Ly Dữ Liệu Lỗi (Quarantine Log)"])
    with t_clean:
        st.dataframe(data["step3_clean_df"][["transaction_id", "order_date", "store_name", "product_name", "quantity", "gross_sales", "net_revenue"]].head(8), use_container_width=True)
    with t_dirty:
        st.dataframe(data["step3_quarantine_df"][["transaction_id", "order_date", "store_name", "gross_sales", "net_revenue", "quarantine_reasons"]], use_container_width=True)
        st.caption("Các lỗi phát hiện tự động: ERR_NEGATIVE_REVENUE, ERR_DUPLICATE_TRANSACTION_ID, ERR_MISSING_FOREIGN_KEY.")

    st.markdown("<br>", unsafe_allow_html=True)
    cb1, cb2, _ = st.columns([1, 2, 3])
    with cb1:
        if st.button("⬅ Nguồn Dữ Liệu", use_container_width=True):
            st.session_state.current_step = 0
            st.rerun()
    with cb2:
        if st.button("Xác Nhận Làm Sạch Và Tiếp Tục ➔", type="primary", use_container_width=True):
            st.session_state.approved_step = max(st.session_state.approved_step, 2)
            st.session_state.current_step = 2
            st.rerun()

# -------------------------------------------------------------
# BƯỚC 3: PHÂN TÍCH CHUYÊN SÂU & TÌM GỐC RỄ
# -------------------------------------------------------------
elif st.session_state.current_step == 2:
    st.markdown("""
    <div class="lux-card">
        <div class="lux-card-title">Phân Rã Biến Động & Tìm Nguyên Nhân Gốc Rễ (Deep Analytics)</div>
        <div class="lux-card-desc">Thực hiện phân rã đóng góp (Contribution Analysis), định luật Pareto 80/20 và tương quan với các biến ngoại cảnh.</div>
    </div>
    """, unsafe_allow_html=True)

    kpi = data["step4_analytics"]["kpi_summary"]
    km1, km2, km3, km4 = st.columns(4)
    with km1:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lux-metric-label">DOANH THU THUẦN</div>
            <div class="lux-metric-val">{kpi['current_revenue']/1e6:,.1f}M</div>
            <span class="lux-metric-delta delta-neg">{kpi['growth_revenue_pct']:+,.2f}% WoW</span>
        </div>
        """, unsafe_allow_html=True)
    with km2:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lux-metric-label">LƯỢNG ĐƠN HÀNG</div>
            <div class="lux-metric-val">{kpi['current_orders']:,}</div>
            <span class="lux-metric-delta delta-neg">{kpi['growth_orders_pct']:+,.2f}% WoW</span>
        </div>
        """, unsafe_allow_html=True)
    with km3:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lux-metric-label">AOV (ĐƠN TRUNG BÌNH)</div>
            <div class="lux-metric-val">{kpi['current_aov']:,.0f} đ</div>
            <span class="lux-metric-delta delta-pos">{kpi['growth_aov_pct']:+,.2f}% WoW</span>
        </div>
        """, unsafe_allow_html=True)
    with km4:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lux-metric-label">BIÊN LỢI NHUẬN GỘP</div>
            <div class="lux-metric-val">{kpi['current_margin']:.1f}%</div>
            <span style="font-size:12px; color:#6B5560; font-weight:600;">{(kpi['current_margin'] - kpi['baseline_margin']):+,.1f}% diff</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c_w, c_p = st.columns(2)
    with c_w:
        st.plotly_chart(data["step5_waterfall"], use_container_width=True)
    with c_p:
        st.plotly_chart(data["step5_pareto"], use_container_width=True)

    st.markdown("""
    <div class="lux-card">
        <div class="lux-card-title">Bằng Chứng Định Lượng (Business Evidence & Correlation)</div>
        <div class="lux-card-desc">Bóc tách các yếu tố ngoại cảnh tác động trực tiếp vào doanh thu.</div>
    </div>
    """, unsafe_allow_html=True)

    ext_corr = data["step4_analytics"].get("external_correlation", {})
    e1, e2 = st.columns(2)
    with e1:
        st.markdown(f"""
        <div class="lux-metric" style="text-align:left;">
            <div class="lux-metric-label">🌧️ TƯƠNG QUAN MƯA BÃO VS LƯỢT KHÁCH</div>
            <div style="font-size:20px; font-weight:800; color:#BE185D;">r = {ext_corr.get('corr_traffic_vs_rainy_hours')}</div>
            <small style="color:#6B5560;">Tương quan nghịch rất mạnh: Mưa lớn ngập lụt kéo giảm hơn 55% lượt khách ghé cửa hàng.</small>
        </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown(f"""
        <div class="lux-metric" style="text-align:left;">
            <div class="lux-metric-label">👥 TƯƠNG QUAN KHÁCH ĐẾN VS DOANH THU</div>
            <div style="font-size:20px; font-weight:800; color:#047857;">r = +{ext_corr.get('corr_traffic_vs_revenue')}</div>
            <small style="color:#6B5560;">Tương quan thuận rất mạnh: Khẳng định thiếu hụt lượt khách trực tiếp gây sụt giảm doanh số.</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cb1, cb2, _ = st.columns([1, 2, 3])
    with cb1:
        if st.button("⬅ Làm Sạch", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    with cb2:
        if st.button("Xác Nhận Và Tạo Báo Cáo ➔", type="primary", use_container_width=True):
            st.session_state.approved_step = max(st.session_state.approved_step, 3)
            st.session_state.current_step = 3
            st.rerun()

# -------------------------------------------------------------
# BƯỚC 4: BÁO CÁO ĐIỀU HÀNH & XUẤT TỆP
# -------------------------------------------------------------
elif st.session_state.current_step == 3:
    st.markdown("""
    <div class="lux-card">
        <div class="lux-card-title">Báo Cáo Điều Hành (Executive Summary) & Cảnh Báo Rủi Ro</div>
        <div class="lux-card-desc">Tổng hợp thông tin điều hành theo chuẩn Minto Pyramid: [Hiện trạng] ➔ [Nguyên nhân cốt lõi] ➔ [Đề xuất hành động].</div>
    </div>
    """, unsafe_allow_html=True)

    # Hiển thị cảnh báo rủi ro chủ động
    alerts = data.get("step6_alerts", [])
    if alerts:
        for a in alerts:
            if a["level"] == "CRITICAL":
                st.markdown(f"""
                <div class="lux-alert-crit">
                    <strong style="color:#9D174D; font-size:14px;">🔥 [{a['level']}] {a['title']}</strong><br>
                    <span style="font-size:13px; color:#831843;">{a['message']}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="lux-alert-warn">
                    <strong style="color:#B45309; font-size:14px;">⚠️ [{a['level']}] {a['title']}</strong><br>
                    <span style="font-size:13px; color:#78350F;">{a['message']}</span>
                </div>
                """, unsafe_allow_html=True)

    # Biểu đồ chuỗi thời gian & dự phóng phục hồi
    st.plotly_chart(data["step5_forecast"], use_container_width=True)

    # Bản Executive Summary trình bày đẹp mắt
    st.markdown("""<div class="lux-card">""", unsafe_allow_html=True)
    st.markdown(data["step5_executive_summary"])
    st.markdown("""</div>""", unsafe_allow_html=True)

    # Nút xuất tệp
    st.markdown("""
    <div class="lux-card">
        <div class="lux-card-title">📥 Xuất Báo Cáo & Dữ Liệu Nghiệp Vụ</div>
        <div class="lux-card-desc">Tải dữ liệu hoàn chỉnh để phục vụ báo cáo hội đồng quản trị hoặc bàn giao cho các phòng ban thực thi.</div>
    </div>
    """, unsafe_allow_html=True)

    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button(
            label="📥 Tải Báo Cáo Hoàn Chỉnh (Excel .xlsx)",
            data=data["step6_excel_bytes"],
            file_name=f"DataLens_Executive_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )
    with dl2:
        st.download_button(
            label="📄 Tải Dữ Liệu Sạch (CSV Chuẩn Hóa)",
            data=data["step3_clean_df"].to_csv(index=False).encode("utf-8-sig"),
            file_name=f"Clean_Data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Ghi nhận phản hồi chuyên gia (Human-in-the-loop)
    st.markdown("""
    <div class="lux-card" style="margin-top:20px;">
        <div class="lux-card-title">💬 Vòng Lặp Phản Hồi Chuyên Gia (Human-in-the-loop)</div>
        <div class="lux-card-desc">Đánh giá của bạn được lưu vào Vector/Memory DB để tự động tối ưu hóa cho các bài toán phân tích tiếp theo.</div>
    </div>
    """, unsafe_allow_html=True)

    fb_c1, fb_c2 = st.columns([1, 2])
    with fb_c1:
        f_rate = st.radio("Đánh giá kết quả phân tích:", ["👍 Rất chính xác (Approve)", "👎 Cần bổ sung (Disapprove)"])
    with fb_c2:
        f_note = st.text_input("Ghi chú bổ sung hoặc hiệu chỉnh logic:")
        if st.button("💾 Lưu Phản Hồi Vào Bộ Nhớ AI Agent"):
            r_code = 1 if "👍" in f_rate else -1
            memory.save_feedback(
                conversation_id=data["conversation_id"],
                question=st.session_state.business_context["questions"].split("\n")[0],
                generated_sql=data["step2_queries"]["sales_transactions"],
                summary=data["step5_executive_summary"],
                rating=r_code,
                comment=f_note
            )
            st.success("🎉 Đã lưu phản hồi thành công vào Memory DB của AI Agent!")

# Footer sang trọng
st.markdown("""
<div style="text-align:center; padding: 40px 0 20px 0; color:#8E7883; font-size:12px; letter-spacing:0.04em;">
    ✨ <strong>DataLens Studio</strong> · Senior Data Business Analyst & Analytics AI Agent · Đồ án AI301
</div>
""", unsafe_allow_html=True)
