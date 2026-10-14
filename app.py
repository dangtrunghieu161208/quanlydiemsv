import streamlit as st
import pandas as pd

# Cấu hình trang giao diện rộng (Wide layout)
st.set_page_config(page_title="Quản lý điểm sinh viên", page_icon="🎓", layout="wide")

# ---------------------------------------------------------
# 1. Khởi tạo dữ liệu 10 sinh viên
# ---------------------------------------------------------
data = {
    "MSSV": ["SV01", "SV02", "SV03", "SV04", "SV05", "SV06", "SV07", "SV08", "SV09", "SV10"],
    "Họ và tên": [
        "An", "Bình", "Cường", "Dung", "Em",
        "Trang", "Lan", "Huy", "Hùng", "Khanh"
    ],
    "Điểm chuyên cần": [8.0, 8.5, 7.5, 9.0, 9.5, 10.0, 6.0, 9.0, 5.0, 8.0],
    "Điểm giữa kỳ":    [8.0, 8.0, 6.5, 7.5, 9.0, 9.0, 5.0, 8.5, 5.5, 7.5],
    "Điểm cuối kỳ":    [8.0, 8.5, 6.5, 8.0, 9.5, 9.0, 5.5, 9.0, 5.0, 8.0]
}

df = pd.DataFrame(data)

# Tính Điểm tổng kết: Chuyên cần (10%), Giữa kỳ (30%), Cuối kỳ (60%)
df["Tổng kết"] = (df["Điểm chuyên cần"] * 0.1 + df["Điểm giữa kỳ"] * 0.3 + df["Điểm cuối kỳ"] * 0.6).round(2)

# Hàm xếp loại sinh viên
def xep_loai(diem):
    if diem >= 8.5:
        return "Xuất sắc"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# Tính xếp hạng
df["Hạng"] = df["Tổng kết"].rank(ascending=False, method="min").astype(int)

# Arrange lại thứ tự cột
df_display = df[["Hạng", "MSSV", "Họ và tên", "Điểm chuyên cần", "Điểm giữa kỳ", "Điểm cuối kỳ", "Tổng kết", "Xếp loại"]]

# ---------------------------------------------------------
# 2. Thanh bên (Sidebar) - Bảng điều khiển
# ---------------------------------------------------------
st.sidebar.title("🎓 Bảng điều khiển")
st.sidebar.subheader("Lọc và tìm kiếm")

# Chọn sinh viên
list_sv = ["Tất cả sinh viên"] + df["Họ và tên"].tolist()
selected_sv = st.sidebar.selectbox("Tìm kiếm hoặc chọn sinh viên", list_sv)

# Lọc theo xếp loại
list_xl = ["Tất cả xếp loại"] + list(df["Xếp loại"].unique())
selected_xl = st.sidebar.selectbox("Lọc theo xếp loại", list_xl)

st.sidebar.markdown("---")

# Thông tin tác giả
st.sidebar.subheader("Thông tin tác giả")
with st.sidebar.container():
    st.write("**Họ và tên:** Đặng Trung Hiếu ")
    st.write("**MSSV:** 070208009954")
    st.write("**Lớp:** AI87")
    st.write("**Trường:** ĐH Giao Thông Vận Tải")

# ---------------------------------------------------------
# 3. Lọc dữ liệu theo Sidebar
# ---------------------------------------------------------
filtered_df = df_display.copy()

if selected_sv != "Tất cả sinh viên":
    filtered_df = filtered_df[filtered_df["Họ và tên"] == selected_sv]

if selected_xl != "Tất cả xếp loại":
    filtered_df = filtered_df[filtered_df["Xếp loại"] == selected_xl]

# ---------------------------------------------------------
# 4. Giao diện chính
# ---------------------------------------------------------
# Header Tiêu đề
st.title("Quản lý điểm sinh viên")
st.caption("Thống kê tự động, biểu đồ tương tác và tra cứu hồ sơ học tập của cả lớp.")

# Thanh điều hướng dạng Tab
tab1, tab2, tab3 = st.tabs(["📊 Tổng quan & Bảng điểm", "📈 Biểu đồ & Phân tích", "🔍 Tra cứu cá nhân"])

# === TAB 1: TỔNG QUAN & BẢNG ĐIỂM ===
with tab1:
    dtb_lop = df["Tổng kết"].mean().round(2)
    so_sv_dat = (df["Tổng kết"] >= 5.0).sum()
    sv_cao_nhat = df.loc[df["Tổng kết"].idxmax()]
    sv_thap_nhat = df.loc[df["Tổng kết"].idxmin()]

    # Dòng thông báo xin chào
    st.info(f"Xin chào! Lớp hiện có **{len(df)}** sinh viên với điểm trung bình **{dtb_lop}**. Đang hiển thị **{len(filtered_df)}/{len(df)}** sinh viên theo bộ lọc ở thanh bên.")

    # 4 Thẻ chỉ số (Metrics)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Điểm TB lớp", dtb_lop, "Thang điểm 10")
    col2.metric("🏆 Điểm cao nhất", sv_cao_nhat["Tổng kết"], sv_cao_nhat["Họ và tên"])
    col3.metric("📉 Điểm thấp nhất", sv_thap_nhat["Tổng kết"], sv_thap_nhat["Họ và tên"])
    col4.metric("✅ Tỷ lệ đạt", f"{(so_sv_dat/len(df))*100:.0f}%", f"{so_sv_dat}/{len(df)} sinh viên")

    st.markdown("### 📋 Bảng điểm sinh viên")
    st.dataframe(filtered_df.sort_values(by="Hạng"), use_container_width=True, hide_index=True)

# === TAB 2: BIỂU ĐỒ & PHÂN TÍCH ===
with tab2:
    st.markdown("### 📈 Biểu đồ điểm tổng kết của các sinh viên")
    st.bar_chart(filtered_df.set_index("Họ và tên")["Tổng kết"])

# === TAB 3: TRA CỨU CÁ NHÂN ===
with tab3:
    st.markdown("### 🔍 Tra cứu thông tin chi tiết")
    select_single_sv = st.selectbox("Chọn sinh viên cần tra cứu:", df["Họ và tên"].tolist())
    
    sv_info = df[df["Họ và tên"] == select_single_sv].iloc[0]
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Điểm chuyên cần", sv_info["Điểm chuyên cần"])
    c2.metric("Điểm giữa kỳ", sv_info["Điểm giữa kỳ"])
    c3.metric("Điểm cuối kỳ", sv_info["Điểm cuối kỳ"])
    c4.metric("Tổng kết", sv_info["Tổng kết"])
    c5.metric("Xếp loại", sv_info["Xếp loại"])
