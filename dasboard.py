import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the all_data.csv file
all_data = pd.read_csv('all_data.csv')

# Pastikan kolom 'order_purchase_timestamp' dalam format datetime
all_data['order_purchase_timestamp'] = pd.to_datetime(all_data['order_purchase_timestamp'], errors='coerce')

# Periksa kolom yang ada
columns = all_data.columns

# Dashboard Title
st.title("E-Commerce Data Analysis")

# Sidebar: Menampilkan kolom-kolom dataset
st.sidebar.header("Dataset Columns")
st.sidebar.write(columns)

# Section 1: Filter Data
st.sidebar.header("Filter Data")

# Filter berdasarkan kategori produk
categories = all_data['product_category_name'].unique()
selected_category = st.sidebar.selectbox("Select a Product Category", categories)

# Filter berdasarkan rentang tanggal pembelian
start_date, end_date = st.sidebar.date_input(
    "Select Date Range", 
    [all_data['order_purchase_timestamp'].min().date(), all_data['order_purchase_timestamp'].max().date()]
)

# Filter data berdasarkan pilihan pengguna
filtered_data = all_data[
    (all_data['product_category_name'] == selected_category) & 
    (all_data['order_purchase_timestamp'].dt.date >= start_date) & 
    (all_data['order_purchase_timestamp'].dt.date <= end_date)
]

# Section 2: Top Product Categories
st.header(f"Top Products in {selected_category} Category")

# Menghitung jumlah pesanan per kategori produk dari data yang sudah difilter
category_counts = filtered_data.groupby('product_category_name')['order_id'].count().reset_index()
category_counts = category_counts.rename(columns={'order_id': 'order_count'})

# Menampilkan 10 kategori produk teratas
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(category_counts['product_category_name'].head(10), category_counts['order_count'].head(10), color='skyblue')
ax.set_xlabel("Number of Orders")
ax.set_ylabel("Category")
ax.set_title("Top 10 Most Ordered Product Categories")
st.pyplot(fig)

# Section 3: Data Overview
st.header("Data Overview")
st.write(f"Showing data for {len(filtered_data)} orders in the selected category and date range.")

# Menampilkan beberapa data untuk memberikan gambaran
st.dataframe(filtered_data.head())

# Section 4: Optional: Sales over Time
st.header("Sales Over Time")

# Menghitung jumlah pesanan berdasarkan tanggal
sales_over_time = filtered_data.groupby(filtered_data['order_purchase_timestamp'].dt.date)['order_id'].count().reset_index()
sales_over_time = sales_over_time.rename(columns={'order_id': 'order_count'})

# Visualisasi sales over time
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(sales_over_time['order_purchase_timestamp'], sales_over_time['order_count'], marker='o', color='orange')
ax.set_xlabel("Date")
ax.set_ylabel("Number of Orders")
ax.set_title("Orders Over Time")
st.pyplot(fig)
