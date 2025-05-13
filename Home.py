import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Analisis Jalur Mandiri PTN", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("DataUniversitas.xlsx")
    df['UKT_Min'] = df['UKT / Semester'].str.extract(r'Rp\s*([\d\.]+)', expand=False).str.replace('.', '', regex=False).astype(float)
    df['UKT_Max'] = df['UKT / Semester'].str.extract(r'–\s*Rp\s*([\d\.]+)', expand=False).str.replace('.', '', regex=False).astype(float)
    df['Wilayah'] = df['Lokasi PTN'].apply(lambda x: 'Jawa' if 'Jawa' in x else 'Luar Jawa')
    return df

df = load_data()

# Judul dan deskripsi
st.title("📊 Dashboard Analisis Jalur Mandiri PTN")
st.markdown("Selamat datang di dashboard analisis **daya tampung** dan **UKT Jalur Mandiri** di Perguruan Tinggi Negeri. Gunakan navbar di samping untuk mengeksplorasi data berdasarkan wilayah.")
st.markdown(""" 
             ## Kelompok 10 E:
            - Ngakan Putu Bagus Ananta Wijaya
            - NI GUSTI AYU AGUNG INDRASWARI
            - Ni Kadek Dwi Marhaeni
            - Ni Komang Ariasih
            """)

st.sidebar.title("🧭 Filter Data")

# Filter wilayah
wilayah_filter = st.sidebar.multiselect("Pilih Wilayah", options=df['Wilayah'].unique(), default=[])

# Filter berdasarkan hasil wilayah
if wilayah_filter:
    filtered_df = df[df['Wilayah'].isin(wilayah_filter)]
else:
    filtered_df = df

# Metrik ringkasan
st.write("")
col1, col2, col3 = st.columns(3)
col1.metric("Jumlah PTN", f"{filtered_df['PTN'].nunique()} PTN")
col2.metric("Jumlah Prodi", f"{filtered_df['Program Studi'].nunique()} Prodi")
col3.metric("Total Daya Tampung", f"{int(filtered_df['Daya Tampung Jalur Mandiri'].sum()):,}")

# Tabs visualisasi
tab1, tab2, tab3, tab4 = st.tabs(["📌 Daya Tampung", "💸 UKT", "🏫 PTN & Prodi", "🌍 Wilayah"])

with tab1:
    st.subheader("Distribusi Daya Tampung Jalur Mandiri")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.histplot(filtered_df['Daya Tampung Jalur Mandiri'], bins=30, kde=True, color="#2b83ba", ax=ax1)
    ax1.set_title('Distribusi Daya Tampung Jalur Mandiri')
    st.pyplot(fig1)
    st.info(f"Daya tampung paling umum berkisar di angka {int(filtered_df['Daya Tampung Jalur Mandiri'].median())} mahasiswa per program studi.")

with tab2:
    st.subheader("Rata-rata UKT Minimum dan Maksimum per PTN")
    ukt_by_ptn = filtered_df.groupby('PTN')[['UKT_Min', 'UKT_Max']].mean().sort_values('UKT_Max', ascending=False)
    fig2, ax2 = plt.subplots(figsize=(10, 12))
    ukt_by_ptn.plot(kind='barh', ax=ax2, color=['#abdda4', '#f46d43'])
    ax2.set_title("Rata-rata UKT Minimum dan Maksimum per PTN")
    st.pyplot(fig2)
    st.info("Beberapa PTN memiliki selisih besar antara UKT minimum dan maksimum, menunjukkan variasi jalur pembayaran atau program studi yang ditawarkan.")

    st.subheader("Top 10 PTN dengan Rata-rata UKT Tertinggi")
    ukt_rata2 = filtered_df.groupby('PTN')[['UKT_Min', 'UKT_Max']].mean()
    ukt_rata2['UKT_Avg'] = (ukt_rata2['UKT_Min'] + ukt_rata2['UKT_Max']) / 2
    top_ukt = ukt_rata2.sort_values('UKT_Avg', ascending=False).head(10)
    fig3, ax3 = plt.subplots(figsize=(10,6))
    top_ukt['UKT_Avg'].plot(kind='barh', color='#d7191c', ax=ax3)
    ax3.set_title("Top 10 PTN dengan UKT Rata-rata Tertinggi")
    st.pyplot(fig3)
    st.info(f"PTN dengan UKT rata-rata tertinggi adalah **{top_ukt.index[0]}** dengan kisaran Rp {int(top_ukt['UKT_Avg'].max()):,}")

    st.subheader("Distribusi UKT Maksimal Berdasarkan Wilayah")
    fig6, ax6 = plt.subplots(figsize=(8,6))
    sns.boxplot(data=filtered_df, x='Wilayah', y='UKT_Max', palette="Set2", ax=ax6)
    ax6.set_title("Distribusi UKT Maksimal Berdasarkan Wilayah")
    st.pyplot(fig6)
    st.info("Wilayah Jawa cenderung memiliki variasi UKT maksimal yang lebih tinggi dibandingkan luar Jawa.")

with tab3:
    st.subheader("10 Program Studi dengan Daya Tampung Terbanyak")
    top_programs = filtered_df.sort_values('Daya Tampung Jalur Mandiri', ascending=False).head(10)
    st.dataframe(top_programs[['PTN', 'Program Studi', 'Daya Tampung Jalur Mandiri']])
    st.info(f"Prodi dengan daya tampung tertinggi adalah **{top_programs.iloc[0]['Program Studi']}** di **{top_programs.iloc[0]['PTN']}** dengan {top_programs.iloc[0]['Daya Tampung Jalur Mandiri']} kursi.")

    st.subheader("Top 10 Program Studi dengan UKT Maksimal Tertinggi")
    top_ukt_prodi = filtered_df[['PTN', 'Program Studi', 'UKT_Max']].sort_values('UKT_Max', ascending=False).head(10)
    fig5, ax5 = plt.subplots(figsize=(10,6))
    sns.barplot(data=top_ukt_prodi, y='Program Studi', x='UKT_Max', hue='PTN', palette='viridis', ax=ax5)
    ax5.set_title("Top 10 Program Studi dengan UKT Maksimal Tertinggi")
    st.pyplot(fig5)
    st.info(f"UKT tertinggi tercatat di program studi **{top_ukt_prodi.iloc[0]['Program Studi']}** di **{top_ukt_prodi.iloc[0]['PTN']}** sebesar Rp {int(top_ukt_prodi.iloc[0]['UKT_Max']):,}")

    with st.expander("📄 Lihat Tabel Lengkap"):
        st.table(top_ukt_prodi.reset_index(drop=True))

with tab4:
    st.subheader("Total Daya Tampung per Lokasi PTN")
    dt_lokasi = filtered_df.groupby('Lokasi PTN')['Daya Tampung Jalur Mandiri'].sum().sort_values(ascending=False)
    fig4, ax4 = plt.subplots(figsize=(12,6))
    dt_lokasi.plot(kind='bar', color='#1a9641', ax=ax4)
    ax4.set_title("Total Daya Tampung Jalur Mandiri per Lokasi PTN")
    ax4.set_ylabel("Total Daya Tampung")
    st.pyplot(fig4)
    lokasi_tertinggi = dt_lokasi.idxmax()
    st.info(f"Lokasi PTN dengan total daya tampung tertinggi adalah **{lokasi_tertinggi}** dengan {int(dt_lokasi.max()):,} kursi.")
