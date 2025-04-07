import streamlit as st

# Başlık
st.title("İzbeton A.Ş 2025 yılı Sözleşmenin ikinci Yılı Maaş Hesaplama Programı")

# Aylar
ay_gunleri = {
    "Ocak": 31, "Şubat": 28, "Mart": 31, "Nisan": 30, "Mayıs": 31, "Haziran": 30,
    "Temmuz": 31, "Ağustos": 31, "Eylül": 30, "Ekim": 31, "Kasım": 30, "Aralık": 31
}

# Form elemanları
grup = st.selectbox("Grup:", ["A", "B", "C", "D"])
kidem_yili = st.number_input("Kıdem Yılı 0-30:", min_value=0, max_value=30, value=25)
imza_primi_yuzdesi = st.number_input("Üretime Dayalı Risk Primi (%):", min_value=0.0, max_value=10.0, value=6.0)
calisan_gun = st.number_input("Çalışılan Günler:", min_value=0, max_value=31, value=20)
tatil_gun = st.number_input("Çalışılmayan Günler:", min_value=0, max_value=31, value=10)
fazla_mesai_saat = st.number_input("Fazla Mesai Saat:", min_value=0.0, max_value=24.0, value=0.0)
fazla_mesai_gun = st.number_input("Fazla Mesai Gün:", min_value=0, max_value=31, value=0)
gece_farki_saat = st.number_input("Gece Çalışması Saat:", min_value=0.0, max_value=24.0, value=0.0)
ekstra_prim = st.number_input("Ekstra Prim:", min_value=0.0, value=0.0)
yol_yardimi = st.number_input("Ulaşım Yardımı (TL):", min_value=0.0, value=0.0)
ay_secimi = st.selectbox("Ay Seçimi:", list(ay_gunleri.keys()))
evlilik_var = st.selectbox("Evli misiniz?", ["Evet", "Hayır"])
es_calisiyor = st.selectbox("Eşiniz Çalışıyor mu?", ["Hayır", "Evet"])
cocuk_sayisi = st.number_input("Çocuk Sayısı:", min_value=0, value=0) if evlilik_var == "Evet" else 0
yillik_izin = st.number_input("Yıllık İzin Gün Sayısı:", min_value=0, value=0)
vardiya = st.selectbox("Vardiya Türü:", ["Tekli Vardiya", "İkili Vardiya", "Üçlü Vardiya"])
isveren_bes_sigorta = st.number_input("İşveren BES Sigorta (TL):", min_value=0.0, value=0.0)


# Hesaplama Fonksiyonu
def hesapla():
    try:
        # Ay gün sayısı
        toplam_gun = calisan_gun + tatil_gun
        taban_yevmiyeleri = {"A": 1731.59, "B": 1796.93, "C": 1877.90, "D": 1943.24}
        taban_yevmiyesi = taban_yevmiyeleri[grup]

        # Kıdem zammı
        kidem_zammi = kidem_yili * 4.01

        # İmza primi hesaplama
        imza_prim_miktar = taban_yevmiyesi * (imza_primi_yuzdesi / 100)

        # Son yevmiye
        son_yevmiyesi = taban_yevmiyesi + kidem_zammi + imza_prim_miktar

        # Fazla Mesai Ücreti
        fazla_mesai_ucreti = (fazla_mesai_saat * (son_yevmiyesi / 7.5) * 2) + (fazla_mesai_gun * son_yevmiyesi * 2)

        # Gece Farkı
        gece_farkı = (son_yevmiyesi / 7.5 * 2 / 2 * 0.2 * gece_farki_saat)

        # Üretim destek primi
        if vardiya == "Tekli Vardiya":
            uretim_destek_primi = (taban_yevmiyesi * ay_gunleri[ay_secimi] / 100) * 7
        elif vardiya == "İkili Vardiya":
            uretim_destek_primi = (taban_yevmiyesi * ay_gunleri[ay_secimi] / 100) * 10
        elif vardiya == "Üçlü Vardiya":
            uretim_destek_primi = (taban_yevmiyesi * ay_gunleri[ay_secimi] / 100) * 12

        # Sabit yardımlar
        aile_yardimi = 2301.54 if evlilik_var == "Evet" else 0
        cocuk_yardimi = cocuk_sayisi * 253.14
        yemek_yardimi = calisan_gun * 330.98
        sosyal_yardim = 3846.71
        sorumluluk_zammi = 6525.78
        yakacak_yardimi = 3309.77
        is_guclugu_primi = calisan_gun * 27.56
        ise_devam_tesvik_primi = (taban_yevmiyesi + kidem_zammi + imza_prim_miktar) * 2

        # Yol Yardımı
        yol_yardimi_toplam = yol_yardimi

        # İkramiye hesaplama
        brüt_ikramiye = son_yevmiyesi * 19

        # Kazançlar
        main_kazanc = son_yevmiyesi * toplam_gun
        kazanclar_toplam = main_kazanc + fazla_mesai_ucreti + gece_farkı

        # Yıllık izin kazancı
        yillik_izin_kazanci = yillik_izin * (son_yevmiyesi * 0.35)

        # Yardımlar
        yardimlar = aile_yardimi + cocuk_yardimi + yemek_yardimi + sosyal_yardim + sorumluluk_zammi + yakacak_yardimi + is_guclugu_primi + ise_devam_tesvik_primi + yol_yardimi_toplam

        # Toplam Kazançlar
        toplam_kazanc = kazanclar_toplam + yardimlar + ekstra_prim + isveren_bes_sigorta + yillik_izin_kazanci + uretim_destek_primi

        # Çıktı
        st.write(f"Toplam Kazanç: {toplam_kazanc:.2f} TL")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")

# Hesapla butonu
if st.button("Hesapla"):
    hesapla()
