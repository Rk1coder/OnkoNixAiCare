import streamlit as st
import pandas as pd
import plotly.express as px
from utils.report_analyzer import ReportAnalyzer
from io import StringIO

def analyze_batch_reports():
    st.markdown("<h2 class='section-header'>Toplu Rapor Analizi</h2>", unsafe_allow_html=True)

    # CSV format bilgisi
    st.markdown("""
    <div class='info-box'>
        <h4>CSV Dosya Formatı</h4>
        <p>CSV dosyanız aşağıdaki sütunları içermelidir:</p>
        <ul>
            <li>hasta_id: Hasta kimlik numarası</li>
            <li>rapor_tarihi: Rapor tarihi (YYYY-MM-DD)</li>
            <li>wbc: Beyaz kan hücresi değeri</li>
            <li>rbc: Kırmızı kan hücresi değeri</li>
            <li>hgb: Hemoglobin değeri</li>
            <li>plt: Trombosit değeri</li>
            <li>cea: CEA değeri</li>
            <li>cyfra: CYFRA 21-1 değeri</li>
            <li>nse: NSE değeri</li>
            <li>ldh: LDH değeri</li>
            <li>alp: ALP değeri</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("CSV Dosyası Yükleyin", type=['csv'])

    if uploaded_file is not None:
        try:
            # CSV dosyasını oku
            df = pd.read_csv(StringIO(uploaded_file.getvalue().decode('utf-8')))

            if all(col in df.columns for col in ['hasta_id', 'rapor_tarihi']):
                st.success("Dosya başarıyla yüklendi!")

                # İlerleme çubuğu
                progress_bar = st.progress(0)

                # Her hasta için risk skorunu hesapla
                risk_scores = []
                analyzed_data = []

                for i, row in df.iterrows():
                    # Test değerlerini analiz et
                    test_values = {
                        'WBC': row.get('wbc', None),
                        'RBC': row.get('rbc', None),
                        'HGB': row.get('hgb', None),
                        'PLT': row.get('plt', None),
                        'CEA': row.get('cea', None),
                        'CYFRA': row.get('cyfra', None),
                        'NSE': row.get('nse', None),
                        'LDH': row.get('ldh', None),
                        'ALP': row.get('alp', None)
                    }

                    # Null olmayan değerleri filtrele
                    test_values = {k: v for k, v in test_values.items() if v is not None}

                    if test_values:
                        analyzer = ReportAnalyzer()
                        analysis = analyzer.analyze_blood_values(test_values)

                        analyzed_data.append({
                            'hasta_id': row['hasta_id'],
                            'rapor_tarihi': row['rapor_tarihi'],
                            'risk_skoru': analysis['risk_score'],
                            'anormal_parametreler': sum(1 for result in analysis['test_results'].values() if result['status'] != 'Normal')
                        })

                    # İlerleme çubuğunu güncelle
                    progress_bar.progress((i + 1) / len(df))

                # Analiz sonuçlarını DataFrame'e çevir
                results_df = pd.DataFrame(analyzed_data)

                # Özet istatistikler
                st.markdown("### Analiz Sonuçları")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h3>Toplam Hasta</h3>
                        <h2>{len(results_df)}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    avg_risk = results_df['risk_skoru'].mean()
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h3>Ortalama Risk Skoru</h3>
                        <h2>{avg_risk:.1f}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    high_risk = len(results_df[results_df['risk_skoru'] > 7])
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h3>Yüksek Riskli Hasta</h3>
                        <h2>{high_risk}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                # Grafikler
                st.markdown("### Trend Analizi")

                # Risk skoru trendi
                fig1 = px.line(results_df, 
                             x='rapor_tarihi', 
                             y='risk_skoru',
                             title='Risk Skoru Trendi')
                fig1.update_traces(line_color='#3498db')
                st.plotly_chart(fig1, use_container_width=True)

                # Anormal parametre dağılımı
                fig2 = px.histogram(results_df,
                                  x='anormal_parametreler',
                                  title='Anormal Parametre Dağılımı',
                                  labels={'anormal_parametreler': 'Anormal Parametre Sayısı'})
                st.plotly_chart(fig2, use_container_width=True)

                # Detaylı tablo
                st.markdown("### Detaylı Rapor Listesi")
                st.dataframe(results_df.sort_values('risk_skoru', ascending=False), use_container_width=True)

            else:
                st.error("CSV dosyası gerekli sütunları içermiyor. Lütfen format bilgisini kontrol edin.")

        except Exception as e:
            st.error(f"Dosya işlenirken bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    analyze_batch_reports()