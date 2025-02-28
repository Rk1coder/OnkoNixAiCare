import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="OnkoNixAI - Akciğer Kanseri Analiz Platformu",
    page_icon="🫁",
    layout="wide"
)

with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='main-header'>OnkoNixAI</h1>", unsafe_allow_html=True)
    st.markdown("### Akciğer Kanseri Teşhis ve Tedavi Platformu")

    # Sidebar
    st.sidebar.title("Navigasyon")
    page = st.sidebar.radio(
        "Sayfa Seçin:",
        ["Ana Sayfa", "Hasta Bilgileri", "Görüntü Analizi", "Doz Hesaplama"]
    )

    if page == "Ana Sayfa":
        show_dashboard()
    elif page == "Hasta Bilgileri":
        show_patient_info()
    elif page == "Görüntü Analizi":
        show_image_analysis()
    elif page == "Doz Hesaplama":
        show_dose_calculator()

def show_dashboard():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3>Aktif Hasta</h3>
            <h2>127</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3>Günlük Analiz</h3>
            <h2>24</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h3>Başarı Oranı</h3>
            <h2>94%</h2>
        </div>
        """, unsafe_allow_html=True)

    # Demo hasta verileri
    sample_data = {
        'Tarih': pd.date_range(start='2024-01-01', periods=10, freq='D'),
        'Hasta_Sayisi': [15, 18, 12, 20, 25, 22, 19, 23, 21, 24],
        'Basari_Orani': [92, 93, 91, 94, 95, 93, 92, 94, 93, 94]
    }
    df = pd.DataFrame(sample_data)

    # Hasta sayısı grafiği
    fig1 = px.line(df, x='Tarih', y='Hasta_Sayisi',
                   title='Günlük Hasta Analizi',
                   template='plotly_white')
    st.plotly_chart(fig1, use_container_width=True)

    # Başarı oranı grafiği
    fig2 = px.line(df, x='Tarih', y='Basari_Orani',
                   title='Teşhis Başarı Oranı Trendi',
                   template='plotly_white')
    st.plotly_chart(fig2, use_container_width=True)

def show_patient_info():
    st.markdown("## Hasta Bilgileri")
    demo_patient = {
        "Ad": "Ahmet",
        "Soyad": "Yılmaz",
        "Yaş": 55,
        "Cinsiyet": "Erkek",
        "Tanı Tarihi": "2024-01-15"
    }
    
    col1, col2 = st.columns(2)
    with col1:
        for key, value in demo_patient.items():
            st.text(f"{key}: {value}")
    
    with col2:
        st.markdown("""
        <div class='info-box'>
            <h4>Son Kontrol Bilgileri</h4>
            <p>Tarih: 2024-02-01</p>
            <p>Durum: Stabil</p>
        </div>
        """, unsafe_allow_html=True)

def show_image_analysis():
    st.markdown("## Bronkoskopi Görüntü Analizi")
    uploaded_file = st.file_uploader("Bronkoskopi görüntüsü yükleyin", type=['jpg', 'png'])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Yüklenen Görüntü')
        st.markdown("""
        <div class='info-box'>
            <h4>Analiz Sonuçları</h4>
            <p>Anormallik Tespit Oranı: 15%</p>
            <p>Güven Skoru: 87%</p>
        </div>
        """, unsafe_allow_html=True)

def show_dose_calculator():
    st.markdown("## Tedavi Doz Hesaplama")
    
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Hasta Kilosu (kg)", min_value=30, max_value=150)
        height = st.number_input("Boy (cm)", min_value=100, max_value=220)
        age = st.number_input("Yaş", min_value=18, max_value=100)
    
    with col2:
        st.markdown("""
        <div class='info-box'>
            <h4>Önerilen Doz</h4>
            <p>Günlük Doz: 250mg</p>
            <p>Tedavi Süresi: 6 hafta</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
