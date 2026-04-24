import cv2
import numpy as np
import os

def detect_blood_cells(image_path, output_path):
    # 1. Görüntüyü Oku
    img = cv2.imread(image_path)
    if img is None:
        print(f"HATA: '{image_path}' bulunamadı. Lütfen dosya yolunu kontrol edin.")
        return

    output_img = img.copy()
    
    # İşlemler için görüntüyü gri tonlamaya çevir (Thresholding gri tonlamada yapılır)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # ---------------------------------------------------------
    # ADIM 1: AKYUVAR TESPİTİ (Basit / Global Thresholding)
    # ---------------------------------------------------------
    # Akyuvarlar (lökositler) içerdikleri çekirdek nedeniyle görüntüdeki en koyu nesnelerdir.
    ret, akyuvar_mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    
    # Morfolojik işlemler (Gürültü silme ve delik kapatma)
    kernel = np.ones((5,5), np.uint8)
    akyuvar_mask = cv2.morphologyEx(akyuvar_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    akyuvar_mask = cv2.dilate(akyuvar_mask, kernel, iterations=2)
    
    akyuvar_contours, _ = cv2.findContours(akyuvar_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    akyuvar_centers = []
    for cnt in akyuvar_contours:
        area = cv2.contourArea(cnt)
        if area > 800: # Akyuvarlar genellikle boyut olarak daha büyüktür
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius) + 15 # Hedef çıktıdaki gibi çemberi biraz geniş çiziyoruz
            
            # Mavi çember ve "Akyuvar" yazısı ekle
            cv2.circle(output_img, center, radius, (255, 0, 0), 2)
            cv2.putText(output_img, "Akyuvar", (center[0] - 40, center[1] - radius - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
            
            akyuvar_centers.append((center, radius))


    # ---------------------------------------------------------
    # ADIM 2: ALYUVAR TESPİTİ (Adaptive / Uyarlanabilir Thresholding)
    # ---------------------------------------------------------
    # "Neredeyse tamamını bulmak" hedefi için klasik Thresholding (Otsu vb.) yetersiz kalabilir
    # Gürültüyü azaltmak için bulanıklaştırma (Blur) uyguluyoruz
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Adaptive Thresholding
    alyuvar_mask = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY_INV, 21, 5)
    
    # Morfolojik işlemler ile pürüzleri temizleme
    kernel_alyuvar = np.ones((3,3), np.uint8)
    alyuvar_mask = cv2.morphologyEx(alyuvar_mask, cv2.MORPH_OPEN, kernel_alyuvar, iterations=1)
    
    alyuvar_contours, _ = cv2.findContours(alyuvar_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in alyuvar_contours:
        area = cv2.contourArea(cnt)
        # Alyuvarlar belirli bir boyut aralığındadır. 
        if 150 < area < 4000:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius)
            
            # Bu bulunan alyuvar, zaten tespit ettiğimiz bir akyuvarın üstüne mi geldi kontrolü
            caksiyor_mu = False
            for ak_center, ak_radius in akyuvar_centers:
                mesafe = np.sqrt((center[0] - ak_center[0])**2 + (center[1] - ak_center[1])**2)
                if mesafe < ak_radius: # Merkez, akyuvar çemberinin içindeyse çizme
                    caksiyor_mu = True
                    break
            
            if not caksiyor_mu:
                # Yeşil çember ve "Alyuvar" yazısı ekle
                cv2.circle(output_img, center, radius, (0, 255, 0), 2)
                cv2.putText(output_img, "Alyuvar", (center[0] - 25, center[1] - radius - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                
    # 3. Sonucu Kaydet
    cv2.imwrite(output_path, output_img)
    print(f"İşlem başarıyla tamamlandı. Çıktı resmi şuraya kaydedildi:\n'{output_path}'")

if __name__ == "__main__":
    # Resmin tam yolu 
    input_image = r"C:\Users\nursi\OneDrive\Masaüstü\task\kan_hucresi.png"  
    
    # Çıktının nereye kaydedileceğinin tam yolu 
    output_image = r"C:\Users\nursi\OneDrive\Masaüstü\Görevler\görev2deneme3\sonuc_hucreler.png"
    
    print("Hücre tespiti başlatılıyor...")
    
    if os.path.exists(input_image):
        detect_blood_cells(input_image, output_image)
    else:
        print(f"HATA: Resim '{input_image}' adresinde bulunamadı. Lütfen yolu kontrol edin.")
