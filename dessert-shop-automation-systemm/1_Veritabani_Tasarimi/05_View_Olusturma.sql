USE TatliciOtomasyon;
GO

-- Rapor: Ürünlerin hangi kategoride olduğunu gösteren JOIN'li View

CREATE VIEW vw_UrunListesiWithKategori AS
SELECT 
    U.UrunID,
    U.UrunAd AS [Ürün Adı],
    K.KategoriAd AS [Kategori],
    U.BirimFiyat AS [Fiyat],
    U.StokMiktari AS [Stok]
FROM Urunler U
--Bu komut, Urunler ve Kategoriler tablolarını ortak olan KategoriID sütunu üzerinden birbirine bağlar.
INNER JOIN Kategoriler K ON U.KategoriID = K.KategoriID;