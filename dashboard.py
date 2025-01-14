import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul
st.title("Dashboard Bike Sharing")

# Sidebar
st.sidebar.title("Dashboard Filter")
st.sidebar.header("Informasi")
st.sidebar.write("Gunakan sidebar untuk memilih filter.")

# Data upload
uploaded_file = 'main_data.xlsx'
day_df = pd.read_excel(uploaded_file)

# Filter
year_month = st.sidebar.selectbox("Pilih Tahun-Bulan:", day_df['year-month'].unique())
st.sidebar.header("Filter Hari Kerja")

working_day_filter = st.sidebar.radio("Pilih Hari Kerja:", ['Working Day', 'Day Off'])

# Data berdasarkan filter
st.header("Data Overview")

filtered_data = day_df[day_df['year-month'] == year_month]
st.subheader(f"Data untuk {year_month}")
st.dataframe(filtered_data)

# Analisis Statistik
st.header("Analisis Statistik")
st.write(filtered_data.describe())

# Total Pengguna (Casual dan Registered)
st.subheader("Grafik Jumlah Pengguna (Casual dan Registered)")

total_casual = filtered_data['casual'].sum()
total_registered = filtered_data['registered'].sum()

st.write(f"Total Casual Users: {total_casual}")
st.write(f"Total Registered Users: {total_registered}")

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(filtered_data['dteday'], filtered_data['casual'], label='Casual', alpha=0.7)
ax.bar(filtered_data['dteday'], filtered_data['registered'], label='Registered', alpha=0.7, bottom=filtered_data['casual'])
ax.set_title(f"Jumlah Pengguna untuk {year_month}")
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel("Tanggal")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# Kondisi Cuaca
st.subheader("Distribusi Kondisi Cuaca")
weather_count = filtered_data['weathersit'].value_counts()

for weather, count in weather_count.items():
    st.write(f"Kondisi Cuaca {weather}: {count} hari")

st.bar_chart(weather_count)

# Rata-rata Temperatur dan Kelembapan
st.subheader("Rata-rata Temperatur dan Kelembapan")
avg_temp_hum = filtered_data[['temp', 'hum']].mean()
st.write(avg_temp_hum)

# Data Berdasarkan Hari Kerja
st.subheader("Data Berdasarkan Hari Kerja")
if working_day_filter == 'Working Day':
    workday_data = filtered_data[filtered_data['workingday'] == 'working day']
else:
    workday_data = filtered_data[filtered_data['workingday'] == 'day off']

total_casual_workday = workday_data['casual'].sum()
total_registered_workday = workday_data['registered'].sum()
total_cnt_workday = workday_data['cnt'].sum()

st.write(f"Total Casual Users: {total_casual_workday}")
st.write(f"Total Registered Users: {total_registered_workday}")
st.write(f"Total Count: {total_cnt_workday}")
st.dataframe(workday_data)

# Total Pengguna di Hari Kerja dan Hari Libur
st.subheader("Total Pengguna: Hari Kerja vs Hari Libur")
workingday_group = filtered_data.groupby('workingday')['cnt'].sum()

total_working_day = workingday_group.get('working day', 0)
total_day_off = workingday_group.get('day off', 0)

st.write(f"Total CNT pada Hari Kerja: {total_working_day}")
st.write(f"Total CNT pada Hari Libur: {total_day_off}")

st.bar_chart(workingday_group)
