import streamlit as st
from utils.data_analysis import calculate_treatment_dose

def calculate_dose():
    """
    Tedavi dozunu hesaplar ve gösterir
    """
    st.markdown("### Doz Hesaplama")
    
    # Hasta bilgileri
    weight = st.number_input("Kilo (kg)", min_value=30, max_value=150, value=70)
    age = st.number_input("Yaş", min_value=18, max_value=100, value=50)
    
    # Kan değerleri
    st.markdown("#### Kan Değerleri")
    wbc = st.number_input("WBC", min_value=0.0, max_value=20.0, value=7.0)
    
    # Doz hesaplama
    blood_values = {'WBC': wbc}
    dose = calculate_treatment_dose(weight, age, blood_values)
    
    st.markdown(f"""
    <div class='info-box'>
        <h4>Hesaplanan Doz</h4>
        <p>Günlük Doz: {dose} mg</p>
        <p>Haftalık Doz: {dose * 7} mg</p>
    </div>
    """, unsafe_allow_html=True)

def show_dose_history():
    """
    Doz geçmişini gösterir
    """
    # Demo doz geçmişi
    history = pd.DataFrame({
        'Tarih': ['2024-01-15', '2024-01-30', '2024-02-15'],
        'Doz (mg)': [150, 150, 145],
        'Notlar': ['Başlangıç dozu', 'Devam', 'Doz azaltma']
    })
    
    st.markdown("### Doz Geçmişi")
    st.dataframe(history)
