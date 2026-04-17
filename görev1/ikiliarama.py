def ikili_arama(sirali_liste, hedef):
    sol = 0
    sag = len(sirali_liste) - 1 #Arama yapacağımız alanın bitiş noktasını temsil eder.
    adim_sayisi = 0
    
    # Aranacak eleman kaldığı sürece döngüye devam etsin
    while sol <= sag:
        adim_sayisi += 1
        
        # 1. Listenin tam ortasına bakıyorum
        orta = (sol + sag) // 2
        orta_deger = sirali_liste[orta]
        
        # Eğer hedefi bulduysak
        if orta_deger == hedef:
            print(f" Hedef {hedef} bulundu! (Toplam {adim_sayisi} adımda)")
            return orta
            
        # 2. Eğer ortadaki sayı hedeften küçükse, sağ yarıya odaklansın
        elif orta_deger < hedef:
            sol = orta + 1
            
        # 3. Eğer ortadaki sayı hedeften büyükse, sol yarıya odaklansın
        else:
            sag = orta - 1
            
    # 4. Sayı bulunamadıysa
    print(f" Hedef {hedef} listede yok. (Toplam {adim_sayisi} adımda bitirildi)")
    return -1

#  Test edelim

# 1'den 100'e kadar sadece çift sayılardan oluşan 50 elemanlı sıralı bir liste oluşturalım
ornek_liste = list(range(2, 102, 2)) 

print("Durum 1: Listede olan bir sayıyı arayalım (Örn: 74)")
indeks1 = ikili_arama(ornek_liste, 74)
print(f"Sonuç İndeksi: {indeks1}\n")

print("Durum 2: Listede olmayan bir sayıyı arayalım (Örn: 25)")
indeks2 = ikili_arama(ornek_liste, 25)
print(f"Sonuç İndeksi: {indeks2}")