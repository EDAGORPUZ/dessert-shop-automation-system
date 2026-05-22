@echo off
echo Tatlici Otomasyonu Arayuzu Baslatiliyor...
echo Lutfen bekleyin, tarayiciniz otomatik olarak acilacaktir.
cd /d "%~dp03_Arayuz_Uygulamasi"
streamlit run app.py
pause
