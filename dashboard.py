import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Memproses data
def load_data(file_path):
    return pd.read_excel(file_path)

# Membuat filter untuk dashboard
def filter_data_dashboard(data, year):
    filter_data = data[data['yr'] == year]
    st.header(f"Data untuk Tahun {year}")
    st.dataframe(filter_data)
    return filter_data

# Grafik jumlah pengguna (Casual dan Registered)
def amount_user(filter_data, data):
    st.subheader("Grafik Pengguna (Casual dan Registered)")
    total_cnt = filter_data['total_cnt'].sum()

    st.write(f"Total CNT: {total_cnt}")

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=filter_data, x='mnth', y='total_cnt', marker='o')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Pengguna')
    plt.title('Visualisasi Jumlah Berdasarkan Bulan')

    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    xticks = range(1, 13)  
    plt.xticks(xticks, month_labels)
    plt.xticks(rotation=45)

    plt.tight_layout()
    st.pyplot(plt)

# Perbedaan total pengguna berdasarkan hari kerja dan libur
def comparison_workday_and_dayoff(filter_data):
    st.subheader("Analisis Total Pengguna: Hari Kerja vs Hari Libur")

    if "tidak ada data" in filter_data['workingday'].values:
        st.write("Tidak ada data untuk grafik ini.")
    elif not filter_data.empty:
        plt.figure(figsize=(10, 6))
        sns.barplot(
            x='mnth', y='cnt_workingday', hue='workingday', 
            data=filter_data, palette='Set1'
        )
        plt.title('Perbandingan Jumlah Konten Berdasarkan Bulan dan Hari Kerja')
        plt.xlabel('Bulan')
        plt.ylabel('Jumlah Konten')
        plt.legend(title='Hari Kerja', loc='upper right')
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.write("Data tidak tersedia untuk grafik ini.")
    
    
def main():
    # Judul dashboard
    st.title("Dashboard Analisis Data Bike Sharing")

    # Sidebar untuk filter
    st.sidebar.title("Filter Data Dashboard")

    # Upload data
    uploaded_file = 'main_data.xlsx'
    data = load_data(uploaded_file)

    # Filter berdasarkan Tahun-Bulan
    st.sidebar.header("Filter Tahun")
    selected_year = st.sidebar.selectbox("Pilih Tahun:", data['yr'].unique())

    # Menampilkan data yang difilter
    filter_data = filter_data_dashboard(data, selected_year)

    # Menampilkan grafik jumlah pengguna
    amount_user(filter_data, selected_year)

    # Menampilkan total pengguna hari kerja vs libur
    comparison_workday_and_dayoff(filter_data)

if __name__ == "__main__":
    main()
