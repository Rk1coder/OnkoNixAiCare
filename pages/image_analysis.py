import streamlit as st
import cv2
import numpy as np
from utils.image_processing import preprocess_image, detect_anomalies

def analyze_bronchoscopy_image(image):
    """
    Bronkoskopi görüntüsünü analiz eder
    """
    # Görüntü ön işleme
    processed_image = preprocess_image(image)
    
    # Anormallik tespiti
    anomaly_score = detect_anomalies(processed_image)
    
    return {
        'processed_image': processed_image,
        'anomaly_score': anomaly_score,
        'confidence': 0.87  # Demo değer
    }

def show_analysis_results(results):
    """
    Analiz sonuçlarını gösterir
    """
    st.markdown("### Analiz Sonuçları")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(results['processed_image'], caption='İşlenmiş Görüntü')
    
    with col2:
        st.markdown(f"""
        <div class='info-box'>
            <h4>Tespit Sonuçları</h4>
            <p>Anormallik Skoru: {results['anomaly_score']:.2%}</p>
            <p>Güven Oranı: {results['confidence']:.2%}</p>
        </div>
        """, unsafe_allow_html=True)

def show_historical_analysis():
    """
    Geçmiş analizleri gösterir
    """
    # Demo geçmiş analiz verileri
    history = pd.DataFrame({
        'Tarih': ['2024-01-15', '2024-01-30', '2024-02-15'],
        'Anormallik Skoru': [0.15, 0.12, 0.10],
        'Güven Oranı': [0.87, 0.89, 0.91]
    })
    
    st.markdown("### Geçmiş Analizler")
    st.dataframe(history)
