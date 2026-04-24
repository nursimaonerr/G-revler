import cv2
import numpy as np

def empty(a):
    pass

# Trackbar'ların tutulacağı pencereyi oluşturuyoruz
cv2.namedWindow("Ayarlar")
cv2.resizeWindow("Ayarlar", 400, 650)

# Renk filtreleme (HSV) için trackbar'lar 
cv2.createTrackbar("H_Low", "Ayarlar", 0, 179, empty)
cv2.createTrackbar("H_High", "Ayarlar", 24, 179, empty)
cv2.createTrackbar("S_Low", "Ayarlar", 65, 255, empty)
cv2.createTrackbar("S_High", "Ayarlar", 255, 255, empty)
cv2.createTrackbar("V_Low", "Ayarlar", 37, 255, empty)
cv2.createTrackbar("V_High", "Ayarlar", 180, 255, empty)
    
# Görüntü işleme filtreleri için trackbar'lar
cv2.createTrackbar("Blur", "Ayarlar", 9, 50, empty)
cv2.createTrackbar("Acilma", "Ayarlar", 30, 100, empty)
cv2.createTrackbar("Min_Alan", "Ayarlar", 5257, 20000, empty)

# Para boyutlarını  belirlemek için trackbar'lar
cv2.createTrackbar("R_1TL", "Ayarlar", 95, 150, empty)
cv2.createTrackbar("R_50Kr", "Ayarlar", 91, 150, empty)
cv2.createTrackbar("R_25Kr", "Ayarlar", 76, 150, empty)
cv2.createTrackbar("R_10Kr", "Ayarlar", 72, 150, empty)
cv2.createTrackbar("R_5Kr", "Ayarlar", 67, 150, empty)
cv2.createTrackbar("R_1Kr", "Ayarlar", 60, 150, empty)
cv2.createTrackbar("R_Min", "Ayarlar", 45, 150, empty)


image_path = "coins.jpg"

while True:
    
    img = cv2.imread(image_path)
    
    if img is None:
        # Eğer resim yoksa uyarı gösteren boş bir ekran oluştur
        img = np.zeros((400, 600, 3), dtype=np.uint8)
        cv2.putText(img, "Gorsel bulunamadi!", (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, "'coins.jpg' adinda resim ekleyin.", (50, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        imgResult = img.copy()
        mask = np.zeros((400, 600), dtype=np.uint8)
    else:
        # Resim çok büyükse ekrana sığması için yeniden boyutlandır
        height, width = img.shape[:2]
        if height > 800 or width > 800:
            scale = 800 / max(height, width)
            img = cv2.resize(img, (int(width * scale), int(height * scale)))
            
        imgResult = img.copy()
        
        # Trackbar'dan anlık değerleri al
        h_min = cv2.getTrackbarPos("H_Low", "Ayarlar")
        h_max = cv2.getTrackbarPos("H_High", "Ayarlar")
        s_min = cv2.getTrackbarPos("S_Low", "Ayarlar")
        s_max = cv2.getTrackbarPos("S_High", "Ayarlar")
        v_min = cv2.getTrackbarPos("V_Low", "Ayarlar")
        v_max = cv2.getTrackbarPos("V_High", "Ayarlar")
        
        blur_val = cv2.getTrackbarPos("Blur", "Ayarlar")
        if blur_val % 2 == 0:
            blur_val += 1 # Blur değeri tek sayı olmalıdır
            
        kernel_size = cv2.getTrackbarPos("Acilma", "Ayarlar")
        if kernel_size == 0:
            kernel_size = 1
            
        min_alan = cv2.getTrackbarPos("Min_Alan", "Ayarlar")
        
        r_1tl = cv2.getTrackbarPos("R_1TL", "Ayarlar")
        r_50kr = cv2.getTrackbarPos("R_50Kr", "Ayarlar")
        r_25kr = cv2.getTrackbarPos("R_25Kr", "Ayarlar")
        r_10kr = cv2.getTrackbarPos("R_10Kr", "Ayarlar")
        r_5kr = cv2.getTrackbarPos("R_5Kr", "Ayarlar")
        r_1kr = cv2.getTrackbarPos("R_1Kr", "Ayarlar")
        r_min = cv2.getTrackbarPos("R_Min", "Ayarlar")
        
        # Görüntüyü BGR'den HSV renk uzayına çevir
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Gürültüyü azaltmak için bulanıklaştırma
        imgBlur = cv2.GaussianBlur(imgHSV, (blur_val, blur_val), 1)
        
        # Renk aralığına göre maske oluştur
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(imgBlur, lower, upper)
        
        # Morfolojik işlemler Gürültü silme ve delik doldurma
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Konturları şekilleri bul
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        total_balance = 0.0
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > min_alan:
                # Konturu çevreleyen en küçük çemberi bul
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                center = (int(x), int(y))
                radius = int(radius)
                
                # Yarıçapa göre paraları sınıflandırma yaptım
                # İki değerin ortalaması sınır kabul edilerek yapıldı
                value_text = ""
                value = 0.0
                
                if radius >= (r_1tl + r_50kr) / 2:
                    value_text = "1 TL"
                    value = 1.0
                elif radius >= (r_50kr + r_25kr) / 2:
                    value_text = "50 Kr"
                    value = 0.5
                elif radius >= (r_25kr + r_10kr) / 2:
                    value_text = "25 Kr"
                    value = 0.25
                elif radius >= (r_10kr + r_5kr) / 2:
                    value_text = "10 Kr"
                    value = 0.10
                elif radius >= (r_5kr + r_1kr) / 2:
                    value_text = "5 Kr"
                    value = 0.05
                elif radius >= r_min:
                    value_text = "1 Kr"
                    value = 0.01
                else:
                    continue # Yarıçapı r_min'den küçükse atlasın
                    
                total_balance += value
                
                # Para etrafına çember çiz ve merkezini işaretlesin
                cv2.circle(imgResult, center, radius, (0, 255, 0), 2)
                cv2.circle(imgResult, center, 2, (0, 0, 255), -1)
                
                # Yazıyı ortalamak için boyutunu hesapla ve yazdırsın
                text_size = cv2.getTextSize(value_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                text_x = center[0] - text_size[0] // 2
                text_y = center[1] + text_size[1] // 2
                cv2.putText(imgResult, value_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                
                # Hata ayıklamayı kolaylaştırmak için paranın gerçek yarıçapını (r) ekrana yazdıralım
                cv2.putText(imgResult, f"r:{radius}", (center[0] - 15, center[1] + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                
        #toplamı yaz
        cv2.putText(imgResult, f"TOTAL: {total_balance:.2f} TL", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
    # Pencereleri göster
    cv2.imshow("Maske", mask)
    cv2.imshow("Sonuc", imgResult)
    
    # 'q' tuşuna basıldığında döngüden çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cv2.destroyAllWindows()
