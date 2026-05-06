import streamlit as st

# Cấu hình trang (Tối ưu cho mobile bằng layout "centered")
st.set_page_config(page_title="Tính Điểm", page_icon="📝", layout="centered")

# CSS tùy chỉnh để thu nhỏ cỡ chữ, giảm khoảng cách thừa giúp giao diện gọn hơn
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 14px; }
    .stMarkdown { margin-bottom: -15px; }
    .stTextInput>div>div>input { font-size: 14px; }
    .stNumberInput>div>div>input { font-size: 14px; }
    .stSelectbox>div>div>div { font-size: 14px; }
    .stButton>button { padding: 5px 15px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #2E86C1;'>📝 CÔNG CỤ TÍNH ĐIỂM</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 1. Ô chọn "Loại"
st.markdown("<b>Loại</b>", unsafe_allow_html=True)
loai_tinh = st.selectbox(
    "", 
    ["Điểm trung bình môn học kì", "Điểm trung bình môn cả năm"], 
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# PHÂN LUỒNG GIAO DIỆN DỰA TRÊN LỰA CHỌN
if loai_tinh == "Điểm trung bình môn học kì":
    
    st.markdown("<b>Tổng số cột thường xuyên</b>", unsafe_allow_html=True)
    tong_cot = st.number_input("", min_value=1, value=4, step=1, label_visibility="collapsed")

    st.markdown("<b>Điểm thường xuyên</b> <span style='color: gray;'>(VD: 10, 9, 10)</span>", unsafe_allow_html=True)
    diem_tx_str = st.text_input("tx", placeholder="Nhập các điểm cách nhau bằng dấu phẩy", label_visibility="collapsed")

    st.markdown("<b>Điểm giữa kì</b> <span style='color: gray;'>(VD: 9.5)</span>", unsafe_allow_html=True)
    diem_gk_str = st.text_input("gk", placeholder="Nhập điểm giữa kì", label_visibility="collapsed")

    st.markdown("<b>Điểm trung bình môn mong muốn</b>", unsafe_allow_html=True)
    diem_mt_str = st.text_input("mt", placeholder="VD: 9.0", label_visibility="collapsed")

elif loai_tinh == "Điểm trung bình môn cả năm":
    
    st.markdown("<b>Điểm trung bình học kì 1</b> <span style='color: gray;'>(VD: 9.5)</span>", unsafe_allow_html=True)
    diem_hk1_str = st.text_input("hk1", placeholder="Nhập điểm học kì 1", label_visibility="collapsed")
    
    st.markdown("<b>Điểm trung bình năm mong muốn</b> <span style='color: gray;'>(VD: 9.0)</span>", unsafe_allow_html=True)
    diem_nam_mt_str = st.text_input("nam_mt", placeholder="Nhập điểm mong muốn cả năm", label_visibility="collapsed")


st.markdown("<br>", unsafe_allow_html=True)

# NÚT TÍNH TOÁN
if st.button("🧮 BẮT ĐẦU TÍNH", use_container_width=True):
    st.markdown("---")
    try:
        # XỬ LÝ: TÍNH ĐIỂM HỌC KÌ
        if loai_tinh == "Điểm trung bình môn học kì":
            diem_tx = [float(x.strip()) for x in diem_tx_str.split(",") if x.strip()]
            diem_gk = [float(x.strip()) for x in diem_gk_str.split(",") if x.strip()]
            
            if not diem_mt_str.strip() or not diem_gk_str.strip():
                st.warning("⚠️ Vui lòng nhập đầy đủ điểm giữa kì và điểm mong muốn.")
            else:
                diem_mt = float(diem_mt_str.strip())
                so_cot_tx_hien_co = len(diem_tx)
                so_cot_gk = len(diem_gk)
                tong_he_so = tong_cot + (so_cot_gk * 2) + 3 
                
                tong_diem_hien_tai = sum(diem_tx) + (sum(diem_gk) * 2)
                diem_tong_can_dat = diem_mt * tong_he_so
                diem_con_thieu = diem_tong_can_dat - tong_diem_hien_tai
                
                so_tx_thieu = tong_cot - so_cot_tx_hien_co
                
                if so_tx_thieu < 0:
                    st.error(f"❌ Nhập thừa điểm thường xuyên! Cần {tong_cot} nhưng đã nhập {so_cot_tx_hien_co}.")
                elif so_tx_thieu == 0:
                    # Áp dụng làm tròn 1 chữ số thập phân
                    diem_ck_can = round(diem_con_thieu / 3, 1)
                    if diem_ck_can <= 10:
                        st.success(f"🎯 Bạn cần đạt **{diem_ck_can:.1f}** điểm cuối kì để trung bình học kì được {diem_mt}.")
                    else:
                        st.error(f"❌ Bạn cần **{diem_ck_can:.1f}** điểm cuối kì. Rất tiếc, mục tiêu này vượt quá 10!")
                else:
                    st.info(f"📌 Đang thiếu **{so_tx_thieu}** cột thường xuyên.")
                    # Áp dụng làm tròn 1 chữ số thập phân
                    diem_bang_nhau = round(diem_con_thieu / (so_tx_thieu + 3), 1)
                    
                    if diem_bang_nhau <= 10:
                        st.success(f"🎯 Để đạt mục tiêu, các bài thường xuyên còn thiếu và cuối kì phải đạt trung bình: **{diem_bang_nhau:.1f}** điểm/bài.")
                    else:
                        st.error(f"❌ Cần trung bình **{diem_bang_nhau:.1f}** cho các bài còn lại. Không khả thi!")

        # XỬ LÝ: TÍNH ĐIỂM CẢ NĂM
        elif loai_tinh == "Điểm trung bình môn cả năm":
            if not diem_hk1_str.strip() or not diem_nam_mt_str.strip():
                st.warning("⚠️ Vui lòng nhập đầy đủ điểm học kì 1 và điểm trung bình năm mong muốn.")
            else:
                diem_hk1 = float(diem_hk1_str.strip())
                diem_nam_mt = float(diem_nam_mt_str.strip())
                
                # Áp dụng làm tròn 1 chữ số thập phân
                diem_hk2_can = round(((diem_nam_mt * 3) - diem_hk1) / 2, 1)
                
                if diem_hk2_can > 10:
                    st.error(f"❌ Để cả năm được **{diem_nam_mt}**, học kì 2 bạn cần đạt **{diem_hk2_can:.1f}**. Mục tiêu này vượt quá khả năng!")
                elif diem_hk2_can < 0:
                    st.success(f"🎯 Điểm học kì 1 của bạn quá cao nên học kì 2 chỉ cần **0.0** điểm là đã đạt được mục tiêu rồi!")
                else:
                    st.success(f"🎯 Học kì 2 bạn cần cố gắng đạt trung bình môn là: **{diem_hk2_can:.1f}** điểm để tổng kết cả năm được {diem_nam_mt}.")

    except ValueError:
        st.error("⚠️ Vui lòng chỉ nhập số và dấu (ví dụ: 9.5). Không nhập chữ cái.")

# Dòng Credit bản quyền ở góc phải dưới
st.markdown("<div style='text-align: right; color: #a9a9a9; font-size: 11px; margin-top: 50px; font-style: italic;'>Website by Nguyễn Bảo Nam</div>", unsafe_allow_html=True)
