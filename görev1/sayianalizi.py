def analiz_et(sayilar):
    # Liste boşsa hata almamak için kontrol yaptım
    if not sayilar:
        return None

    # Başlangıç değerlerini listenin ilk elemanı olarak atıyorum
    en_buyuk = sayilar[0]
    en_kucuk = sayilar[0]
    toplam = 0
    
    # Döngü ile her bir sayıyı kontrol ediyorum
    for sayi in sayilar:
        # En büyük sayıyı bulma mantığı
        if sayi > en_buyuk:
            en_buyuk = sayi
            
        # En küçük sayıyı bulma mantığı
        if sayi < en_kucuk:
            en_kucuk = sayi
            
        # Ortalama için tüm sayıları toplama
        toplam += sayi

    # Ortalama hesaplama (Toplam / Eleman Sayısı)
    ortalama = toplam / len(sayilar)

    # Sonuçları dictionary olarak döndürelim
    sonuc = {
        "Listedeki en büyük sayı": en_buyuk,
        "Listedeki en küçük sayı": en_kucuk,
        "Listedeki sayıalrın ortalaması": ortalama
    }
    
    return sonuc

# Test etmek için liste oluşturalım
liste = [10, 25, 5, 40, 15]
print(analiz_et(liste))