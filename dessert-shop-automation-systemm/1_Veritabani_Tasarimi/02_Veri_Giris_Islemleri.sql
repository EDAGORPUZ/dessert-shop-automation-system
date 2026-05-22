USE TatliciOtomasyon;
GO

-- 1. KATEGORİLERİ EKLEYELİM
INSERT INTO Kategoriler (KategoriAd) VALUES ('Şerbetli Tatlılar');
INSERT INTO Kategoriler (KategoriAd) VALUES ('Sütlü Tatlılar');
INSERT INTO Kategoriler (KategoriAd) VALUES ('Pastalar');
INSERT INTO Kategoriler (KategoriAd) VALUES ('İçecekler');

-- 2. ÜRÜNLERİ EKLEYELİM (UNIQUE kısıtlaması sayesinde aynı isimli ürün eklenemez)
INSERT INTO Urunler (UrunAd, KategoriID, BirimFiyat, StokMiktari) VALUES 
('Fıstıklı Baklava', 1, 450.00, 50),
('Sütlü Nuriye', 1, 380.00, 30),
('Kazandibi', 2, 120.00, 20),
('Sütlaç', 2, 110.00, 25),
('Çikolatalı Pasta', 3, 600.00, 10),
('Çay', 4, 30.00, 100),
('Türk Kahvesi', 4, 70.00, 80);

-- 3. ÖRNEK MÜŞTERİLER
INSERT INTO Musteriler (Ad, Soyad, Telefon, Eposta) VALUES 
('Ahmet', 'Yılmaz', '05321112233', 'ahmet@mail.com'),
('Selin', 'Kaya', '05442223344', 'selin@mail.com'),
('Mert', 'Demir', '05553334455', 'mert@mail.com');

-- 4. ÇALIŞANLAR (Asgari ücret kontrolü CHECK kısıtlaması devrede)
INSERT INTO Calisanlar (AdSoyad, Gorev, Maas) VALUES 
('Eda Görpüz', 'Yönetici', 45000.00),
('Mehmet Usta', 'Baş Ustabaşı', 35000.00),
('Ayşe Yılmaz', 'Kasiyer', 18500.00);

-- 5. ÖDEME YÖNTEMLERİ
INSERT INTO OdemeYontemleri (YontemAd) VALUES ('Nakit'), ('Kredi Kartı'), ('Multinet');