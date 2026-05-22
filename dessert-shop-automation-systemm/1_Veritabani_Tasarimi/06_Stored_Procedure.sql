USE TatliciOtomasyon;
GO

-- Kategoriye göre ürün getiren parametreli prosedür

CREATE PROCEDURE sp_KategoriyeGoreUrunler
    @KategoriAdi NVARCHAR(50)
AS
BEGIN
    SELECT 
        U.UrunAd, 
        U.BirimFiyat, 
        U.StokMiktari 
    FROM Urunler U
    INNER JOIN Kategoriler K ON U.KategoriID = K.KategoriID
    WHERE K.KategoriAd = @KategoriAdi;
END;
GO
