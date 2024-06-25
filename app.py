import streamlit as st
import pandas as pd
import plotly.express as px

# Membaca dataset
@st.cache_data  # Mengizinkan mutasi pada objek yang dikembalikan
def load_data():
    data = pd.read_csv('retail_sales_dataset.csv')
    return data

# Memanggil fungsi untuk memuat data
data = load_data()

data['Date'] = pd.to_datetime(data['Date'])
data['Month'] = data['Date'].dt.month
data['Year'] = data['Date'].dt.year

# Mengubah kolom 'DayOfWeek' untuk analisis hari dalam seminggu
data['DayOfWeek'] = data['Date'].dt.dayofweek

st.sidebar.markdown('### Unduh Dataset')
st.sidebar.markdown('[Download CSV](https://www.kaggle.com/datasets/mohammadtalib786/retail-sales-dataset)')

# Judul aplikasi Streamlit
st.title('Tugas Sistem Pendukung Keputusan')

# Menampilkan data teratas dari dataset
st.subheader('Data Retail Sales (5 baris pertama):')
st.write(data.head())

# Sidebar untuk memilih analisis
analysis_choice = st.sidebar.selectbox(
    'Pilih Analisis:',
    ('Tren Penjualan', 'Pelanggan', 'Produk', 'Pembelian dan Pengeluaran')
)

# Analisis Tren Penjualan
if analysis_choice == 'Tren Penjualan':
    st.header('Tren Penjualan')

    # Pertanyaan 1: Tren penjualan bulanan per tahun
    st.subheader('Pertanyaan 1 : Bagaimana Tren Penjualan Bulanan per Tahun?')

    years = data['Year'].unique().tolist()  
    all_months = range(1, 13)  
    all_dates = [(year, month) for year in years for month in all_months]
    all_sales = []
    for year, month in all_dates:
        total_sales = data[(data['Year'] == year) & (data['Month'] == month)]['Total Amount'].sum()
        all_sales.append({'Year': year, 'Month': month, 'Total Amount': total_sales})
    monthly_sales = pd.DataFrame(all_sales)
    tren_penjualan = px.line(monthly_sales, x='Month', y='Total Amount', color='Year', title='Tren Penjualan Bulanan per Tahun')
    st.plotly_chart(tren_penjualan)

    # Pertanyaan 2: Penjualan berdasarkan hari dalam seminggu
    st.subheader('Pertanyaan 2 : Total Penjualan Berdasarkan Hari dalam Seminggu')
    day_sales = data.groupby('DayOfWeek')['Total Amount'].sum().reset_index()
    salesofweek = px.bar(day_sales, x='DayOfWeek', y='Total Amount', title='Total Penjualan Berdasarkan Hari dalam Seminggu', labels={'DayOfWeek': 'Hari dalam Seminggu', 'Total Amount': 'Total Penjualan'})
    st.plotly_chart(salesofweek)

    # Pertanyaan 3: Penjualan pada akhir pekan vs hari kerja
    st.subheader('Pertanyaan 3 : Lebih bagus mana Penjualan pada Akhir Pekan vs Hari Kerja?')
    data['Weekend'] = data['Date'].dt.dayofweek >= 5
    weekend_sales = data.groupby('Weekend')['Total Amount'].sum().reset_index()
    wvsk = px.bar(weekend_sales, x='Weekend', y='Total Amount', title='Penjualan pada Akhir Pekan vs Hari Kerja', labels={'Total Amount': 'Total Penjualan', 'Weekend': 'Periode'},
                  color='Weekend', color_discrete_map={True: 'orange', False: 'blue'})
    st.plotly_chart(wvsk)

# Analisis Pelanggan
elif analysis_choice == 'Pelanggan':
    st.header('Analisis Pelanggan')

    # Pertanyaan 1: Perbandingan jumlah gender yang sering berbelanja
    st.subheader('Pertanyaan 1 : Perbandingan Jumlah Gender yang Sering Berbelanja')
    gender_counts = data['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    gen_buy = px.bar(gender_counts, x='Gender', y='Count', title='Perbandingan Jumlah Gender yang Sering Berbelanja',
                  labels={'Count': 'Jumlah Transaksi'}, color='Gender', color_discrete_map={'Male': 'blue', 'Female': 'red'})
    st.plotly_chart(gen_buy)

    # Pertanyaan 2: Profil demografis pelanggan
    st.subheader('Pertanyaan 2 : Bagaimana Distribusi Usia Pelanggan berdasarkan Gender?')
    gend = px.histogram(data, x='Age', color='Gender', title='Distribusi Usia Pelanggan berdasarkan Gender', labels={'Age': 'Usia', 'Gender': 'Gender'})
    st.plotly_chart(gend)

    # Pertanyaan 3: Perbedaan kebiasaan berbelanja berdasarkan gender
    st.subheader('Pertanyaan 3 : Rata-rata Pengeluaran Berdasarkan Gender')
    gender_sales = data.groupby('Gender')['Total Amount'].mean().reset_index()
    kebiasaan = px.bar(gender_sales, x='Gender', y='Total Amount', title='Rata-rata Pengeluaran Berdasarkan Gender', labels={'Total Amount': 'Rata-rata Pengeluaran'},
                   color='Gender', color_discrete_map={'Male': 'blue', 'Female': 'red'})
    st.plotly_chart(kebiasaan)

# Analisis Produk
elif analysis_choice == 'Produk':
    st.header('Analisis Produk')

    st.header('Produk yang Tersedia')
    products = data['Product Category'].unique()
    st.write("Daftar Produk:")
    st.write(products)

    # Pertanyaan 1: Kategori produk yang paling banyak terjual
    st.subheader('Pertanyaan 1 : Kategori Produk yang Paling Banyak Terjual')
    category_sales = data.groupby('Product Category')['Quantity'].sum().reset_index().sort_values(by='Quantity', ascending=True)
    produk = px.bar(category_sales, x='Quantity', y='Product Category', orientation='h', title='Kategori Produk yang Paling Banyak Terjual', labels={'Quantity': 'Jumlah Terjual', 'Product Category': 'Kategori Produk'})
    st.plotly_chart(produk)

    # Pertanyaan 2: Kontribusi produk terhadap total pendapatan
    st.subheader('Pertanyaan 2 : Kontribusi Produk terhadap Total Pendapatan')
    category_revenue = data.groupby('Product Category')['Total Amount'].sum().reset_index().sort_values(by='Total Amount', ascending=True)
    ptop = px.bar(category_revenue, x='Total Amount', y='Product Category', orientation='h', title='Kontribusi Produk terhadap Total Pendapatan', labels={'Total Amount': 'Total Pendapatan', 'Product Category': 'Kategori Produk'})
    st.plotly_chart(ptop)

    # Pertanyaan 3: Distribusi penjualan berdasarkan kategori produk
    st.subheader('Pertanyaan 3 : Distribusi Penjualan Berdasarkan Kategori Produk')
    disP = px.pie(category_revenue, names='Product Category', values='Total Amount', title='Distribusi Penjualan Berdasarkan Kategori Produk')
    st.plotly_chart(disP)

# Analisis Pembelian dan Pengeluaran
elif analysis_choice == 'Pembelian dan Pengeluaran':
    st.header('Analisis Pembelian dan Pengeluaran')

    # Pertanyaan 1: Rata-rata jumlah unit yang dibeli per transaksi
    average_quantity = data['Quantity'].mean()
    st.subheader(f'Rata-rata jumlah unit yang dibeli per transaksi: {average_quantity:.2f}')

    # Pertanyaan 2: Rata-rata pengeluaran per pelanggan
    average_spending = data.groupby('Customer ID')['Total Amount'].sum().mean()
    st.subheader(f'Rata-rata pengeluaran per pelanggan: {average_spending:.2f}')

    # Pertanyaan 3: Korelasi antara usia pelanggan dan total pengeluaran
    st.subheader('Korelasi Usia Pelanggan dan Total Pengeluaran')
    kor_usia = px.scatter(data, x='Age', y='Total Amount', color='Gender',
                       title='Korelasi Usia Pelanggan dan Total Pengeluaran',
                       labels={'Age': 'Usia Pelanggan', 'Total Amount': 'Total Pengeluaran'},
                       color_discrete_map={'Male': 'blue', 'Female': 'pink'})
    st.plotly_chart(kor_usia)

st.sidebar.markdown('### Nama Kelompok : ')
st.sidebar.markdown('1. Minan Abdillah')
st.sidebar.markdown('2. M. Dzaki Wicaksono')
st.sidebar.markdown('3. M. Maulana Fathul Muin')