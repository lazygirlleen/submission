import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi tampilan Seaborn
sns.set_style("whitegrid")

# Title of the app
st.title("📊 Analisis Peminjaman Sepeda")

# Load dataset
df_day = pd.read_csv("day.csv")
df_day["dteday"] = pd.to_datetime(df_day["dteday"])

df_hour = pd.read_csv("hour.csv")
df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])

# Sidebar untuk filter data
st.sidebar.image("download.png", width=150)
st.sidebar.subheader("🔍 Filter Data")

# Pilih rentang tanggal
start_date = st.sidebar.date_input("Tanggal Mulai", df_day["dteday"].min())
end_date = st.sidebar.date_input("Tanggal Akhir", df_day["dteday"].max())

# Pilih musim
season_options = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
selected_season = st.sidebar.selectbox("Pilih Musim", season_options.values())
selected_season_key = list(season_options.keys())[list(season_options.values()).index(selected_season)]

# Filter data berdasarkan pilihan
filtered_df_day = df_day[
    (df_day["dteday"] >= pd.to_datetime(start_date)) &
    (df_day["dteday"] <= pd.to_datetime(end_date)) &
    (df_day["season"] == selected_season_key)
]

filtered_df_hour = df_hour[
    (df_hour["dteday"] >= pd.to_datetime(start_date)) &
    (df_hour["dteday"] <= pd.to_datetime(end_date)) &
    (df_hour["season"] == selected_season_key)
]

# Tampilkan statistik peminjaman
st.subheader("📈 Statistik Peminjaman")
col1, col2 = st.columns(2)

with col1:
    total_orders = filtered_df_day["cnt"].sum()
    st.metric("Total Peminjaman (Harian)", value=total_orders)

with col2:
    total_orders_hourly = filtered_df_hour["cnt"].sum()
    st.metric("Total Peminjaman (Jam)", value=total_orders_hourly)

# Grafik Tren Peminjaman Sepeda Harian
st.subheader("📅 Tren Peminjaman Sepeda Harian")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_df_day["dteday"], filtered_df_day["cnt"], linewidth=2, marker="o", color="b", label="Harian")
ax.set_title("Tren Peminjaman Sepeda Harian")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman")
ax.legend()
st.pyplot(fig)

# Grafik Tren Peminjaman Sepeda Tiap Jam
st.subheader("⏳ Tren Peminjaman Sepeda Tiap Jam")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_df_hour, x="hr", y="cnt", ci=None, marker="o", ax=ax, color="g")
ax.set_title("Tren Peminjaman Sepeda Tiap Jam")
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig)

# Checkbox untuk menampilkan data mentah
if st.checkbox("📜 Tampilkan Data Mentah"):
    st.write("### Data Harian")
    st.dataframe(filtered_df_day)
    st.write("### Data Per Jam")
    st.dataframe(filtered_df_hour)
