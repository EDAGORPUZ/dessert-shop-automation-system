import pyodbc
import pandas as pd

# Veritabanı Bağlantı Ayarları
DRIVER = 'ODBC Driver 17 for SQL Server'
SERVER = r'.\SQLEXPRESS' # Veya 'localhost' veya '.\SQLEXPRESS' gibi kendi sunucu adınız
DATABASE = 'TatliciOtomasyon'

def get_connection():
    """SQL Server'a bağlantı oluşturur ve döndürür."""
    conn_str = f"DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        return None

def fetch_data(query, params=None):
    """Verilen SQL sorgusunu çalıştırıp sonucu Pandas DataFrame olarak döndürür."""
    conn = get_connection()
    if conn:
        try:
            if params:
                df = pd.read_sql(query, conn, params=params)
            else:
                df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            print(f"Sorgu hatası: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    return pd.DataFrame()

def execute_query(query, params=None):
    """Ekleme, güncelleme, silme (INSERT, UPDATE, DELETE) işlemleri için kullanılır."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return True
        except Exception as e:
            print(f"İşlem hatası: {e}")
            return False
        finally:
            conn.close()
    return False

# ----- TABLO İŞLEMLERİ -----

# Ürünler
def get_urunler():
    query = """
        SELECT U.UrunID, U.UrunAd, K.KategoriAd, U.BirimFiyat, U.StokMiktari 
        FROM Urunler U
        INNER JOIN Kategoriler K ON U.KategoriID = K.KategoriID
    """
    return fetch_data(query)

def add_urun(urun_ad, kategori_id, birim_fiyat, stok):
    query = "INSERT INTO Urunler (UrunAd, KategoriID, BirimFiyat, StokMiktari) VALUES (?, ?, ?, ?)"
    return execute_query(query, (urun_ad, kategori_id, birim_fiyat, stok))

# Kategoriler
def get_kategoriler():
    return fetch_data("SELECT * FROM Kategoriler")

# Müşteriler
def get_musteriler():
    return fetch_data("SELECT * FROM Musteriler")

def add_musteri(ad, soyad, telefon, eposta):
    query = "INSERT INTO Musteriler (Ad, Soyad, Telefon, Eposta) VALUES (?, ?, ?, ?)"
    return execute_query(query, (ad, soyad, telefon, eposta))

def add_musteri_get_id(ad, soyad, telefon, eposta=None):
    """Müşteri ekler ve oluşturulan MüşteriID'yi döndürür."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Musteriler (Ad, Soyad, Telefon, Eposta) OUTPUT Inserted.MusteriID VALUES (?, ?, ?, ?)"
            cursor.execute(query, (ad, soyad, telefon, eposta))
            m_id = cursor.fetchone()[0]
            conn.commit()
            return int(m_id)
        except Exception as e:
            print(f"Müşteri ekleme hatası: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    return None

# Siparişler
def get_siparisler():
    query = """
        SELECT S.SiparisID, M.Ad + ' ' + M.Soyad AS Musteri, C.AdSoyad AS Calisan, S.SiparisTarihi, S.ToplamTutar
        FROM Siparisler S
        INNER JOIN Musteriler M ON S.MusteriID = M.MusteriID
        INNER JOIN Calisanlar C ON S.CalisanID = C.CalisanID
        ORDER BY S.SiparisTarihi DESC
    """
    return fetch_data(query)

# Çalışanlar
def get_calisanlar():
    return fetch_data("SELECT * FROM Calisanlar")

# ----- YENİ SİPARİŞ İŞLEMLERİ -----

def add_siparis_with_details(musteri_id, calisan_id, toplam_tutar, sepet):
    """
    Siparişi ve detaylarını veritabanına ekler. (Trigger stoğu otomatik düşer).
    sepet listesi formatı: [{'urun_id': 1, 'adet': 2, 'fiyat': 150.0}, ...]
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # 1. Siparişi oluştur ve oluşan ID'yi al
            query_siparis = "INSERT INTO Siparisler (MusteriID, CalisanID, ToplamTutar) OUTPUT Inserted.SiparisID VALUES (?, ?, ?)"
            cursor.execute(query_siparis, (musteri_id, calisan_id, toplam_tutar))
            siparis_id = cursor.fetchone()[0]
            
            # 2. Sipariş detaylarını ekle
            query_detay = "INSERT INTO SiparisDetay (SiparisID, UrunID, Adet, BirimFiyat) VALUES (?, ?, ?, ?)"
            for item in sepet:
                cursor.execute(query_detay, (siparis_id, item['urun_id'], item['adet'], item['fiyat']))
                
            conn.commit()
            return True
        except Exception as e:
            print(f"Sipariş ekleme hatası: {e}")
            conn.rollback() # Hata durumunda işlemi geri al
            return False
        finally:
            conn.close()
    return False

def get_siparis_detaylari(siparis_id):
    query = """
        SELECT U.UrunAd AS [Ürün], SD.Adet, SD.BirimFiyat AS [Birim Fiyat], (SD.Adet * SD.BirimFiyat) AS [Toplam]
        FROM SiparisDetay SD
        INNER JOIN Urunler U ON SD.UrunID = U.UrunID
        WHERE SD.SiparisID = ?
    """
    return fetch_data(query, (siparis_id,))

# ----- 6 ADET RAPOR / SORGULAR -----

# 1. vw_UrunListesiWithKategori
def get_vw_urun_listesi_kategori():
    return fetch_data("SELECT * FROM vw_UrunListesiWithKategori")

# 2. sp_KategoriyeGoreUrunler
def get_urunler_by_kategori(kategori_adi):
    query = "EXEC sp_KategoriyeGoreUrunler @KategoriAdi=?"
    return fetch_data(query, (kategori_adi,))

# 3. vw_KritikStokTakibi
def get_kritik_stok():
    return fetch_data("SELECT * FROM vw_KritikStokTakibi")

# 4. vw_EnCokSatanUrunler
def get_encok_satan():
    return fetch_data("SELECT * FROM vw_EnCokSatanUrunler")

# 5. vw_GunlukCiroRaporu
def get_gunluk_ciro():
    return fetch_data("SELECT * FROM vw_GunlukCiroRaporu")

# 6. sp_MusteriSatisGecmisi
def get_musteri_satis_gecmisi(telefon):
    return fetch_data("EXEC sp_MusteriSatisGecmisi @Telefon=?", (telefon,))

