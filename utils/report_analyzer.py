import re
from datetime import datetime

class ReportAnalyzer:
    def __init__(self):
        # Türkçe dil modeli için basit bir model kullanıyoruz
        self.important_terms = {
            'tani': ['karsinom', 'adenokarsinom', 'metastaz', 'tümör', 'nodül'],
            'boyut': ['mm', 'cm', 'boyut'],
            'lokasyon': ['sağ', 'sol', 'üst', 'alt', 'lob', 'akciğer'],
            'evre': ['evre', 'stage', 'grade'],
            'metastaz': ['metastaz', 'yayılım', 'invazyon']
        }

    def extract_measurements(self, text):
        """Metinden ölçümleri çıkarır"""
        measurement_pattern = r'(\d+(?:\.\d+)?)\s*(mm|cm|m)'
        measurements = re.findall(measurement_pattern, text.lower())
        return [{'value': float(value), 'unit': unit} for value, unit in measurements]

    def extract_important_findings(self, text):
        """Önemli bulguları çıkarır"""
        findings = {category: [] for category in self.important_terms}

        # Metni küçük harfe çevir ve satırlara böl
        lines = text.lower().split('\n')

        # Her bir satır için önemli terimleri ara
        for line in lines:
            for category, terms in self.important_terms.items():
                for term in terms:
                    if term in line:
                        # Eğer terim bulunduysa ve daha önce eklenmemişse ekle
                        if line.strip() not in findings[category]:
                            findings[category].append(line.strip())

        return findings

    def analyze_report(self, report_text):
        """Raporu analiz eder ve yapılandırılmış sonuçlar döndürür"""
        measurements = self.extract_measurements(report_text)
        findings = self.extract_important_findings(report_text)

        # Evreyi belirle
        stage = None
        for stage_text in findings['evre']:
            stage_match = re.search(r'evre\s+([IVX]+)', stage_text, re.IGNORECASE)
            if stage_match:
                stage = stage_match.group(1)
                break

        return {
            'measurements': measurements,
            'findings': findings,
            'stage': stage,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def generate_summary(self, analysis_results):
        """Analiz sonuçlarından özet oluşturur"""
        summary = []

        if analysis_results['stage']:
            summary.append(f"Evre: {analysis_results['stage']}")

        if analysis_results['measurements']:
            sizes = [f"{m['value']}{m['unit']}" for m in analysis_results['measurements']]
            summary.append(f"Tespit edilen boyutlar: {', '.join(sizes)}")

        for category, findings in analysis_results['findings'].items():
            if findings:
                summary.append(f"\n{category.title()} ile ilgili bulgular:")
                for finding in findings:
                    summary.append(f"- {finding}")

        return '\n'.join(summary)