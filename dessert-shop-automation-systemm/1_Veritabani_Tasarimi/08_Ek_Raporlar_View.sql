USE TatliciOtomasyon;
GO

-- RAPOR 3: KRİTİK STOK RAPORU
-- Stok miktarı 15'in altına düşen ürünleri gösterir (İşletme yönetimi için kritik).
CREATE VIEW vw_KritikStokTakibi AS
SELECT 
    UrunAd AS [Ürün],
    StokMiktari AS [Kalan Stok],
    'STOK AZALIYOR!' AS [Durum]
FROM Urunler
WHERE StokMiktari < 15;
GO

-- RAPOR 4: EN ÇOK SATAN ÜRÜNLER (TOP 5)
-- Hangi tatlıların daha popüler olduğunu analiz eder.
CREATE VIEW vw_EnCokSatanUrunler AS
SELECT TOP 5
    U.UrunAd AS [Ürün],
    SUM(SD.Adet) AS [Toplam Satış Adedi]
FROM SiparisDetay SD
INNER JOIN Urunler U ON SD.UrunID = U.UrunID
GROUP BY U.UrunAd
ORDER BY [Toplam Satış Adedi] DESC;
GO

-- RAPOR 5: GÜNLÜK KAZANÇ ÖZETİ (CİRO)
-- Bugün yapılan toplam satışı ve net kazancı gösterir.
CREATE VIEW vw_GunlukCiroRaporu AS
SELECT 
    CAST(S.SiparisTarihi AS DATE) AS [Tarih],
    COUNT(S.SiparisID) AS [Toplam Sipariş],
    SUM(SD.Adet * SD.BirimFiyat) AS [Toplam Ciro]
FROM Siparisler S
INNER JOIN SiparisDetay SD ON S.SiparisID = SD.SiparisID
GROUP BY CAST(S.SiparisTarihi AS DATE);
GO