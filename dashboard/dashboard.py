import streamlit as st
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi tampilan Seaborn
sns.set_style("whitegrid")

# Title of the app
st.title("📊 Analisis Peminjaman Sepeda dari Always Bike")

# Load dataset
def load_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    return pd.read_csv(filepath)

df_day = load_data("day.csv")
df_hour = load_data("hour.csv")

df_day["dteday"] = pd.to_datetime(df_day["dteday"])
df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])

# Sidebar untuk filter data
st.sidebar.image("https://cdn.pixabay.com/photo/2023/03/25/19/23/bicycle-7876692_1280.png", caption="Always Bike")
st.sidebar.subheader("🔍 Filter Data")

# Pilih rentang tanggal
start_date = st.sidebar.date_input("Tanggal Mulai", df_day["dteday"].min())
end_date = st.sidebar.date_input("Tanggal Akhir", df_day["dteday"].max())

# Pilih musim
season_options = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
selected_season = st.sidebar.selectbox(
    "Pilih Musim", 
    options=list(season_options.keys()), 
    format_func=lambda x: season_options.get(x)
)

# Pilih cuaca
weather_options = {1: "Cerah", 2: "Berawan", 3: "Gerimis", 4: "Hujan"}
selected_weather = st.sidebar.selectbox(
    "Pilih Cuaca", 
    options=list(weather_options.keys()), 
    format_func=lambda x: weather_options.get(x)
)

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
