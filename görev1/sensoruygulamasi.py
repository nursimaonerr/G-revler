'''
Sensör sınıfı oluşturuyoruz.
'''
class Sensor:
    def __init__(self, sensor_adi):
        self.sensor_adi = sensor_adi
        self.okunan_deger = 0  # başlangıç değerine sıfır atadık

    def deger_guncelle(self, yeni_deger):# Sensörün okuduğu değeri güncelleyen method
        self.okunan_deger = yeni_deger

    def kontrol_et(self):               
                                       
        if self.okunan_deger < 10:
            return f"{self.sensor_adi}: Engel algılandı!"  #Eğer mesafe 10 cm'den küçükse "Engel algılandı!",
        else:
            return f"{self.sensor_adi}: Yol açık."          #değilse "Yol açık." mesajı döndürsün.


# Listeyi kontrol eden fonksiyon
def sensorleri_kontrol_et(sensor_listesi):
    sonuc_listesi = []

    for sensor in sensor_listesi:
        sonuc_listesi.append(sensor.kontrol_et()) 

    return sonuc_listesi



# Sensörler için 4 değişken (on, arka, sag, sol) oluşturdum
on = Sensor("Ön Sensör")
arka = Sensor("Arka Sensör")
sag = Sensor("Sağ Sensör")
sol = Sensor("Sol Sensör")

# Kullanıcıdan float tipinde mesafe verisi aldım.
on_deger = float(input("Ön sensör mesafesi (cm): "))
arka_deger = float(input("Arka sensör mesafesi (cm): "))
sag_deger = float(input("Sağ sensör mesafesi (cm): "))
sol_deger = float(input("Sol sensör mesafesi (cm): "))

# Değerleri güncelledim
on.deger_guncelle(on_deger)
arka.deger_guncelle(arka_deger)
sag.deger_guncelle(sag_deger)
sol.deger_guncelle(sol_deger)

# Sensörler için lste oluşturum.
sensorler = [on, arka, sag, sol]

# Sensörleri kontrol edip sonuclar' a atadım
sonuclar = sensorleri_kontrol_et(sensorler)

# Sonuçları yazdırdım
print("\n--- SONUÇLAR ---")
for sonuc in sonuclar:
    print(sonuc)