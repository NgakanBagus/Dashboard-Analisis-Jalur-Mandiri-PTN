import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

model = joblib.load('Models/model_ukt.pkl')

df_ptn = pd.read_excel('DataUniversitas.xlsx')

label_encoder_pulau = LabelEncoder()
df_ptn['Pulau PTN'] = label_encoder_pulau.fit_transform(df_ptn['Pulau PTN'])

def get_ptn_data(ptn_name):
    ptn_data = df_ptn[df_ptn['PTN'] == ptn_name].iloc[0]
    return ptn_data['Daya Tampung Jalur Mandiri'], ptn_data['Pulau PTN']

def reverse_label_ukt(encoded_value):
    return {0: 'Rendah', 1: 'Sedang', 2: 'Tinggi'}[encoded_value]

st.title('Klasifikasi Kategori UKT berdasarkan PTN')

ptn_name = st.selectbox('Pilih PTN', df_ptn['PTN'].unique())

if ptn_name:
    daya_tampung, pulau_ptn = get_ptn_data(ptn_name)
    
    st.write(f"**Nama PTN:** {ptn_name}")
    st.write(f"**Daya Tampung Jalur Mandiri:** {daya_tampung}")
    st.write(f"**Pulau PTN:** {label_encoder_pulau.inverse_transform([pulau_ptn])[0]}")

    features = [[daya_tampung, pulau_ptn]]
    
    prediction = model.predict(features)
    
    kategori_ukt = reverse_label_ukt(prediction[0])
    
    st.write(f"**Kategori UKT:** {kategori_ukt}")
