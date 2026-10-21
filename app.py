import streamlit as st

from Data_Penjualan import (
    load_data,
    create_category_bar,
    create_monthly_line,
    create_segment_pie,
    create_scatter_plot,
    create_horizontal_top_subcategories,
)

st.set_page_config(page_title="Dashboard Penjualan Superstore", layout="wide")

# Membaca data 
try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "File 'Sample - Superstore.csv' tidak ditemukan. "
        "Letakkan file CSV dalam folder yang sama dengan app.py dan Data_Penjualan.py."
    )
    st.stop()

st.title("Dashboard Penjualan Superstore")
st.write(
    "Dashboard interaktif untuk menganalisis penjualan, keuntungan, kuantitas, "
    "dan perilaku pelanggan pada dataset Superstore."
)

# BUAT SLICER INTERAKTIF
st.sidebar.header("Filter Data")
categories = sorted(df["Category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Pilih Kategori Produk:",
    options=categories,
    default=categories,
)
regions = sorted(df["Region"].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect(
    "Pilih Wilayah:",
    options=regions,
    default=regions,
)

# Penerapan
df_filtered = df[
    df["Category"].isin(selected_categories)
    & df["Region"].isin(selected_regions)
].copy()
if df_filtered.empty:
    st.warning("Tidak ada data yang sesuai. Pilih minimal satu kategori dan satu wilayah.")
    st.stop()

st.caption(f"Jumlah baris setelah filter: {len(df_filtered):,} dari {len(df):,} baris")

# KPI: semua dihitung dari data yang sudah difilter
st.subheader("Ringkasan Kinerja")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penjualan", f"${df_filtered['Sales'].sum():,.2f}")
col2.metric("Total Keuntungan", f"${df_filtered['Profit'].sum():,.2f}")
col3.metric("Total Kuantitas", f"{df_filtered['Quantity'].sum():,}")
col4.metric("Total Pesanan", f"{df_filtered['Order ID'].nunique():,}")

# VISUALISASI

st.subheader("Analisis Penjualan")
left, right = st.columns(2)
with left:
    st.plotly_chart(create_category_bar(df_filtered), use_container_width=True)
with right:
    st.plotly_chart(create_monthly_line(df_filtered), use_container_width=True)

left, right = st.columns(2)
with left:
    st.plotly_chart(create_segment_pie(df_filtered), use_container_width=True)
with right:
    st.plotly_chart(create_scatter_plot(df_filtered), use_container_width=True)

st.plotly_chart(
    create_horizontal_top_subcategories(df_filtered, top_n=10),
    use_container_width=True,
)
