from pathlib import Path
import pandas as pd
import plotly.express as px
DEFAULT_DATA_PATH = Path(__file__).resolve().parent / "Sample - Superstore.csv"

def load_data(file_path=DEFAULT_DATA_PATH):
    df = pd.read_csv(file_path, encoding="cp1252")
    df["Order Date"] = pd.to_datetime(
        df["Order Date"], format="%m/%d/%Y"
    )
    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"], format="%m/%d/%Y"
    )
    return df

def create_category_bar(df):
    """Bar chart total penjualan per kategori produk."""
    sales_by_category = (
        df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )
    return px.bar(
        sales_by_category,
        x="Category",
        y="Sales",
        title="Penjualan berdasarkan Kategori Produk",
        labels={"Category": "Kategori Produk", "Sales": "Total Penjualan ($)"},
    )

def create_monthly_line(df):
    """Line chart total penjualan per bulan."""
    monthly_sales = (
        df.assign(Month=df["Order Date"].dt.to_period("M").dt.to_timestamp())
        .groupby("Month", as_index=False)["Sales"]
        .sum()
        .sort_values("Month")
    )
    return px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        title="Tren Penjualan Bulanan",
        labels={"Month": "Bulan", "Sales": "Total Penjualan ($)"},
    )
    
def create_segment_pie(df):
    """Pie/donut chart total penjualan per segmen pelanggan."""
    segment_sales = (
        df.groupby("Segment", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )
    return px.pie(
        segment_sales,
        names="Segment",
        values="Sales",
        title="Penjualan berdasarkan Segmen Pelanggan",
        hole=0.3,
    )


def create_scatter_plot(df):
    """Scatter plot untuk melihat hubungan Sales dan Profit."""
    return px.scatter(
        df,
        x="Sales",
        y="Profit",
        color="Category",
        size="Quantity",
        hover_data=["Sub-Category", "Product Name"],
        title="Hubungan antara Penjualan dan Keuntungan",
        labels={
            "Sales": "Total Penjualan ($)",
            "Profit": "Total Keuntungan ($)",
            "Category": "Kategori Produk",
            "Quantity": "Kuantitas",
        },
    )

def create_horizontal_top_subcategories(df, top_n=10):
    """Horizontal bar chart"""
    sales_by_subcategory = (
        df.groupby("Sub-Category", as_index=False)["Sales"]
        .sum()
    )
    top_subcategories = (
        sales_by_subcategory.nlargest(top_n, "Sales")
        .sort_values("Sales", ascending=True)
    )
    return px.bar(
        top_subcategories,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        title=f"Top {min(top_n, len(top_subcategories))} Subkategori berdasarkan Penjualan",
        labels={
            "Sub-Category": "Subkategori Produk",
            "Sales": "Total Penjualan ($)",
        },
    )

def print_data_summary(df):
    """Menampilkan ringkasan ketika file ini dijalankan langsung."""
    print("\n10 baris pertama:")
    print(df.head(10))
    print("\nUkuran dataset (baris, kolom):", df.shape)
    print("\nInformasi tipe data:")
    df.info()
    print("\nStatistik deskriptif:")
    print(df.describe())
    print("\nJumlah nilai kosong per kolom:")
    print(df.isnull().sum())
    print("\nJumlah baris duplikat persis:", df.duplicated().sum())
    print("\nTotal Penjualan:", round(df["Sales"].sum(), 2))
    print("Total Keuntungan:", round(df["Profit"].sum(), 2))
    print("Total Kuantitas:", int(df["Quantity"].sum()))
    print("Total Pesanan Unik:", df["Order ID"].nunique())
    print("\nPenjualan berdasarkan kategori:")
    print(df.groupby("Category")["Sales"].sum().sort_values(ascending=False))
    print("\nKeuntungan berdasarkan wilayah:")
    print(df.groupby("Region")["Profit"].sum().sort_values(ascending=False))
    print("\nPenjualan bulanan (10 bulan pertama):")
    print(df.assign(Month=df["Order Date"].dt.to_period("M")).groupby("Month")["Sales"].sum().head(10))
    
if __name__ == "__main__":
    data = load_data()
    print_data_summary(data)
    create_category_bar(data).show()
    create_monthly_line(data).show()
    create_segment_pie(data).show()
    create_scatter_plot(data).show()
    create_horizontal_top_subcategories(data).show()
