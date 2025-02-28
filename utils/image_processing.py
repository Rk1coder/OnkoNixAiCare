import cv2
import numpy as np

def preprocess_image(image):
    """
    Bronkoskopi görüntülerini ön işlemden geçirir
    """
    # Görüntüyü gri tonlamaya çevir
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Gürültü azaltma
    denoised = cv2.GaussianBlur(gray, (5,5), 0)
    
    # Kontrast artırma
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)
    
    return enhanced

def detect_anomalies(image):
    """
    Görüntüdeki anormallikleri tespit eder
    """
    # Demo amaçlı basit bir eşikleme
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    
    # Konturları bul
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Anormallik skoru (demo amaçlı)
    anomaly_score = len(contours) / 100.0
    
    return min(anomaly_score, 1.0)
