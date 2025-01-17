import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Memproses data
def load_data(file_path):
    return pd.read_excel(file_path)

# Membuat filter untuk dashboard
def filter_data_dashboard(data, year_month):
    filter_data = data[data['year-month'] == year_month]
    st.header(f"Data untuk Bulan {year_month}")
    st.dataframe(filter_data)
    return filter_data

# Grafik jumlah pengguna (Casual dan Registered)
def amount_user(filter_data, year_month):
    st.subheader("Grafik Pengguna (Casual dan Registered)")
    total_casual_users = filter_data['casual'].sum()
    total_registered_users = filter_data['registered'].sum()

    st.write(f"Total Pengguna Casual: {total_casual_users}")
    st.write(f"Total Pengguna Registered: {total_registered_users}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(filter_data['dteday'], filter_data['casual'], label='Casual Users', color='skyblue', alpha=0.7)
    ax.bar(filter_data['dteday'], filter_data['registered'], label='Registered Users', color='orange', alpha=0.7, bottom=filter_data['casual'])
    ax.set_title(f"Pengguna Berdasarkan Tanggal - {year_month}")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Pengguna")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Distribusi kondisi cuaca
def distribution_weather(filter_data):
    st.subheader("Distribusi Berdasarkan Kondisi Cuaca")
    distribution_weather = filter_data['weathersit'].value_counts()

    for condition, count in distribution_weather.items():
        st.write(f"Kondisi Cuaca {condition}: {count} hari")

    st.bar_chart(distribution_weather)

# Data berdasarkan hari kerja
def workday(filter_data, working_day_filter):
    st.subheader("Data Berdasarkan Hari Kerja / Libur")
    if working_day_filter == 'Working Day':
        filter_workday = filter_data[filter_data['workingday'] == 'working day']
    else:
        filter_workday = filter_data[filter_data['workingday'] == 'day off']

    total_casual_workday = filter_workday['casual'].sum()
    total_registered_workday = filter_workday['registered'].sum()
    total_cnt_workday = filter_workday['cnt'].sum()

    st.write(f"Pengguna Casual: {total_casual_workday}")
    st.write(f"Pengguna Registered: {total_registered_workday}")
    st.write(f"Total CNT: {total_cnt_workday}")
    st.dataframe(filter_workday)

# Perbedaan total pengguna berdasarkan hari kerja dan libur
def comparison_workday_and_dayoff(filter_data):
    st.subheader("Analisis Total Pengguna: Hari Kerja vs Hari Libur")
    summary_workday = filter_data.groupby('workingday')['cnt'].sum()

    workday_cnt = summary_workday.get('working day', 0)
    day_off_cnt = summary_workday.get('day off', 0)

    st.write(f"Total Pengguna pada Hari Kerja: {workday_cnt}")
    st.write(f"Total Pengguna pada Hari Libur: {day_off_cnt}")
    st.bar_chart(summary_workday)

def main():
    # Judul dashboard
    st.title("Dashboard Analisis Data Bike Sharing")

    # Sidebar untuk filter
    st.sidebar.title("Filter Data Dashboard")

    # Upload data
    uploaded_file = 'main_data.xlsx'
    data = load_data(uploaded_file)

    # Filter berdasarkan Tahun-Bulan
    st.sidebar.header("Filter Tanggal")
    selected_year_month = st.sidebar.selectbox("Pilih Tahun-Bulan:", data['year-month'].unique())

    # Filter berdasarkan Hari Kerja
    st.sidebar.header("Filter Hari Kerja")
    workday_filter_option = st.sidebar.radio("Pilih Kategori Hari:", ['Working Day', 'Day Off'])

    # Menampilkan data yang difilter
    filter_data = filter_data_dashboard(data, selected_year_month)

    # Menampilkan grafik jumlah pengguna
    amount_user(filter_data, selected_year_month)

    # Menampilkan distribusi kondisi cuaca
    distribution_weather(filter_data)

    # Menampilkan data berdasarkan hari kerja
    workday(filter_data, workday_filter_option)

    # Menampilkan total pengguna hari kerja vs libur
    comparison_workday_and_dayoff(filter_data)

if __name__ == "__main__":
    main()
