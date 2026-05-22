-- Mevcut veritabanını kullanıyoruz
USE TatliciOtomasyon;
GO

-- 1. KATEGORİLER TABLOSU
CREATE TABLE Kategoriler (
    KategoriID INT PRIMARY KEY IDENTITY(1,1),
    KategoriAd NVARCHAR(50) NOT NULL CONSTRAINT UQ_KategoriAd UNIQUE -- Aynı isimde kategori eklenemez
);

-- 2. URUNLER TABLOSU (Mükerrer isim sorununu UNIQUE ile çözdük)
CREATE TABLE Urunler (
    UrunID INT PRIMARY KEY IDENTITY(1,1),
    UrunAd NVARCHAR(100) NOT NULL,
    KategoriID INT NOT NULL,
    BirimFiyat DECIMAL(10,2) NOT NULL,
    StokMiktari INT DEFAULT 0  , -- DEFAULT kısıtlaması 
    CONSTRAINT FK_Urun_Kategori FOREIGN KEY (KategoriID) REFERENCES Kategoriler(KategoriID), -- FK ilişkisi 
    CONSTRAINT CHK_Stok_EksiyeDusmez CHECK (StokMiktari >= 0),
    CONSTRAINT CHK_Fiyat CHECK (BirimFiyat > 0), -- CHECK kısıtlaması (Fiyat 0 olamaz) 
    CONSTRAINT UQ_UrunAd UNIQUE (UrunAd) -- Aynı isimli tatlı tekrar eklenemez
);

-- 3. MUSTERILER TABLOSU
CREATE TABLE Musteriler (
    MusteriID INT PRIMARY KEY IDENTITY(1,1),
    Ad NVARCHAR(50) NOT NULL,
    Soyad NVARCHAR(50) NOT NULL,
    Telefon CHAR(11) NOT NULL CONSTRAINT UQ_MusteriTel UNIQUE, -- Aynı telefonla iki kayıt olmaz
    Eposta NVARCHAR(100) CONSTRAINT UQ_MusteriEposta UNIQUE
);

-- 4. CALISANLAR TABLOSU
CREATE TABLE Calisanlar (
    CalisanID INT PRIMARY KEY IDENTITY(1,1),
    AdSoyad NVARCHAR(100) NOT NULL,
    Gorev NVARCHAR(50) DEFAULT 'Tezgahtar',
    Maas DECIMAL(10,2) CONSTRAINT CHK_Maas CHECK (Maas >= 17002) 
);

-- 5. SIPARISLER TABLOSU
CREATE TABLE Siparisler (
    SiparisID INT PRIMARY KEY IDENTITY(1,1),
    MusteriID INT NOT NULL,
    CalisanID INT NOT NULL,
    SiparisTarihi DATETIME DEFAULT GETDATE(), -- DEFAULT: Sistem tarihini otomatik atar 
    ToplamTutar DECIMAL(10,2) DEFAULT 0,
    CONSTRAINT FK_Siparis_Musteri FOREIGN KEY (MusteriID) REFERENCES Musteriler(MusteriID),
    CONSTRAINT FK_Siparis_Calisan FOREIGN KEY (CalisanID) REFERENCES Calisanlar(CalisanID)
);

-- 6. SIPARIS_DETAY TABLOSU (İlişki tablosu)
CREATE TABLE SiparisDetay (
    DetayID INT PRIMARY KEY IDENTITY(1,1),
    SiparisID INT NOT NULL,
    UrunID INT NOT NULL,
    Adet INT NOT NULL CONSTRAINT CHK_Adet CHECK (Adet > 0),
    BirimFiyat DECIMAL(10,2) NOT NULL,
    CONSTRAINT FK_Detay_Siparis FOREIGN KEY (SiparisID) REFERENCES Siparisler(SiparisID),
    CONSTRAINT FK_Detay_Urun FOREIGN KEY (UrunID) REFERENCES Urunler(UrunID)
);

-- 7. ODEME_YONTEMLERI TABLOSU (6+ Tablo kuralı için ekstra )
CREATE TABLE OdemeYontemleri (
    OdemeID INT PRIMARY KEY IDENTITY(1,1),
    YontemAd NVARCHAR(30) NOT NULL UNIQUE
);
