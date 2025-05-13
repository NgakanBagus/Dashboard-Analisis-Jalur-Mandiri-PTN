import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Load model yang sudah disimpan
model = joblib.load('Models/model_ukt.pkl')

# Membaca data PTN untuk referensi
df_ptn = pd.read_excel('DataUniversitas.xlsx')

# Label Encoder untuk 'Pulau PTN' dan 'Kategori UKT' (sesuai dengan preprocessing sebelumnya)
label_encoder_pulau = LabelEncoder()
df_ptn['Pulau PTN'] = label_encoder_pulau.fit_transform(df_ptn['Pulau PTN'])

# Fungsi untuk mendapatkan data berdasarkan nama PTN
def get_ptn_data(ptn_name):
    ptn_data = df_ptn[df_ptn['PTN'] == ptn_name].iloc[0]
    return ptn_data['Daya Tampung Jalur Mandiri'], ptn_data['Pulau PTN']

# Fungsi untuk mengembalikan kategori UKT
def reverse_label_ukt(encoded_value):
    # Menentukan kategori UKT yang sesuai dengan label encoding
    return {0: 'Rendah', 1: 'Sedang', 2: 'Tinggi'}[encoded_value]

# Judul aplikasi
st.title('Klasifikasi Kategori UKT berdasarkan PTN')

# Input nama PTN
ptn_name = st.selectbox('Pilih PTN', df_ptn['PTN'].unique())

# Ketika pengguna memilih PTN
if ptn_name:
    daya_tampung, pulau_ptn = get_ptn_data(ptn_name)
    
    # Menampilkan informasi PTN yang dipilih
    st.write(f"**Nama PTN:** {ptn_name}")
    st.write(f"**Daya Tampung Jalur Mandiri:** {daya_tampung}")
    st.write(f"**Pulau PTN:** {label_encoder_pulau.inverse_transform([pulau_ptn])[0]}")

    # Menyusun fitur untuk prediksi
    features = [[daya_tampung, pulau_ptn]]
    
    # Prediksi kategori UKT
    prediction = model.predict(features)
    
    # Mengembalikan hasil prediksi ke kategori asli
    kategori_ukt = reverse_label_ukt(prediction[0])
    
    # Menampilkan hasil prediksi
    st.write(f"**Kategori UKT:** {kategori_ukt}")
