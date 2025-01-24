import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Memproses data
def load_data(file_path):
    return pd.read_excel(file_path)

# Membuat filter untuk dashboard
def filter_data_dashboard(data, selected_year):
    filter_data = data[data['yr'] == selected_year]
    st.subheader(f"Data untuk Tahun {selected_year}")
    st.dataframe(filter_data)
    return filter_data

# Grafik jumlah pengguna 
def amount_user(filter_data, selected_year):
    st.subheader(f"Grafik Pengguna Perbulan di Tahun {selected_year}")
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
def comparison_workday_and_dayoff(filter_data, selected_year):
    st.subheader(f"Grafik Total Pengguna Hari Kerja vs Hari Libur di Tahun {selected_year}")

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

# Halaman ringkasan data
def summary_page(data):
    st.subheader("Grafik Total Pengguna 2011 - 2013")
    df_2011 = data[data['yr'] == 2011]
    df_2012 = data[data['yr'] == 2012]
    df_2013 = data[data['yr'] == 2013]
    
    plt.figure(figsize=(12, 6))
    plt.plot(df_2011['mnth'], df_2011['total_cnt'], label='2011', marker='o')
    plt.plot(df_2012['mnth'], df_2012['total_cnt'], label='2012', marker='o')
    plt.plot(df_2013['mnth'], df_2013['total_cnt'], label='Predicted 2013', marker='o', linestyle='--')
    
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Pengguna')
    plt.title('Tren Jumlah Pengguna (2011-2013)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # Kesimpulan dari peminjaman sepeda berdasarkan hari kerja
    st.subheader("Grafik Total Pengguna Hari Kerja vs Hari Libur 2011 - 2012")
    data_filtered = data[data['yr'] != 2013]

    plt.figure(figsize=(10, 6))
    sns.barplot(x='yr', y='cnt_workingday', hue='workingday', data=data_filtered, palette='Set1')
    plt.title('Perbandingan Jumlah Konten Berdasarkan Tahun dan Hari Kerja')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Konten')
    plt.legend(title='Hari Kerja', loc='upper right')
    st.pyplot(plt)
    
def main():
    # Judul aplikasi
    st.title("Dashboard Analisis Data Bike Sharing")

    # Sidebar untuk navigasi
    st.sidebar.title("Dashboard Bike Sharing")
    st.sidebar.subheader("Navigasi Halaman")
    page = st.sidebar.selectbox("Pilih Halaman:", ["Dashboard", "Summary"])

    # Upload data
    uploaded_file = 'main_data.xlsx'
    data = load_data(uploaded_file)

    if page == "Dashboard":
        # Filter berdasarkan Tahun
        st.sidebar.header("Filter Tahun")
        selected_year = st.sidebar.selectbox("Pilih Tahun:", data['yr'].unique())

        # Menampilkan data yang difilter
        filter_data = filter_data_dashboard(data, selected_year)

        # Menampilkan grafik jumlah pengguna
        amount_user(filter_data, selected_year)

        # Menampilkan total pengguna hari kerja vs libur
        comparison_workday_and_dayoff(filter_data, selected_year)

    elif page == "Summary":
        # Tampilkan halaman ringkasan
        summary_page(data)

if __name__ == "__main__":
    main()
