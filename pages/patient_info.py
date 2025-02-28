import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_analysis import analyze_blood_values, analyze_pathology_report

def show_patient_details(patient_id):
    """
    Hasta detaylarını gösterir
    """
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
    Kan testi sonuçlarını gösterir ve analiz eder
    """
    st.markdown("### Kan Testi Sonuçları")

    # Demo kan testi verileri
    blood_tests = {
        'WBC': 6.8,    # Beyaz kan hücresi
        'RBC': 4.9,    # Kırmızı kan hücresi
        'HGB': 14.8,   # Hemoglobin
        'PLT': 265,    # Trombosit
        'CEA': 4.2,    # Tümör belirteci
        'CYFRA': 2.8,  # CYFRA 21-1
        'NSE': 15.5,   # Nöron spesifik enolaz
        'LDH': 250,    # Laktat dehidrogenaz
        'ALP': 130     # Alkalen fosfataz
    }

    # Sonuçları analiz et
    analysis = analyze_blood_values(blood_tests)

    # Sonuçları görüntüle
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Test Değerleri")
        for param, result in analysis['test_results'].items():
            status_color = {
                'Normal': 'success-text',
                'Düşük': 'warning-text',
                'Yüksek': 'warning-text'
            }[result['status']]

            st.markdown(f"""
            <div style='margin-bottom: 10px;'>
                <strong>{param}:</strong> 
                <span class='{status_color}'>{result['value']}</span>
                <br/>
                <small>Referans Aralığı: {result['reference_range']}</small>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### Risk Değerlendirmesi")
        risk_score = analysis['risk_score']

        # Risk skoruna göre renk belirleme
        if risk_score < 3:
            risk_color = 'success-text'
        elif risk_score < 7:
            risk_color = 'warning-text'
        else:
            risk_color = 'error-text'

        st.markdown(f"""
        <div class='info-box'>
            <h4>Risk Skoru: <span class='{risk_color}'>{risk_score:.1f}/10</span></h4>
            <p>Bu skor, test sonuçlarına dayalı genel risk değerlendirmesini gösterir.</p>
        </div>
        """, unsafe_allow_html=True)

def show_pathology_results():
    """
    Patoloji sonuçlarını gösterir
    """
    st.markdown("### Patoloji Sonuçları")

    # Demo patoloji verileri
    pathology_data = {
        'histology': 'Adenokarsinom',
        'stage': 'Stage II',
        'differentiation': 'Orta derecede diferansiye'
    }

    analysis = analyze_pathology_report(pathology_data)

    st.markdown(f"""
    <div class='info-box'>
        <h4>Patoloji Raporu</h4>
        <p><strong>Kanser Tipi:</strong> {analysis['cancer_type']}</p>
        <p><strong>Histoloji:</strong> {analysis['histology']}</p>
        <p><strong>Evre:</strong> {analysis['stage']}</p>
        <p><strong>Diferansiyasyon:</strong> {analysis['differentiation']}</p>
    </div>
    """, unsafe_allow_html=True)

def show_treatment_history():
    """
    Tedavi geçmişini gösterir
    """
    st.markdown("### Tedavi Geçmişi")

    treatments = pd.DataFrame({
        'Tarih': ['2024-01-15', '2024-01-30', '2024-02-15'],
        'İşlem': ['Kemoterapi', 'Kontrol', 'Kemoterapi'],
        'Notlar': ['İlk seans', 'Yan etki yok', 'İkinci seans'],
        'Kan Değerleri': ['Normal', 'WBC düşük', 'Normal'],
        'Doz Ayarlaması': ['Standart', 'Doz azaltma', 'Standart']
    })

    st.dataframe(treatments, use_container_width=True)

def main():
    st.markdown("## Hasta Bilgi Sistemi")

    tabs = st.tabs([
        "Hasta Detayları",
        "Kan Testleri",
        "Patoloji",
        "Tedavi Geçmişi"
    ])

    with tabs[0]:
        show_patient_details("P001")

    with tabs[1]:
        show_blood_tests()

    with tabs[2]:
        show_pathology_results()

    with tabs[3]:
        show_treatment_history()

if __name__ == "__main__":
    main()