import random

class Müşteri:
    def __init__(self, id, talep):
        self.id = id  
        self.talep = talep  

class Temsilci:
    def __init__(self, id, yetenekler, kazanç, kapasite=50):
        self.id = id  
        self.yetenekler = yetenekler  
        self.kazanç = kazanç  
        self.kapasite = kapasite  
        self.mevcut_yük = 0  

    
    def uygun_mu(self, müşteri):
        return müşteri.talep in self.yetenekler  

    
    def kabul_edebilir_mi(self):
        return self.mevcut_yük < self.kapasite  

    
    def müşteri_atama(self):
        if self.kabul_edebilir_mi():
            self.mevcut_yük += 1  
            return True
        return False  


def temsilcileri_yönlendir(müşteriler, temsilciler):
    toplam_kazanç = 0  
    atamalar = []  

    
    for müşteri in müşteriler:
        
        uygun_temsilciler = sorted(
            [temsilci for temsilci in temsilciler if temsilci.uygun_mu(müşteri) and temsilci.kabul_edebilir_mi()],
            key=lambda r: r.mevcut_yük  
        )
        
        if uygun_temsilciler:
            seçilen_rep = uygun_temsilciler[0]  
            if seçilen_rep.müşteri_atama():  
                atamalar.append((müşteri.id, müşteri.talep, seçilen_rep.id, seçilen_rep.yetenekler, seçilen_rep.kazanç))
                toplam_kazanç += seçilen_rep.kazanç  

    return toplam_kazanç, atamalar  

class Kampanya:
    def __init__(self, id, maliyet, roi):
        self.id = id  
        self.maliyet = maliyet  
        self.roi = roi  


def pazarlama_kampanyalarını_seç(kampanyalar, bütçe):
    n = len(kampanyalar) 
    dp = [0] * (bütçe + 1)  
    seçilen_kampanyalar = [[] for _ in range(bütçe + 1)]  
    yatırım_maliyetleri = [0] * (bütçe + 1)  

    for i in range(n):
        rastgele_roi = kampanyalar[i].roi * random.uniform(0.5, 1.5)  
        for b in range(bütçe, kampanyalar[i].maliyet - 1, -1):  
            if dp[b] < dp[b - kampanyalar[i].maliyet] + rastgele_roi:  
                dp[b] = dp[b - kampanyalar[i].maliyet] + rastgele_roi  
                seçilen_kampanyalar[b] = seçilen_kampanyalar[b - kampanyalar[i].maliyet] + [kampanyalar[i]]  
                yatırım_maliyetleri[b] = yatırım_maliyetleri[b - kampanyalar[i].maliyet] + kampanyalar[i].maliyet  

    
    toplam_kazanç = dp[bütçe]  
    toplam_yatırım = yatırım_maliyetleri[bütçe]  
    roi = (toplam_kazanç - toplam_yatırım) / toplam_yatırım * 100 if toplam_yatırım > 0 else 0  

    return roi, seçilen_kampanyalar[bütçe], toplam_yatırım, toplam_kazanç  


def main():
    
    müşteriler = [
        Müşteri(1, 'teknik'),
        Müşteri(2, 'faturalama'),
        Müşteri(3, 'teknik'),
        Müşteri(4, 'müşteri_hizmetleri'),
        Müşteri(5, 'faturalama'),
        Müşteri(6, 'teknik'),
        Müşteri(7, 'faturalama'),
        Müşteri(8, 'müşteri_hizmetleri'),
        Müşteri(9, 'teknik'),
        Müşteri(10, 'faturalama')
    ]
    
    temsilciler = [
        Temsilci(1, ['teknik'], 10),
        Temsilci(2, ['faturalama'], 5),
        Temsilci(3, ['teknik', 'faturalama'], 15),
        Temsilci(4, ['müşteri_hizmetleri'], 8)
    ]

    
    toplam_kazanç, atamalar = temsilcileri_yönlendir(müşteriler, temsilciler)
    print("\nMüşteri Destek Temsilcisi Yönlendirme:")
    print("---------------------------------------------------")
    print("| Müşteri ID | Talep Türü          | Temsilci ID | Kazanç |")
    print("---------------------------------------------------")
    for müşteri_id, talep, rep_id, yetenekler, kazanç in atamalar:
        print(f"| {müşteri_id:^10} | {talep:^18} | {rep_id:^11} | {kazanç:^6} |")
    print("---------------------------------------------------")
    print(f" Toplam Kazanç:  {toplam_kazanç}\n")

    kampanyalar = [
        Kampanya(1, 50, 100),
        Kampanya(2, 30, 60),
        Kampanya(3, 20, 40),
        Kampanya(4, 70, 120),
        Kampanya(5, 10, 30)
    ]
    bütçe = 100

    roi, seçilen_kampanyalar, toplam_yatırım, toplam_kazanç = pazarlama_kampanyalarını_seç(kampanyalar, bütçe)
    print(" Pazarlama Kampanyası Seçimi:")
    print("---------------------------------------------------")
    print(f" Bütçe: {bütçe}")
    print(f" Maksimum ROI: {roi:.2f}%")
    print(" Seçilen Kampanyalar:")
    for kampanya in seçilen_kampanyalar:
        print(f"  - Kampanya {kampanya.id} → Maliyet: {kampanya.maliyet}, Beklenen Getiri: {kampanya.roi}")
    print("---------------------------------------------------")
    print(f" Toplam Harcama: {toplam_yatırım}")
    print(f" Toplam Getiri: {toplam_kazanç}\n")

if __name__ == "__main__":
    main()


# Zaman Karmaşıklığı ve Yer Karmaşıklığı Hesaplamaları:

# 1. Temsilcileri Yönlendir (temsilcileri_yönlendir fonksiyonu):
# - Her müşteri için uygun temsilciler filtreleniyor ve sıralanıyor.
# - Filtreleme: O(r) -> Her temsilci için 'uygun_mu' ve 'kabul_edebilir_mi' fonksiyonları çalıştırılır.
# - Sıralama: O(r log r) -> Her müşteri için temsilciler sıralanır.
# - Toplam Zaman Karmaşıklığı: O(n * r log r) -> n müşteri var ve her müşteri için r temsilci işlenir.

# - Yer Karmaşıklığı: O(r) -> Geçici bir liste olan 'uygun_temsilciler' kullanılır.

# 2. Pazarlama Kampanyası Seçimi (pazarlama_kampanyalarını_seç fonksiyonu):
# - Dinamik programlama tablosu 'dp' güncelleniyor.
# - Her kampanya için, her bütçe aralığına kadar güncelleme yapılıyor.
# - Toplam Zaman Karmaşıklığı: O(n * B) -> n kampanya var ve her biri için bütçe aralığında işlem yapılıyor.

# - Yer Karmaşıklığı: O(B) -> Dinamik programlama tablosu ve yardımcı listeler ile yer kullanımı.
