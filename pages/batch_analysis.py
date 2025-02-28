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
            <li>rapor_metni: Hasta rapor metni</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("CSV Dosyası Yükleyin", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # CSV dosyasını oku
            df = pd.read_csv(StringIO(uploaded_file.getvalue().decode('utf-8')))
            
            if all(col in df.columns for col in ['hasta_id', 'rapor_tarihi', 'rapor_metni']):
                st.success("Dosya başarıyla yüklendi!")
                
                # Rapor analiz aracını başlat
                analyzer = ReportAnalyzer()
                
                # İlerleme çubuğu
                progress_bar = st.progress(0)
                
                # Analiz sonuçlarını sakla
                results = []
                
                # Her raporu analiz et
                for i, row in df.iterrows():
                    analysis = analyzer.analyze_report(row['rapor_metni'])
                    
                    results.append({
                        'hasta_id': row['hasta_id'],
                        'rapor_tarihi': row['rapor_tarihi'],
                        'evre': analysis['stage'],
                        'olcumler': len(analysis['measurements']),
                        'risk_skoru': len(analysis['findings'].get('tani', [])) + 
                                    len(analysis['findings'].get('metastaz', []))
                    })
                    
                    # İlerleme çubuğunu güncelle
                    progress_bar.progress((i + 1) / len(df))
                
                # Sonuçları DataFrame'e çevir
                results_df = pd.DataFrame(results)
                
                # Özet istatistikler
                st.markdown("### Analiz Sonuçları")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h3>Toplam Rapor</h3>
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
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h3>Evre Dağılımı</h3>
                        <h2>{results_df['evre'].value_counts().index[0]}</h2>
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
                
                # Evre dağılımı
                evre_dagilimi = results_df['evre'].value_counts()
                fig2 = px.pie(values=evre_dagilimi.values, 
                            names=evre_dagilimi.index,
                            title='Evre Dağılımı')
                st.plotly_chart(fig2, use_container_width=True)
                
                # Detaylı tablo
                st.markdown("### Detaylı Rapor Listesi")
                st.dataframe(results_df, use_container_width=True)
                
            else:
                st.error("CSV dosyası gerekli sütunları içermiyor. Lütfen format bilgisini kontrol edin.")
        
        except Exception as e:
            st.error(f"Dosya işlenirken bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    analyze_batch_reports()
