import streamlit as st
import pandas as pd
from datetime import datetime

def show_patient_details(patient_id):
    """
    Hasta detaylarını gösterir
    """
    # Demo hasta verileri
    patient_data = {
        'Hasta ID': patient_id,
        'Ad Soyad': 'Ahmet Yılmaz',
        'Doğum Tarihi': '1969-05-15',
        'Tanı': 'Akciğer Kanseri - Evre 2',
        'Tedavi Başlangıç': '2024-01-15'
    }
    
    st.markdown("### Hasta Detayları")
    for key, value in patient_data.items():
        st.text(f"{key}: {value}")

def show_blood_tests():
    """
    Kan testi sonuçlarını gösterir
    """
    # Demo kan testi verileri
    blood_tests = pd.DataFrame({
        'Tarih': ['2024-01-15', '2024-01-30', '2024-02-15'],
        'WBC': [7.2, 6.8, 7.0],
        'RBC': [4.8, 4.9, 5.0],
        'HGB': [14.5, 14.8, 14.7],
        'PLT': [250, 265, 260]
    })
    
    st.markdown("### Kan Testi Sonuçları")
    st.dataframe(blood_tests)

def show_treatment_history():
    """
    Tedavi geçmişini gösterir
    """
    # Demo tedavi geçmişi
    treatments = pd.DataFrame({
        'Tarih': ['2024-01-15', '2024-01-30', '2024-02-15'],
        'İşlem': ['Kemoterapi', 'Kontrol', 'Kemoterapi'],
        'Notlar': ['İlk seans', 'Yan etki yok', 'İkinci seans']
    })
    
    st.markdown("### Tedavi Geçmişi")
    st.dataframe(treatments)
