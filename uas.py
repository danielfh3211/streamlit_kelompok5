import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px

# Menyusun menu dengan pilihan yang lebih menarik
with st.sidebar:
    choose = option_menu("Pilih Dataset", ["Penjualan Manga", "Kejahatan US", "Produksi Beras", "MPL ID Season 10"],
                         icons=['book', 'boombox', 'kanban', 'controller'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
         "container": {"padding": "5!important", "background-color": "#fafafa"},
         "icon": {"color": "orange", "font-size": "25px"},
         "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#ddd"},
         "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

# Gaya untuk setiap halaman
st.markdown(
    """
    <style>
    .sidebar-content {
        background-color: #f4f4f4;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .sidebar-title {
        font-size: 20px;
        margin-bottom: 10px;
    }
    .sidebar-menu-item, .sidebar-menu-item-active {
        padding: 10px 0;
    }
    .sidebar-menu-item-active {
        background-color: #2e7d32;
        color: #fff;
        padding: 10px 0;
        border-radius: 5px;
    }
    table {
        width: 100%;
        text-align: center;
    }
    th {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Latar Belakang
if choose == "MPL ID Season 10":
    
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1678924587662-d8c63e57eb11?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    # Judul dan Deskripsi
    st.title("Hero Statistik MPL ID Season 10 🎮")
    st.subheader("Tentang")
    description = """
        Mobile Legends: Bang Bang Professional League (MPL) adalah kompetisi game mobile terbesar dan paling prestisius di Asia Tenggara.
        Didorong oleh tekad untuk meningkatkan ekosistem esports, MPL membuat terobosan dengan membangun liga esports bermodel waralaba pertama di Asia Tenggara.
        Memastikan keberlanjutan komunitas secara keseluruhan, model waralaba ini akan menerapkan pembagian pendapatan, batas gaji, dan manfaat khusus lainnya untuk tim-tim peserta.
        """
    st.write(f'<p style="text-align: justify;">{description}</p>', unsafe_allow_html=True)

    # Memuat data dari MPL_ID_S10.csv
    data = pd.read_csv("MPL_ID_S10.csv")

    # Top 5 hero yang paling banyak dipilih
    top_pick = data.nlargest(5, "Hero_picked")[["Hero", "Hero_picked"]]
    top_pick.columns = ["Hero", "Pick"]
    st.subheader("Top 5 Pick")
    html_pick = top_pick.to_html(index=False)
    st.write(f"{html_pick}", unsafe_allow_html=True)

    # Top 5 hero yang paling banyak diban
    top_ban = data.nlargest(5, "Hero_banned")[["Hero", "Hero_banned"]]
    top_ban.columns = ["Hero", "Ban"]
    st.subheader("Top 5 Ban")
    html_ban = top_ban.to_html(index=False)
    st.write(f"{html_ban}", unsafe_allow_html=True)

    # Membersihkan data dengan menggantikan "-" dengan NaN pada kolom 'Winrate'
    data['T_winrate'] = data['T_winrate'].replace('-', np.nan)
    # Mengonversi kolom 'T_winrate' ke tipe data numerik (float)
    data['T_winrate'] = data['T_winrate'].str.rstrip('%').astype(float)

    # Top 5 hero dengan Winrate tertinggi (minimal 5 pertandingan)
    top_winrate = data[data['Hero_picked'] >= 5].nlargest(5, 'T_winrate')[['Hero', 'T_winrate']]
    top_winrate.columns = ['Hero', 'Winrate']
    top_winrate['Winrate'] = top_winrate['Winrate'].astype(str) + ' %'
    st.subheader("Top 5 Winrate Tertinggi (Minimal 5 Pertandingan)")
    html_winrate = top_winrate.to_html(index=False)
    st.write(f"{html_winrate}", unsafe_allow_html=True)

    # Input pengguna: pilih hero(s) untuk tabel data
    st.subheader("Hero Statistik Pertandingan MPL ID S10", divider='blue')
    selected_heroes = st.multiselect("Pilih Hero(s) untuk Tabel Data", data["Hero"])

    # Menyaring data berdasarkan hero yang dipilih
    if not selected_heroes:
        filtered_data = data[["Hero", "Hero_picked", "Hero_banned", "T_wins", "T_lose", "T_winrate"]]
    else:
        filtered_data = data[data["Hero"].isin(selected_heroes)][["Hero", "Hero_picked", "Hero_banned", "T_wins", "T_lose", "T_winrate"]]

    # Mengganti nama kolom
    filtered_data.columns = ["Hero", "Pick", "Ban", "Win", "Lose", "Winrate"]

    # Handling nilai NaN
    filtered_data = filtered_data.fillna("-")

    # Menambahkan % pada kolom 'Winrate'
    filtered_data['Winrate'] = filtered_data['Winrate'].astype(str) + ' %'

    # Menampilkan tabel data dengan fitur scroll
    st.write(
        f'<div style="max-height: 400px; overflow-y: auto;">'
        f'{filtered_data.to_html(index=False, escape=False)}</div>',
        unsafe_allow_html=True
    )

    # Input pengguna: pilih kolom untuk grafik
    selected_column = st.selectbox("Pilih Kolom untuk Grafik", filtered_data.columns[1:5])

    # Grafik berdasarkan pilihan pengguna
    if selected_column in ["Pick", "Ban", "Win", "Lose"]:
    # Mengurutkan data berdasarkan nilai terbesar pada kolom terpilih
        sorted_data = filtered_data.sort_values(by=selected_column, ascending=False)

    # Grafik batang untuk kolom Pick, Ban, Win, Lose
    fig = px.bar(
        sorted_data,
        x="Hero",
        y=selected_column,
        title=f"{selected_column} per Hero",
        labels={"Hero": "Hero", selected_column: selected_column},
        color="Hero",  # Mewarnai batang berdasarkan hero
        color_discrete_map={"Hero": "blue"},  # Menggunakan warna biru
        hover_name="Hero",  # Menampilkan nama hero pada hover
        text=selected_column,  # Menampilkan nilai pada batang
        category_orders={"Hero": sorted_data["Hero"].tolist()},  # Menyusun urutan kategori pada sumbu x
    )

    # Menambahkan layout untuk penataan grafik
    fig.update_layout(
        xaxis=dict(tickangle=-45, title_text='Hero'),
        yaxis=dict(title_text=selected_column, range=[0, sorted_data[selected_column].max() + 5]),
        showlegend=False,  # Menyembunyikan legenda karena warna diatur berdasarkan hero
        height=600,  # Menetapkan tinggi grafik
    )

    # Menampilkan grafik
    st.plotly_chart(fig)

# Konteks Data
elif choose == "Produksi Beras":
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1678924587662-d8c63e57eb11?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    st.title("Data Produksi Beras Pada Tahun 2020-2022 🌾") 
    
    st.markdown("<h1 class='sidebar-title'>Latar Belakang</h1>", unsafe_allow_html=True)
    st.write("Beras adalah komoditas pertanian penting di Indonesia dan merupakan tanaman utama yang dapat ditanam sepanjang tahun. Produktivitas padi atau beras dalam 3 tahun terakhir fluktuatif di semua provinsi di Indonesia.")
    st.write("Data ini diambil dari Badan Pusat Statistik Indonesia (https://www.bps.go.id/) untuk menggambarkan produksi, produktivitas, dan luas lahan yang digunakan untuk budidaya padi dari tahun 2020 hingga 2022.")
    
    # Membaca data
    data = pd.read_csv("Rice Production Indonesia 2020-2022.csv") 
    st.subheader('Tabel Data Produksi Beras 2020-2022', divider='green')
    
    # Membuat selectbox untuk memfilter tahun
    tahun_terpilih = st.selectbox("Pilih Tahun", data["Year"].unique())
    
    # Filter data berdasarkan tahun terpilih
    data_terfilter = data[data["Year"] == tahun_terpilih]
    
    # Menampilkan data yang sudah difilter
    st.write(f"Data untuk tahun {tahun_terpilih}:")
    st.dataframe(data_terfilter)
    
    # Menyiapkan palet warna
    palette = sns.color_palette("Set3", len(data_terfilter))

    # Membuat grafik bar dengan sumbu x dan y yang dibalik
    fig, ax = plt.subplots(figsize=(14, 12))
    bars = ax.barh(data_terfilter['Provinsi'], data_terfilter['Production.(ton)'], color=palette)

    # Menambahkan label dan warna pada grafik bar
    for bar, color in zip(bars, palette):
        bar.set_color(color)
        width = bar.get_width()
        ax.annotate(f'{width}',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0),  # 3 points horizontal offset
                    textcoords="offset points",
                    ha='left', va='center', color='black')

    # Mengatur label sumbu x dan y serta judul grafik
    ax.set_xlabel('Produksi (ton)')
    ax.set_ylabel('Provinsi')
    ax.set_title(f'Produksi Padi Nasional per Provinsi Tahun {tahun_terpilih }')

    # Menampilkan grafik bar
    st.subheader(f'Grafik Produksi Padi Tahun {tahun_terpilih }')
    st.pyplot(fig)
    
    # Membaca data
    st.markdown("<h1 class='sidebar-title'>Diagram</h1>", unsafe_allow_html=True)
    total_produksi_tahun = data.groupby("Year")["Production.(ton)"].sum()
    
    # Menampilkan total produksi
    st.write("Total Produksi Beras tiap Tahun:")
    st.dataframe(total_produksi_tahun)
    
    # Membuat diagram batang dari total produksi
    plt.figure(figsize=(12, 6))
    plt.bar(total_produksi_tahun.index, total_produksi_tahun.values)
    plt.xlabel("Tahun")
    plt.ylabel("Total Produksi")
    plt.title("Diagram Batang Total Produksi Beras per Tahun")
    plt.ylim(54000000, 55000000)
    plt.xticks(total_produksi_tahun.index, rotation=45)
    st.pyplot(plt)
    
    # Menghitung rata-rata produktivitas berdasarkan tahun
    rata_rata_produktivitas = data.groupby("Year")["Productivity(kw/ha)"].mean()
    
    # Menampilkan rata-rata produktivitas
    st.write("Rata-rata Produktivitas Beras tiap Tahun:")
    st.dataframe(rata_rata_produktivitas)
    
    # Membuat diagram garis dari rata-rata produktivitas
    plt.figure(figsize=(12, 6))
    plt.plot(rata_rata_produktivitas.index, rata_rata_produktivitas.values, marker='o')
    plt.xlabel("Tahun")
    plt.ylabel("Produktivitas")
    plt.title("Diagram Garis Rata-Rata Produktivitas Beras per Tahun")
    plt.ylim(43, 47)
    plt.xticks(rata_rata_produktivitas.index, rotation=45)
    st.pyplot(plt)
        
elif choose == "Penjualan Manga": 
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1678924587662-d8c63e57eb11?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.title('Data Penjualan Manga 📒')
    
    st.markdown("""
    <div style="text-align: justify;">
        <h4>Tentang Data Penjualan Manga</h4>
        <p>Data ini mencakup informasi penjualan manga terlaris sepanjang waktu. Tabel menyajikan detail tentang jumlah manga series, total volume manga, dan penjualan volume manga per rata-rata penjualan per volume.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader('Tabel Data Manga', divider='orange')
    # Membaca data
    data = pd.read_csv("best-selling-manga.csv") 
    st.dataframe(data)

    # Membuat tiga kolom pernyataan yang berbeda
    col1, col2, col3 = st.columns(3)
    # Kolom pertama
    with col1:
        st.markdown('<p style="text-align:center; ">Total Manga Series</p>', unsafe_allow_html=True)
        total_data = len(data)
        st.markdown(f'<p style="text-align:center; font-weight: bold;">{total_data}</p>', unsafe_allow_html=True)

    # Kolom kedua
    with col2:
        st.markdown('<p style="text-align:center;">Total Volume Semua Manga</p>', unsafe_allow_html=True)
        total_volume = data['No. of collected volumes'].sum()
        st.markdown(f'<p style="text-align:center;  font-weight: bold;">{total_volume}</p>', unsafe_allow_html=True)

    # Kolom ketiga
    with col3:
        st.markdown('<p style="text-align:center;"> Total Penjualan Volume Manga</p>', unsafe_allow_html=True)
        rata_rata_penjualan = data["Average sales per volume in million(s)"].sum()
        st.markdown(f'<p style="text-align:center; font-weight: bold;">{rata_rata_penjualan} million</p>', unsafe_allow_html=True)


    st.subheader('Untuk Memilih Judul Manga')

    # Input pilihan author
    selected_author = st.text_input('Cari Author:')
    if selected_author:
        filtered_df = data[data['Author(s)'].str.contains(selected_author, case=False)]

        # Tampilkan hasil filter
        st.subheader('Hasil Pemilahan Author:')
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning('Tidak ditemukan hasil untuk author yang dimasukkan.')
    # Menyiapkan palet warna
    #palette = sns.color_palette("Set3", len(data))

    # Menyusun data dalam urutan menurun berdasarkan penjualan
    sorted_data = sorted(zip(data['Manga series'], data['Average sales per volume in million(s)']), key=lambda x: x[1], reverse=True)
    # Mengambil 10 data teratas
    top_10_data = sorted_data[:10]

    # Mengekstrak kembali judul manga dan penjualan dari data teratas
    top_10_manga = [item[0] for item in top_10_data]
    top_10_sales = [item[1] for item in top_10_data]

    # Membuat dataframe dari data top 10
    top_10_df = pd.DataFrame({'Manga series': top_10_manga, 'Average sales per volume in million(s)': top_10_sales})

    # Mengatur warna secara manual untuk setiap bar
    custom_colors = ['#FF5733', '#FFC300', '#C70039', '#900C3F', '#581845',
                    '#006266', '#118C4E', '#06D6A0', '#17202A', '#774F0B']

    # Membuat grafik batang horizontal yang sudah diurutkan dengan warna-warna kustom
    fig = px.bar(top_10_df, y='Manga series', x='Average sales per volume in million(s)', title='Top 10 Manga dengan Penjualan Volume Terbanyak',
                color=custom_colors, orientation='h' )
    fig.update_traces(showlegend=False)
    st.plotly_chart(fig)

    # Menghitung jumlah berdasarkan 'Demographic'
    demographic_counts = data['Demographic'].value_counts()

    # Membuat diagram lingkaran
    fig = px.pie(names=demographic_counts.index, values=demographic_counts.values, title='Demographic Distribution')
    st.plotly_chart(fig)

elif choose == "Kejahatan US":
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1678924587662-d8c63e57eb11?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    st.title('Analisis Kejahatan di Amerika Serikat (1960-2014) 🚓')
    st.markdown("""
        **Sumber Data dan Analisis Keunggulan**

        Dataset ini berasal dari sumber terpercaya, menyajikan informasi tentang tingkat kejahatan di Amerika Serikat
        dari tahun 1960 hingga 2014. Analisis ini bertujuan untuk memberikan wawasan tentang tren dan pola kejahatan 
        selama beberapa dekade terakhir.

        Kami mengganti nama kolom dataset agar lebih mudah dipahami dalam bahasa Indonesia dan memberikan konteks tambahan
        untuk membantu interpretasi hasil analisis.
    """)
    st.subheader('Tabel Data Kejahatan US', divider='red')

    # Membaca data
    data = pd.read_csv("US_Crime_Rates_1960_2014.csv")

    # Dictionary untuk mapping nama kolom dalam bahasa Indonesia
    nama_kolom = {
        'Year': 'Tahun',
        'Population': 'Populasi',
        'Total': 'Total',
        'Violent': 'Kekerasan',
        'Property': 'Properti',
        'Murder': 'Pembunuhan',
        'Forcible_Rape': 'Perkosaan',
        'Robbery': 'Perampokan',
        'Aggravated_assault': 'Penyerangan_Berdarah',
        'Burglary': 'Pembobolan',
        'Larceny_Theft': 'Pencurian',
        'Vehicle_Theft': 'Pencurian_Kendaraan'
    }

    # Mengganti nama kolom menggunakan fungsi rename
    data = data.rename(columns=nama_kolom)

    # Menampilkan tabel data
    st.dataframe(data.set_index('Tahun'), use_container_width=True)

    # Palet warna yang berbeda untuk setiap grafik
    color_palette = px.colors.qualitative.Plotly

    # Filter tahun
    tahun_range = st.slider("Pilih Rentang Tahun", min_value=data['Tahun'].min(), max_value=data['Tahun'].max(), value=(data['Tahun'].min(), data['Tahun'].max()))

    # Filter data berdasarkan rentang tahun yang dipilih
    data_terfilter = data[(data['Tahun'] >= tahun_range[0]) & (data['Tahun'] <= tahun_range[1])]

    # Grafik untuk kolom kekerasan
    fig_kekerasan = px.line(data_terfilter, x='Tahun', y='Kekerasan', title='Trend Kekerasan', labels={'Kekerasan': 'Jumlah Kejahatan'}, line_shape="linear", color_discrete_sequence=[color_palette[0]])
    st.plotly_chart(fig_kekerasan)

    # Grafik untuk kolom pembunuhan
    fig_pembunuhan = px.bar(data_terfilter, x='Tahun', y='Pembunuhan', title='Jumlah Pembunuhan', labels={'Pembunuhan': 'Jumlah Kejahatan'}, color_discrete_sequence=[color_palette[1]])
    st.plotly_chart(fig_pembunuhan)

    # Grafik untuk kolom perampokan
    fig_perampokan = px.area(data_terfilter, x='Tahun', y='Perampokan', title='Jumlah Perampokan', labels={'Perampokan': 'Jumlah Kejahatan'}, color_discrete_sequence=[color_palette[2]])
    st.plotly_chart(fig_perampokan)

    # Grafik untuk kolom pencurian
    fig_pencurian = px.scatter(data_terfilter, x='Tahun', y='Pencurian', title='Jumlah Pencurian', labels={'Pencurian': 'Jumlah Kejahatan'}, color_discrete_sequence=[color_palette[3]])
    st.plotly_chart(fig_pencurian)