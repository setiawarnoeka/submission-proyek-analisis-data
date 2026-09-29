import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_style("whitegrid")

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
all_df = pd.read_csv(os.path.join(BASE_DIR, "main_data.csv"))

st.title("Dashboard Analisis E-Commerce")
st.markdown("Analisis pesanan *delivered* periode 2017-2018")

# Pertanyaan 1: Revenue per kategori
st.header("Kategori Produk dengan Revenue Tertinggi & Terendah")

category_revenue_df = all_df.groupby("product_category_name_english")["price"].sum() \
    .sort_values(ascending=False).reset_index()

top5 = category_revenue_df.head(5).sort_values("price")
bottom5 = category_revenue_df.tail(5)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top5["product_category_name_english"], top5["price"], color="#1f77b4")
    ax.set_title("5 Kategori Revenue Tertinggi")
    ax.set_xlabel("Total Revenue (BRL)")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(bottom5["product_category_name_english"], bottom5["price"], color="#d62728")
    ax.set_title("5 Kategori Revenue Terendah")
    ax.set_xlabel("Total Revenue (BRL)")
    st.pyplot(fig)

# Pertanyaan 2: Revenue per state
st.header("State dengan Pelanggan & Revenue Terbesar")

state_df = all_df.groupby("customer_state").agg(
    jumlah_pelanggan=("customer_unique_id", "nunique"),
    total_revenue=("price", "sum")
).sort_values("total_revenue", ascending=False).reset_index()

top10_state = state_df.head(10).sort_values("total_revenue")

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top10_state["customer_state"], top10_state["total_revenue"], color="#1f77b4")
ax.set_title("10 State dengan Revenue Tertinggi")
ax.set_xlabel("Total Revenue (BRL)")
st.pyplot(fig)

# Analisis Lanjutan: Segmentasi RFM
st.header("Segmentasi Pelanggan (RFM)")

segment_df = all_df.drop_duplicates("customer_unique_id")["segment"].value_counts().reset_index()
segment_df.columns = ["segment", "jumlah_pelanggan"]

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(segment_df["segment"], segment_df["jumlah_pelanggan"], color="#1f77b4")
ax.set_title("Jumlah Pelanggan per Segmen RFM")
ax.set_xlabel("Jumlah Pelanggan")
ax.invert_yaxis()
st.pyplot(fig)

st.caption("Dashboard dibuat untuk submission Proyek Analisis Data - Dicoding")