import pandas as pd
import numpy as np

def analyze_blood_values(blood_data):
    """
    Kan değerlerini analiz eder
    """
    # Demo kan değeri analizi
    reference_ranges = {
        'WBC': (4.5, 11.0),
        'RBC': (4.5, 5.5),
        'HGB': (13.5, 17.5),
        'PLT': (150, 450)
    }
    
    results = {}
    for param, (min_val, max_val) in reference_ranges.items():
        if param in blood_data:
            value = blood_data[param]
            status = 'Normal'
            if value < min_val:
                status = 'Düşük'
            elif value > max_val:
                status = 'Yüksek'
            results[param] = {'value': value, 'status': status}
    
    return results

def calculate_treatment_dose(weight, age, blood_values=None):
    """
    Tedavi dozunu hesaplar
    """
    # Demo doz hesaplama
    base_dose = weight * 2  # mg
    
    # Yaşa göre düzeltme
    if age > 65:
        base_dose *= 0.8
    
    # Kan değerlerine göre düzeltme (demo)
    if blood_values and 'WBC' in blood_values:
        if blood_values['WBC'] < 4.0:
            base_dose *= 0.9
    
    return round(base_dose, 2)
