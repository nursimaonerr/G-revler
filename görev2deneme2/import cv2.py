"Hocam merhaba, renk uzayı (HSV) ve kontur tespiti yöntemleriyle hücreleri filtreledim. "
"Akyuvarların mor çekirdekleri belirgin olduğu için mavi çemberlerle net bir şekilde izole edilebildi."
" Ancak alyuvarlar birbirine temas ettiği ve renkleri arka planla daha iç içe olduğunu fark ettim bunun için destek aldım"
"alttaki iki yöntem bunu çözmek içindir"
" basit eşikleme (thresholding) yöntemiyle bazıları bitişik algılandı."
" Gürültüleri alan hesaplamasıyla (contourArea) temizledim."


import cv2
import numpy as np

fotograf = cv2.imread('kan_hucresi.png')
hsv_fotograf = cv2.cvtColor(fotograf, cv2.COLOR_BGR2HSV)

koyu_mor = np.array([120, 50, 50])
acik_mor = np.array([160, 255, 255])
akyuvar_maske = cv2.inRange(hsv_fotograf, koyu_mor, acik_mor)

sinirlar_akyuvar, _ = cv2.findContours(akyuvar_maske, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for sinir in sinirlar_akyuvar:
    alan = cv2.contourArea(sinir)
    if alan > 500:
        (x, y), yaricap = cv2.minEnclosingCircle(sinir)
        merkez = (int(x), int(y))
        cv2.circle(fotograf, merkez, int(yaricap), (255, 0, 0), 2)
        cv2.putText(fotograf, 'Akyuvar', (merkez[0]-35, merkez[1]-int(yaricap)-5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

koyu_pembe = np.array([160, 40, 150])
acik_pembe = np.array([180, 255, 255])
alyuvar_maske = cv2.inRange(hsv_fotograf, koyu_pembe, acik_pembe)

sinirlar_alyuvar, _ = cv2.findContours(alyuvar_maske, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for sinir in sinirlar_alyuvar:
    alan = cv2.contourArea(sinir)
    if alan > 100 and alan < 2000:
        (x, y), yaricap = cv2.minEnclosingCircle(sinir)
        merkez = (int(x), int(y))
        cv2.circle(fotograf, merkez, int(yaricap), (0, 255, 0), 2)

cv2.imshow('Filtrelenmis Hucre Tespiti', fotograf)
cv2.waitKey(0)
cv2.destroyAllWindows()