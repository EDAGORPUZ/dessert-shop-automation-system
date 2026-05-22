USE TatliciOtomasyon;
GO

-- 1. GÜNCELLEME (UPDATE) DEMOSU
PRINT '--- GUNCELLEME ONCESI DURUM ---';
SELECT UrunID, UrunAd, BirimFiyat FROM Urunler WHERE UrunAd = 'Fıstıklı Baklava';

-- Fiyatı güncelliyoruz
UPDATE Urunler 
SET BirimFiyat = 500.00 
WHERE UrunAd = 'Fıstıklı Baklava';

PRINT '--- GUNCELLEME SONRASI DURUM ---';
SELECT UrunID, UrunAd, BirimFiyat FROM Urunler WHERE UrunAd = 'Fıstıklı Baklava';


-- 2. SILME (DELETE) DEMOSU
INSERT INTO Urunler (UrunAd, KategoriID, BirimFiyat, StokMiktari) 
VALUES ('Tiramisu', 1, 10.00, 100);

-- Ürünün eklendiğini ispatlayalım [cite: 80]
SELECT * FROM Urunler WHERE UrunAd = 'Tiramisu';

DELETE FROM Urunler 
WHERE UrunAd = 'Tiramisu';

-- Ürünün silindiğini (tablonun boş döneceğini) ispatlayalım 
SELECT * FROM Urunler WHERE UrunAd = 'Tiramisu';