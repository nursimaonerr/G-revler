import cv2
import numpy as np

# --- HAZIRLIK ---
fotograf = cv2.imread('kan_hucresi.png') 
hsv_fotograf = cv2.cvtColor(fotograf, cv2.COLOR_BGR2HSV)

# ==========================================
# 1. BÖLÜM: AKYUVAR TESPİTİ (MOR RENK)
# ==========================================
koyu_mor = np.array([120, 50, 50])
acik_mor = np.array([160, 255, 255])
akyuvar_maske = cv2.inRange(hsv_fotograf, koyu_mor, acik_mor)

sinirlar_akyuvar, _ = cv2.findContours(akyuvar_maske, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for sinir in sinirlar_akyuvar:
    (x, y), yaricap = cv2.minEnclosingCircle(sinir)
    merkez = (int(x), int(y))
    # Mavi Çizgi (255, 0, 0)
    cv2.circle(fotograf, merkez, int(yaricap), (255, 0, 0), 2)

# ==========================================
# 2. BÖLÜM: ALYUVAR TESPİTİ (PEMBE/KIRMIZI RENK)
# ==========================================
koyu_pembe = np.array([160, 40, 150])
acik_pembe = np.array([180, 255, 255])
alyuvar_maske = cv2.inRange(hsv_fotograf, koyu_pembe, acik_pembe)

sinirlar_alyuvar, _ = cv2.findContours(alyuvar_maske, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for sinir in sinirlar_alyuvar:
    (x, y), yaricap = cv2.minEnclosingCircle(sinir)
    merkez = (int(x), int(y))
    # Yeşil Çizgi (0, 255, 0)
    cv2.circle(fotograf, merkez, int(yaricap), (0, 255, 0), 2)


# --- SONUÇ ---
cv2.imshow('Tum Hucreler', fotograf)
cv2.waitKey(0)