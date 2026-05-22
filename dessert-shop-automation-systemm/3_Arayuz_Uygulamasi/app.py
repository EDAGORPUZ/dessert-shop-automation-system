import streamlit as st
import db_functions as db
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Tatlıcı Otomasyonu", page_icon="🍰", layout="wide")

# Session State (Sepet için)
if 'sepet' not in st.session_state:
    st.session_state.sepet = []

# Sol Menü (Sidebar)
st.sidebar.title("🍰 Tatlıcı Otomasyonu")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Menü Seçimi",
    ("Ana Sayfa (Dashboard)", "Ürün Yönetimi", "Müşteri İşlemleri", "Siparişler", "Raporlar")
)

# ----------------- ANA SAYFA -----------------
if menu == "Ana Sayfa (Dashboard)":
    st.title("📊 Yönetim Paneli")
    st.markdown("Tatlıcı otomasyon sistemine hoş geldiniz! Sol menüden işlem seçebilirsiniz.")
    
    col1, col2, col3 = st.columns(3)
    
    df_urunler = db.get_urunler()
    df_musteriler = db.get_musteriler()
    df_siparisler = db.get_siparisler()
    
    with col1:
        urun_sayisi = len(df_urunler) if not df_urunler.empty else 0
        st.metric(label="Toplam Ürün Çeşidi", value=urun_sayisi)
        
    with col2:
        musteri_sayisi = len(df_musteriler) if not df_musteriler.empty else 0
        st.metric(label="Toplam Kayıtlı Müşteri", value=musteri_sayisi)
        
    with col3:
        siparis_sayisi = len(df_siparisler) if not df_siparisler.empty else 0
        st.metric(label="Toplam Sipariş", value=siparis_sayisi)

# ----------------- ÜRÜN YÖNETİMİ -----------------
elif menu == "Ürün Yönetimi":
    st.title("🍩 Ürün Yönetimi")
    
    tab1, tab2 = st.tabs(["Ürün Listesi", "Yeni Ürün Ekle"])
    
    with tab1:
        st.subheader("Mevcut Tatlılar")
        df_urunler = db.get_urunler()
        if not df_urunler.empty:
            st.dataframe(df_urunler, use_container_width=True, hide_index=True)
        else:
            st.info("Veritabanında kayıtlı ürün bulunamadı veya bağlantı sağlanamadı.")
            
    with tab2:
        st.subheader("Sisteme Yeni Tatlı Ekle")
        df_kat = db.get_kategoriler()
        if not df_kat.empty:
            kategori_dict = dict(zip(df_kat['KategoriAd'], df_kat['KategoriID']))
            
            with st.form("urun_ekle_form"):
                yeni_urun_ad = st.text_input("Tatlı Adı")
                secilen_kategori = st.selectbox("Kategori", list(kategori_dict.keys()))
                yeni_fiyat = st.number_input("Birim Fiyat (TL)", min_value=0.0, format="%.2f")
                yeni_stok = st.number_input("Stok Miktarı", min_value=0, step=1)
                
                submit = st.form_submit_button("Ürünü Kaydet")
                
                if submit:
                    if yeni_urun_ad:
                        kat_id = kategori_dict[secilen_kategori]
                        if db.add_urun(yeni_urun_ad, kat_id, yeni_fiyat, yeni_stok):
                            st.success(f"'{yeni_urun_ad}' başarıyla eklendi!")
                            st.rerun()
                        else:
                            st.error("Ürün eklenirken hata oluştu.")
                    else:
                        st.warning("Lütfen ürün adını giriniz.")
        else:
            st.warning("Önce veritabanına kategori eklenmesi gerekmektedir.")

# ----------------- MÜŞTERİ İŞLEMLERİ -----------------
elif menu == "Müşteri İşlemleri":
    st.title("👥 Müşteri İşlemleri")
    
    tab1, tab2 = st.tabs(["Müşteri Listesi", "Yeni Müşteri Ekle"])
    
    with tab1:
        st.subheader("Kayıtlı Müşteriler")
        df_musteriler = db.get_musteriler()
        if not df_musteriler.empty:
            st.dataframe(df_musteriler, use_container_width=True, hide_index=True)
        else:
            st.info("Sistemde müşteri bulunmuyor.")
            
    with tab2:
        st.subheader("Yeni Müşteri Kaydı")
        with st.form("musteri_ekle_form"):
            m_ad = st.text_input("Ad")
            m_soyad = st.text_input("Soyad")
            m_telefon = st.text_input("Telefon (11 Hane)", max_chars=11)
            m_eposta = st.text_input("E-posta (İsteğe bağlı)")
            
            submit_m = st.form_submit_button("Müşteri Ekle")
            
            if submit_m:
                if m_ad and m_soyad and m_telefon:
                    if db.add_musteri(m_ad, m_soyad, m_telefon, m_eposta if m_eposta else None):
                        st.success("Müşteri başarıyla kaydedildi!")
                        st.rerun()
                    else:
                        st.error("Kayıt başarısız. Telefon numarası daha önce eklenmiş olabilir.")
                else:
                    st.warning("Lütfen Ad, Soyad ve Telefon alanlarını doldurun.")

# ----------------- SİPARİŞLER -----------------
elif menu == "Siparişler":
    st.title("🛒 Sipariş İşlemleri")
    
    tab1, tab2 = st.tabs(["Yeni Sipariş Oluştur", "Geçmiş Siparişler & Detaylar"])
    
    with tab1:
        st.subheader("Sipariş Sepeti")
        df_musteriler = db.get_musteriler()
        df_calisanlar = db.get_calisanlar()
        df_urunler = db.get_urunler()
        
        if not df_musteriler.empty and not df_calisanlar.empty and not df_urunler.empty:
            # 1. Müşteri ve Çalışan Seçimi
            st.markdown("**Müşteri ve Çalışan Bilgileri**")
            musteri_tipi = st.radio("Müşteri Seçimi", ["Kayıtlı Müşteri", "Yeni Müşteri Oluştur (Hızlı Kayıt)"], horizontal=True)
            
            col1, col2 = st.columns(2)
            
            yeni_m_ad = ""
            yeni_m_soyad = ""
            yeni_m_tel = ""
            
            with col1:
                if musteri_tipi == "Kayıtlı Müşteri":
                    musteri_isimleri = df_musteriler['Ad'] + ' ' + df_musteriler['Soyad'] + ' (' + df_musteriler['Telefon'] + ')'
                    musteri_dict = dict(zip(musteri_isimleri, df_musteriler['MusteriID']))
                    secilen_musteri = st.selectbox("Müşteri Seçin", list(musteri_dict.keys()))
                else:
                    st.info("Bu bilgiler sipariş tamamlandığında otomatik kaydedilecektir.")
                    yeni_m_ad = st.text_input("Müşteri Adı *")
                    yeni_m_soyad = st.text_input("Müşteri Soyadı *")
                    yeni_m_tel = st.text_input("Telefon (11 Hane) *", max_chars=11)
            
            with col2:
                calisan_dict = dict(zip(df_calisanlar['AdSoyad'], df_calisanlar['CalisanID']))
                secilen_calisan = st.selectbox("Satışı Yapan Çalışan (Tezgahtar)", list(calisan_dict.keys()))
            
            st.markdown("---")
            
            # 2. Ürün Sepete Ekleme
            st.markdown("**Ürün Seçimi**")
            col3, col4, col5 = st.columns([2, 1, 1])
            
            urun_isimleri = df_urunler['UrunAd'].tolist()
            secilen_urun_ad = col3.selectbox("Tatlı Seçin", urun_isimleri)
            
            # Seçilen ürünün bilgisini al
            urun_bilgi = df_urunler[df_urunler['UrunAd'] == secilen_urun_ad].iloc[0]
            max_stok = int(urun_bilgi['StokMiktari'])
            birim_fiyat = float(urun_bilgi['BirimFiyat'])
            
            alinacak_adet = col4.number_input(f"Adet (Stok: {max_stok})", min_value=1, max_value=max_stok if max_stok>0 else 1, step=1)
            
            if col5.button("Sepete Ekle", use_container_width=True):
                if max_stok < alinacak_adet:
                    st.error("Yeterli stok yok!")
                else:
                    st.session_state.sepet.append({
                        'urun_ad': secilen_urun_ad,
                        'urun_id': int(urun_bilgi['UrunID']),
                        'adet': alinacak_adet,
                        'fiyat': birim_fiyat,
                        'ara_toplam': alinacak_adet * birim_fiyat
                    })
                    st.success(f"{secilen_urun_ad} sepete eklendi.")
            
            # 3. Sepet Özeti
            if st.session_state.sepet:
                st.markdown("### 🛍️ Sepetiniz")
                df_sepet = pd.DataFrame(st.session_state.sepet)
                # Görüntüleme için tabloyu düzenle
                df_goster = df_sepet[['urun_ad', 'adet', 'fiyat', 'ara_toplam']].rename(
                    columns={'urun_ad': 'Ürün', 'adet': 'Adet', 'fiyat': 'Birim Fiyat', 'ara_toplam': 'Ara Toplam'}
                )
                st.table(df_goster)
                
                toplam_tutar = sum(item['ara_toplam'] for item in st.session_state.sepet)
                st.subheader(f"Genel Toplam: {toplam_tutar:.2f} TL")
                
                col_clear, col_submit = st.columns(2)
                if col_clear.button("Sepeti Temizle"):
                    st.session_state.sepet = []
                    st.rerun()
                    
                if col_submit.button("✅ Siparişi Tamamla", type="primary"):
                    m_id = None
                    # Müşteri belirleme
                    if musteri_tipi == "Kayıtlı Müşteri":
                        m_id = musteri_dict[secilen_musteri]
                    else:
                        if yeni_m_ad and yeni_m_soyad and yeni_m_tel:
                            # Önce müşteriyi veritabanına kaydet ve ID'sini al
                            m_id = db.add_musteri_get_id(yeni_m_ad, yeni_m_soyad, yeni_m_tel)
                            if not m_id:
                                st.error("Müşteri sisteme kaydedilemedi. Bu telefon numarası başkasına ait olabilir.")
                        else:
                            st.warning("Lütfen yeni müşterinin Ad, Soyad ve Telefon bilgilerini eksiksiz doldurun.")
                            
                    if m_id: # Müşteri id'si başarıyla alındıysa siparişi tamamla
                        c_id = calisan_dict[secilen_calisan]
                        
                        if db.add_siparis_with_details(m_id, c_id, toplam_tutar, st.session_state.sepet):
                            st.balloons()
                            if musteri_tipi == "Yeni Müşteri Oluştur (Hızlı Kayıt)":
                                st.success("Yeni müşteri sisteme eklendi ve sipariş başarıyla oluşturuldu! Stoklar güncellendi.")
                            else:
                                st.success("Sipariş başarıyla oluşturuldu! Stoklar güncellendi.")
                            st.session_state.sepet = [] # Sepeti boşalt
                        else:
                            st.error("Sipariş oluşturulurken bir hata meydana geldi.")
        else:
            st.warning("Sipariş oluşturabilmek için sistemde müşteri, çalışan ve ürün bulunmalıdır.")

    with tab2:
        st.subheader("Geçmiş Siparişler")
        df_siparisler = db.get_siparisler()
        if not df_siparisler.empty:
            # Sipariş ID'sine göre detay getirme
            siparis_liste = [f"Sipariş No: {row['SiparisID']} - {row['Musteri']} ({row['SiparisTarihi'].strftime('%Y-%m-%d')})" for idx, row in df_siparisler.iterrows()]
            secilen_siparis_str = st.selectbox("Detayını Görmek İstediğiniz Siparişi Seçin", siparis_liste)
            
            secilen_id = int(secilen_siparis_str.split(" ")[2]) # 'Sipariş No: 12 - ...' içinden 12'yi alır
            
            # Detay tablosu
            st.markdown(f"**Sipariş No: {secilen_id} Detayları**")
            df_detay = db.get_siparis_detaylari(secilen_id)
            if not df_detay.empty:
                st.dataframe(df_detay, use_container_width=True, hide_index=True)
                
                # Genel bilgileri altta göster
                s_bilgi = df_siparisler[df_siparisler['SiparisID'] == secilen_id].iloc[0]
                st.info(f"Müşteri: {s_bilgi['Musteri']} | Satışı Yapan: {s_bilgi['Calisan']} | **Toplam Tutar: {s_bilgi['ToplamTutar']} TL**")
            else:
                st.warning("Bu siparişe ait detay bulunamadı.")
        else:
            st.info("Henüz sipariş kaydı bulunmuyor.")

# ----------------- RAPORLAR -----------------
elif menu == "Raporlar":
    st.title("📈 Gelişmiş Raporlar")
    st.markdown("Aşağıdaki sekmelerden sistemdeki 6 farklı SQL raporuna ulaşabilirsiniz.")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Kategorili Liste (View)", 
        "Kategori Filtresi (SP)", 
        "Kritik Stok", 
        "En Çok Satanlar", 
        "Günlük Ciro", 
        "Müşteri Geçmişi"
    ])
    
    with tab1:
        st.subheader("Rapor 1: Ürünlerin Kategorileriyle Listesi")
        df1 = db.get_vw_urun_listesi_kategori()
        if not df1.empty:
            st.dataframe(df1, use_container_width=True, hide_index=True)
        else:
            st.info("Kayıt bulunamadı.")

    with tab2:
        st.subheader("Rapor 2: Kategoriye Göre Ürünler (Stored Procedure)")
        df_kat = db.get_kategoriler()
        if not df_kat.empty:
            kat_isimleri = df_kat['KategoriAd'].tolist()
            secili_kat = st.selectbox("Kategori Seçin:", kat_isimleri)
            if st.button("Ürünleri Getir"):
                df2 = db.get_urunler_by_kategori(secili_kat)
                if not df2.empty:
                    st.dataframe(df2, use_container_width=True, hide_index=True)
                else:
                    st.info("Bu kategoride ürün bulunamadı.")
                    
    with tab3:
        st.subheader("Rapor 3: Kritik Stok Takibi")
        st.markdown("*Stok miktarı 15'in altına düşen ürünleri listeler.*")
        df3 = db.get_kritik_stok()
        if not df3.empty:
            st.error("Dikkat: Aşağıdaki ürünlerin stoğu azalmış durumda!")
            st.dataframe(df3, use_container_width=True, hide_index=True)
        else:
            st.success("Tüm ürünlerin stokları yeterli seviyede.")
            
    with tab4:
        st.subheader("Rapor 4: En Çok Satan İlk 5 Ürün")
        df4 = db.get_encok_satan()
        if not df4.empty:
            st.bar_chart(data=df4, x="Ürün", y="Toplam Satış Adedi")
            st.dataframe(df4, use_container_width=True, hide_index=True)
        else:
            st.info("Henüz yeterli satış verisi yok.")

    with tab5:
        st.subheader("Rapor 5: Günlük Kazanç (Ciro) Raporu")
        df5 = db.get_gunluk_ciro()
        if not df5.empty:
            st.line_chart(data=df5, x="Tarih", y="Toplam Ciro")
            st.dataframe(df5, use_container_width=True, hide_index=True)
        else:
            st.info("Henüz satış yapılmamış.")
            
    with tab6:
        st.subheader("Rapor 6: Müşteri Sipariş Geçmişi Sorgulama")
        st.markdown("*Müşterinin telefon numarasını girerek tüm geçmiş alımlarını görebilirsiniz.*")
        tel_ara = st.text_input("Telefon Numarası (11 Hane):", max_chars=11)
        if st.button("Geçmişi Sorgula"):
            if tel_ara:
                df6 = db.get_musteri_satis_gecmisi(tel_ara)
                if not df6.empty:
                    st.dataframe(df6, use_container_width=True, hide_index=True)
                else:
                    st.warning("Bu telefon numarasına ait bir sipariş kaydı bulunamadı.")
            else:
                st.error("Lütfen bir telefon numarası giriniz.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("VTYS Final Projesi - Arayüz")
