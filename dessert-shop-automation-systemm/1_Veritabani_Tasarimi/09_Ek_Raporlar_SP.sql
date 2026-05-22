USE TatliciOtomasyon;
GO

-- RAPOR 6: MÜŞTERİ SİPARİŞ GEÇMİŞİ SORGULAMA
-- Parametre olarak Telefon numarası alır ve müşterinin tüm alımlarını getirir.
CREATE PROCEDURE sp_MusteriSatisGecmisi
    @Telefon CHAR(11)
AS
BEGIN
    SELECT 
        M.Ad + ' ' + M.Soyad AS [Müşteri],
        S.SiparisTarihi AS [Tarih],
        U.UrunAd AS [Alınan Ürün],
        SD.Adet AS [Adet],
        SD.BirimFiyat AS [Birim Fiyat]
    FROM Musteriler M
    INNER JOIN Siparisler S ON M.MusteriID = S.MusteriID
    INNER JOIN SiparisDetay SD ON S.SiparisID = SD.SiparisID
    INNER JOIN Urunler U ON SD.UrunID = U.UrunID
    WHERE M.Telefon = @Telefon;
END;
GO