USE TatliciOtomasyon;
GO

-- Satış yapıldığında stoktan otomatik düşen Trigger
-- Rubrikteki 'DML sonrası otomatik devreye giren' şartını karşılar.
CREATE TRIGGER trg_StokDusur
ON SiparisDetay
AFTER INSERT
AS
BEGIN
    UPDATE Urunler
    SET StokMiktari = StokMiktari - inserted.Adet
    FROM Urunler
    INNER JOIN inserted ON Urunler.UrunID = inserted.UrunID;
END;
GO

