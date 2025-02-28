import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="OnkoNixAI - Akciğer Kanseri Analiz Platformu",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS yükleme - cache ile
@st.cache_data
def load_css():
    with open('assets/style.css') as f:
        return f'<style>{f.read()}</style>'

st.markdown(load_css(), unsafe_allow_html=True)

# Demo verileri için cache
@st.cache_data
def get_sample_data():
    return pd.DataFrame({
        'Tarih': pd.date_range(start='2024-01-01', periods=10, freq='D'),
        'Hasta_Sayisi': [15, 18, 12, 20, 25, 22, 19, 23, 21, 24],
        'Basari_Orani': [92, 93, 91, 94, 95, 93, 92, 94, 93, 94]
    })

def main():
    st.markdown("<h1 class='main-header'>OnkoNixAI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-header'>Akciğer Kanseri Teşhis ve Tedavi Platformu</p>", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("<h2 class='section-header'>Navigasyon</h2>", unsafe_allow_html=True)
        page = st.radio(
            "",
            ["Ana Sayfa", "Hasta Bilgileri", "Görüntü Analizi", "Rapor Analizi", "Doz Hesaplama"]
        )

    if page == "Ana Sayfa":
        show_dashboard()
    elif page == "Hasta Bilgileri":
        show_patient_info()
    elif page == "Görüntü Analizi":
        show_image_analysis()
    elif page == "Rapor Analizi":
        show_report_analysis()
    elif page == "Doz Hesaplama":
        show_dose_calculator()

@st.cache_data
def create_metric_card(title, value):
    return f"""
    <div class='metric-card'>
        <h3>{title}</h3>
        <h2>{value}</h2>
    </div>
    """

def show_dashboard():
    # Metrik kartları
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(create_metric_card("Aktif Hasta", "127"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card("Günlük Analiz", "24"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card("Başarı Oranı", "94%"), unsafe_allow_html=True)

    st.markdown("<h2 class='section-header'>Analiz Metrikleri</h2>", unsafe_allow_html=True)

    # Cached veri kullanımı
    df = get_sample_data()

    # Grafikleri yan yana göster
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(df, x='Tarih', y='Hasta_Sayisi',
                    title='Günlük Hasta Analizi',
                    template='plotly_white')
        fig1.update_traces(line_color='#3498db')
        fig1.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

    with col2:
        fig2 = px.line(df, x='Tarih', y='Basari_Orani',
                    title='Teşhis Başarı Oranı Trendi',
                    template='plotly_white')
        fig2.update_traces(line_color='#27ae60')
        fig2.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    st.markdown("""
    <div class='info-box'>
        <h4>Sistem Performans Özeti</h4>
        <p>• Son 30 günde %94 doğruluk oranı</p>
        <p>• Ortalama analiz süresi: 15 dakika</p>
        <p>• Aktif hasta takip sayısı: 127</p>
    </div>
    """, unsafe_allow_html=True)

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

def show_report_analysis():
    st.markdown("## Hasta Rapor Analizi")
    # Add your report analysis code here.  This is a placeholder.
    st.write("Bu bölümde hasta rapor analizleri yer alacaktır.")


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