import pandas as pd
import numpy as np

def analyze_blood_values(blood_data):
    """
    Kan değerlerini analiz eder ve anormallikleri tespit eder
    """
    reference_ranges = {
        # Tam Kan Sayımı
        'WBC': (4.5, 11.0),  # Beyaz kan hücresi (×10^9/L)
        'RBC': (4.5, 5.5),   # Kırmızı kan hücresi (×10^12/L)
        'HGB': (13.5, 17.5), # Hemoglobin (g/dL)
        'PLT': (150, 450),   # Trombosit (×10^9/L)

        # Tümör Belirteçleri
        'CEA': (0, 5.0),     # Karsinoembriyonik antijen (ng/mL)
        'CYFRA': (0, 3.3),   # CYFRA 21-1 (ng/mL)
        'NSE': (0, 16.3),    # Nöron spesifik enolaz (ng/mL)

        # Biyokimya
        'LDH': (140, 280),   # Laktat dehidrogenaz (U/L)
        'ALP': (44, 147)     # Alkalen fosfataz (U/L)
    }

    results = {}
    risk_score = 0

    for param, (min_val, max_val) in reference_ranges.items():
        if param in blood_data:
            value = blood_data[param]
            status = 'Normal'
            risk = 0

            if value < min_val:
                status = 'Düşük'
                risk = 1
            elif value > max_val:
                status = 'Yüksek'
                risk = 2 if param in ['CEA', 'CYFRA', 'NSE'] else 1

            results[param] = {
                'value': value,
                'status': status,
                'reference_range': f'{min_val}-{max_val}',
                'risk_level': risk
            }
            risk_score += risk

    return {
        'test_results': results,
        'risk_score': min(risk_score / len(blood_data) * 5, 10)  # 0-10 arası risk skoru
    }

def analyze_pathology_report(report_data):
    """
    Patoloji raporunu analiz eder
    """
    cancer_types = {
        'NSCLC': ['Adenokarsinom', 'Skuamöz hücreli karsinom', 'Büyük hücreli karsinom'],
        'SCLC': ['Küçük hücreli karsinom']
    }

    results = {
        'cancer_type': None,
        'histology': None,
        'stage': None,
        'differentiation': None,
        'risk_level': 0
    }

    if 'histology' in report_data:
        results['histology'] = report_data['histology']
        for type_group, subtypes in cancer_types.items():
            if report_data['histology'] in subtypes:
                results['cancer_type'] = type_group

    if 'stage' in report_data:
        results['stage'] = report_data['stage']
        # Risk seviyesi hesaplama (Stage I: 2, II: 4, III: 6, IV: 8)
        stage_num = roman_to_int(report_data['stage'].split()[1])
        results['risk_level'] = stage_num * 2

    if 'differentiation' in report_data:
        results['differentiation'] = report_data['differentiation']

    return results

def roman_to_int(roman):
    """
    Roma rakamını integer'a çevirir
    """
    roman_values = {'I': 1, 'II': 2, 'III': 3, 'IV': 4}
    return roman_values.get(roman, 0)

def calculate_treatment_dose(weight, age, blood_values=None, pathology_results=None):
    """
    Tedavi dozunu hesaplar
    """
    base_dose = weight * 2  # mg/kg başlangıç dozu

    # Yaşa göre düzeltme
    if age > 65:
        base_dose *= 0.8

    # Kan değerlerine göre düzeltme
    if blood_values:
        if blood_values.get('WBC', 100) < 4.0:
            base_dose *= 0.9
        if blood_values.get('PLT', 400) < 100:
            base_dose *= 0.85

    # Patoloji sonuçlarına göre düzeltme
    if pathology_results and 'stage' in pathology_results:
        stage_multiplier = {
            'I': 1.0,
            'II': 1.1,
            'III': 1.2,
            'IV': 1.3
        }
        stage = pathology_results['stage'].split()[1]
        base_dose *= stage_multiplier.get(stage, 1.0)

    return round(base_dose, 2)