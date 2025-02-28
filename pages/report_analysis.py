import streamlit as st
import pandas as pd
from utils.report_analyzer import ReportAnalyzer

def show_report_analysis():
    st.markdown("<h2 class='section-header'>Hasta Rapor Analizi</h2>", unsafe_allow_html=True)
    
    # Rapor analiz aracını başlat
    analyzer = ReportAnalyzer()
    
    # Rapor girişi
    report_text = st.text_area(
        "Hasta raporunu buraya yapıştırın:",
        height=200,
        help="Patoloji raporu, radyoloji raporu veya diğer tıbbi raporları yapıştırın."
    )
    
    if st.button("Raporu Analiz Et"):
        if report_text:
            with st.spinner("Rapor analiz ediliyor..."):
                # Raporu analiz et
                analysis_results = analyzer.analyze_report(report_text)
                summary = analyzer.generate_summary(analysis_results)
                
                # Sonuçları göster
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Özet Bulgular")
                    st.markdown(f"""
                    <div class='info-box'>
                        <pre>{summary}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("#### Detaylı Analiz")
                    
                    # Ölçümler
                    if analysis_results['measurements']:
                        st.markdown("##### Tespit Edilen Ölçümler")
                        measurements_df = pd.DataFrame(analysis_results['measurements'])
                        st.dataframe(measurements_df)
                    
                    # Evre bilgisi
                    if analysis_results['stage']:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <h3>Hastalık Evresi</h3>
                            <h2>Evre {analysis_results['stage']}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Önemli bulgular için ayrı bir bölüm
                st.markdown("#### Kategorilere Göre Bulgular")
                for category, findings in analysis_results['findings'].items():
                    if findings:
                        with st.expander(f"{category.title()} ile İlgili Bulgular"):
                            for finding in findings:
                                st.markdown(f"- {finding}")
        else:
            st.warning("Lütfen analiz edilecek bir rapor metni girin.")

if __name__ == "__main__":
    show_report_analysis()
