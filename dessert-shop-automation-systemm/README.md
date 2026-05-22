# 🍰 Tatlıcı Otomasyon Sistemi

Bu proje, bir tatlıcı/pastane işletmesinin günlük operasyonlarını (ürün, müşteri, çalışan ve sipariş yönetimi) kolayca yönetebilmek amacıyla geliştirilmiş **ilişkisel bir veritabanı tasarımı** ve bu veritabanına bağlı çalışan modern bir **kullanıcı arayüzü (Streamlit Dashboard)** uygulamasıdır. 

Proje, **Veritabanı Yönetim Sistemleri (VTYS)** dersi kapsamında geliştirilmiştir ve ilişkisel veritabanı kuralları, kısıtlamalar (constraints), görünümler (views), tetikleyiciler (triggers) ile saklı yordamları (stored procedures) içermektedir.

---

## 🚀 Proje Yapısı

Proje dosyaları mantıksal bir sırayla aşağıdaki şekilde düzenlenmiştir:

```text
VTYS_ÖDEV/
│
├── 1_Veritabani_Tasarimi/     # SQL Tablo Tanımlamaları ve İlişkisel Şema
│   ├── 00_DB_Olusturma.sql    # Veritabanının oluşturulması (Create DB)
│   ├── 01_Tablo_Olusturma.sql # Tablolar, birincil/yabancı anahtarlar ve kısıtlamalar
│   ├── 02_Veri_Giris_Islemleri.sql  # Örnek başlangıç verileri (Kategori, Ürün, Müşteri, Çalışan)
│   ├── 03_Veri_Giris_Islemleri.sql  # Ek sipariş ve detay örnek verileri
│   ├── 04_DML_Guncelleme_Silme.sql   # Örnek DML güncelleme ve silme sorguları
│   ├── 05_View_Olusturma.sql  # Ürün-kategori JOIN görünümü
│   ├── 06_Stored_Procedure.sql # Kategori bazlı filtreleme prosedürü
│   ├── 07_Trigger_Olusturma.sql # Stok kontrolü yapan DML tetikleyicisi
│   ├── 08_Ek_Raporlar_View.sql # Kritik stok, En çok satanlar ve Ciro görünümleri
│   ├── 09_Ek_Raporlar_SP.sql   # Müşteri satın alım geçmişi prosedürü
│   └── Diyagramlar.png        # Veritabanı E-R İlişki Diyagramı
│
├── 2_Veritabani_Yedegi/       # Veritabanı Yedeği (.BAK)
│   └── Tatlici_Yedek.bak      # Microsoft SQL Server Yedek Dosyası
│
├── 3_Arayuz_Uygulamasi/       # Python Streamlit Web Arayüzü
│   ├── app.py                 # Streamlit arayüz uygulamasının ana kodu
│   ├── db_functions.py        # SQL Server bağlantı ve sorgu fonksiyonları
│   └── requirements.txt       # Gerekli kütüphaneler listesi
│
├── baslat.bat                 # Windows için tek tıkla arayüzü başlatan betik
└── README.md                  # Proje açıklama dokümanı (Bu dosya)
```

---

## 🛠️ Kullanılan Teknolojiler

* **Veritabanı Yönetim Sistemi:** Microsoft SQL Server (MSSQL)
* **Kullanıcı Arayüzü:** Python & Streamlit Framework
* **Veri Analizi:** Pandas
* **Veritabanı Bağlantısı:** PyODBC (ODBC Driver 17 for SQL Server)
* **Tasarım/Stil:** Streamlit entegre CSS ve Metric modülleri

---

## 📊 Veritabanı Tasarımı ve Tablo Yapısı

Veritabanında veri bütünlüğünü ve ilişkisel kuralları korumak adına **PRIMARY KEY**, **FOREIGN KEY**, **UNIQUE**, **DEFAULT** ve **CHECK** kısıtlamaları (constraints) aktif olarak kullanılmıştır.

### 🔑 Tablolar ve İlişkiler

1. **`Kategoriler`**: Tatlıların ve içeceklerin kategorilerini tutar. (Örn: Şerbetli Tatlılar, Sütlü Tatlılar, Pastalar, İçecekler)
   * `KategoriID` (PK, Identity)
   * `KategoriAd` (NVARCHAR, NOT NULL, UNIQUE)
2. **`Urunler`**: Satışta olan tatlı ve içeceklerin bilgilerini tutar.
   * `UrunID` (PK, Identity)
   * `UrunAd` (NVARCHAR, NOT NULL, UNIQUE)
   * `KategoriID` (FK) -> `Kategoriler(KategoriID)`
   * `BirimFiyat` (DECIMAL, CHECK: `BirimFiyat > 0`)
   * `StokMiktari` (INT, DEFAULT: 0, CHECK: `StokMiktari >= 0`)
3. **`Musteriler`**: Sipariş veren müşterilerin temel bilgilerini tutar.
   * `MusteriID` (PK, Identity)
   * `Ad` (NVARCHAR, NOT NULL), `Soyad` (NVARCHAR, NOT NULL)
   * `Telefon` (CHAR(11), NOT NULL, UNIQUE)
   * `Eposta` (NVARCHAR, UNIQUE)
4. **`Calisanlar`**: Siparişi alan/satışı gerçekleştiren personelleri tutar.
   * `CalisanID` (PK, Identity)
   * `AdSoyad` (NVARCHAR, NOT NULL)
   * `Gorev` (NVARCHAR, DEFAULT: 'Tezgahtar')
   * `Maas` (DECIMAL, CHECK: `Maas >= 17002` - Asgari Ücret Sınırı)
5. **`Siparisler`**: Her bir siparişin genel bilgilerini tutar.
   * `SiparisID` (PK, Identity)
   * `MusteriID` (FK) -> `Musteriler(MusteriID)`
   * `CalisanID` (FK) -> `Calisanlar(CalisanID)`
   * `SiparisTarihi` (DATETIME, DEFAULT: `GETDATE()`)
   * `ToplamTutar` (DECIMAL, DEFAULT: 0)
6. **`SiparisDetay`**: Siparişlerin içerisinde hangi üründen kaç adet alındığını gösteren ara/ilişki tablosudur.
   * `DetayID` (PK, Identity)
   * `SiparisID` (FK) -> `Siparisler(SiparisID)`
   * `UrunID` (FK) -> `Urunler(UrunID)`
   * `Adet` (INT, CHECK: `Adet > 0`)
   * `BirimFiyat` (DECIMAL, NOT NULL)
7. **`OdemeYontemleri`**: Desteklenen ödeme kanallarını tutar.
   * `OdemeID` (PK, Identity)
   * `YontemAd` (NVARCHAR, UNIQUE)

---

## ⚡ Gelişmiş Veritabanı Mantığı (Views, Triggers, SPs)

### 📌 Tetikleyiciler (Triggers)
* **`trg_StokDusur` (AFTER INSERT ON `SiparisDetay`)**: Sipariş başarıyla onaylandığında, sipariş edilen ürün miktarı kadar `Urunler` tablosundaki `StokMiktari` sütununu otomatik olarak düşürür. Bu sayede manuel stok güncelleme gereksinimi ortadan kalkar ve stokların eksiye düşmesi veritabanı düzeyinde engellenir.

### 📌 Görünümler (Views / Raporlar)
* **`vw_UrunListesiWithKategori`**: Ürünleri bağlı oldukları kategorilerin isimleriyle birlikte listeler.
* **`vw_KritikStokTakibi`**: Stok miktarı **15'in altına düşen** ürünleri tespit eder ve yönetim paneline uyarı bildirir.
* **`vw_EnCokSatanUrunler`**: En çok satılan ilk 5 ürünü ve toplam satış adetlerini getirerek bar grafik oluşturulmasına olanak tanır.
* **`vw_GunlukCiroRaporu`**: Gün bazında toplam sipariş sayısını ve elde edilen ciroyu hesaplar.

### 📌 Saklı Yordamlar (Stored Procedures)
* **`sp_KategoriyeGoreUrunler`**: Parametre olarak aldığı kategori ismine göre o kategorideki ürünlerin ad, fiyat ve stok bilgisini hızlıca sorgular.
* **`sp_MusteriSatisGecmisi`**: Parametre olarak alınan telefon numarasıyla eşleşen müşterinin geçmişte hangi tarihte hangi üründen ne kadar aldığını detaylıca listeler.

---

## 🖥️ Arayüz Özellikleri (Python & Streamlit)

Arayüz uygulaması kullanıcı dostu bir kontrol paneli sunmaktadır:
* **Ana Sayfa (Dashboard):** Toplam ürün çeşidi, müşteri sayısı ve toplam sipariş miktarını özetleyen metrik kartları.
* **Ürün Yönetimi:** Mevcut tatlıları listeleyen tablo ve sisteme yeni kategori bazlı ürün ekleme formu.
* **Müşteri İşlemleri:** Kayıtlı müşterileri listeleme ve telefon/eposta doğrulamalı yeni müşteri kaydı.
* **Sipariş İşlemleri:**
  * Kayıtlı müşteriyi seçerek veya **"Hızlı Kayıt"** ile anında yeni müşteri oluşturarak sipariş başlatma.
  * Seçilen ürünlerin stok miktarına göre dinamik adet seçimi yapabilen, ara toplamı gösteren **Dinamik Sepet Sistemi**.
  * Geçmiş siparişlerin detaylarını ve satışı yapan tezgahtar bilgisini anlık sorgulama.
* **Gelişmiş Raporlar:** SQL Server'da oluşturulmuş olan 6 farklı raporu sekmeler halinde, grafiksel şemalar (çizgi ve çubuk grafikler) eşliğinde görüntüleme paneli.

---

## ⚙️ Kurulum ve Çalıştırma Adımları

Sistemi kendi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla uygulayabilirsiniz:

### 1. Veritabanının Kurulması (MSSQL Server)

Veritabanını kurmak için iki farklı yöntem tercih edebilirsiniz:

#### **A Yöntemi: Veritabanı Yedeğini Geri Yüklemek (Restore)**
1. SQL Server Management Studio (SSMS) uygulamasını açın.
2. Sol menüde **Databases** klasörüne sağ tıklayıp **Restore Database...** seçeneğini seçin.
3. **Device** kısmını seçerek `2_Veritabani_Yedegi/Tatlici_Yedek.bak` dosyasını gösterin ve veritabanını geri yükleyin.

#### **B Yöntemi: SQL Betiklerini Sırayla Çalıştırmak**
SSMS üzerinde yeni bir sorgu penceresi açıp `1_Veritabani_Tasarimi` klasöründeki dosyaları **numara sırasına göre** (`00_` -> `09_`) çalıştırın.

---

### 2. Arayüzün Kurulumu ve Başlatılması

1. Bilgisayarınızda **Python 3.8+** sürümünün kurulu olduğundan emin olun.
2. Komut satırını (Terminal/PowerShell) açın ve projenin ana dizinine gidin.
3. Gerekli Python kütüphanelerini yükleyin:
   ```bash
   pip install -r 3_Arayuz_Uygulamasi/requirements.txt
   ```
4. **Veritabanı Bağlantısını Yapılandırın:**
   * [db_functions.py](file:///c:/Users/Eda/Desktop/VTYS_%C3%96DEV/3_Arayuz_Uygulamasi/db_functions.py) dosyasını açın.
   * `SERVER` değişkenini kendi SQL Server Instance adınızla güncelleyin (Varsayılan olarak `.\SQLEXPRESS` olarak ayarlanmıştır):
     ```python
     SERVER = r'.\SQLEXPRESS' # veya 'localhost' ya da kendi sunucu adınız
     ```
5. **Uygulamayı Çalıştırın:**
   * Ana dizinde bulunan [baslat.bat](file:///c:/Users/Eda/Desktop/VTYS_%C3%96DEV/baslat.bat) dosyasına çift tıklayarak arayüzü başlatabilirsiniz.
   * Veya terminalden manuel olarak şu komutla çalıştırabilirsiniz:
     ```bash
     cd 3_Arayuz_Uygulamasi
     streamlit run app.py
     ```
   * Tarayıcınız otomatik olarak `http://localhost:8501` adresinde açılacaktır.

---