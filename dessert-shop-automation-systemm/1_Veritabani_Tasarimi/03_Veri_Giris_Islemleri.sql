USE TatliciOtomasyon;
GO

-- 1. KATEGORİLER (UNIQUE kontrolü var, aynı isimle tekrar ekleyemezsin)
INSERT INTO Kategoriler (KategoriAd) VALUES ('Şerbetli Tatlılar'), ('Sütlü Tatlılar'), ('Pastalar'), ('İçecekler');

-- 2. ÜRÜNLER (UNIQUE kontrolü var, mükerrer isim hatasını engeller)
INSERT INTO Urunler (UrunAd, KategoriID, BirimFiyat, StokMiktari) VALUES 
('Fıstıklı Baklava', 1, 450.00, 50),
('Sütlü Nuriye', 1, 380.00, 30),
('Kazandibi', 2, 120.00, 20),
('Sütlaç', 2, 110.00, 25),
('Çikolatalı Pasta', 3, 600.00, 10),
('Çay', 4, 30.00, 100),
('Türk Kahvesi', 4, 70.00, 80);

-- 3. MÜŞTERİLER
INSERT INTO Musteriler (Ad, Soyad, Telefon, Eposta) VALUES 
('Ahmet', 'Yılmaz', '05321112233', 'ahmet@mail.com'),
('Selin', 'Kaya', '05442223344', 'selin@mail.com'),
('Mert', 'Demir', '05553334455', 'mert@mail.com');

-- 4. ÇALIŞANLAR
INSERT INTO Calisanlar (AdSoyad, Gorev, Maas) VALUES 
('Eda Görpüz', 'Yönetici', 45000.00),
('Mehmet Usta', 'Baş Ustabaşı', 35000.00),
('Ayşe Kasiyer', 'Kasiyer', 19500.00);

-- 5. ÖDEME YÖNTEMLERİ
INSERT INTO OdemeYontemleri (YontemAd) VALUES ('Nakit'), ('Kredi Kartı'), ('Multinet');