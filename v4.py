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
vardiya = st.selectbox("Vardiya Türü:", ["Tekli Vardiya", "İkili Vardiya", "Üçlü Vardiya"])
ay_secimi = st.selectbox("Ay Seçimi:", list(ay_gunleri.keys()))
kidem_yili = st.slider("Kıdem Yılı (0-30):", 0, 30, 25)
imza_primi_yuzdesi = st.selectbox("Üretime Dayalı Risk Primi (%):", [0, 3, 4, 6])
calisan_gun = st.number_input("Çalışılan Günler:", min_value=0, max_value=31, value=20)
tatil_gun = st.number_input("Çalışılmayan Günler:", min_value=0, max_value=31, value=10)
yillik_izin = st.number_input("Yıllık İzin Gün Sayısı:", min_value=0, value=0)
fazla_mesai_saat = st.number_input("Fazla Mesai Saat:", min_value=0.0, max_value=24.0, value=0.0)
fazla_mesai_gun = st.number_input("Fazla Mesai Gün:", min_value=0, max_value=31, value=0)
gece_farki_saat = st.number_input("Gece Çalışması Saat:", min_value=0.0, max_value=24.0, value=0.0)
ikramiye = st.selectbox("İkramiye Gün Sayısı:",[0, 18, 19])  
ekstra_prim = st.number_input("Ekstra Prim:", min_value=0.0, value=0.0)
yol_yardimi = st.number_input("Ulaşım Yardımı (TL):", min_value=0.0, value=0.0)
evlilik_var = st.selectbox("Evli misiniz?", ["Evet", "Hayır"])
es_calisiyor = st.selectbox("Eşiniz Çalışıyor mu?", ["Hayır", "Evet"])
cocuk_sayisi = st.number_input("Çocuk Sayısı:", min_value=0, value=0) if evlilik_var == "Evet" else 0
isveren_bes_sigorta = st.number_input("İşveren BES Sigorta (TL):", min_value=0.0, value=0.0)
engelli_indirimi = st.selectbox("Engel İndirimi (TL):", [0, 2400, 5700, 9900])
ozel_kesinti = st.number_input("ilaç , bağış , vb kesintiler (TL):", min_value=0.0, value=0.0)

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
        brüt_ikramiye = son_yevmiyesi * ikramiye

        # Kazançlar
        main_kazanc = son_yevmiyesi * toplam_gun
        kazanclar_toplam = main_kazanc + fazla_mesai_ucreti + gece_farkı

        # Yıllık izin kazancı
        yillik_izin_kazanci = yillik_izin * (son_yevmiyesi * 0.35)

        # Yardımlar
        yardimlar = (sorumluluk_zammi + yakacak_yardimi + is_guclugu_primi + aile_yardimi + cocuk_yardimi + yemek_yardimi + sosyal_yardim +
                     ise_devam_tesvik_primi + ekstra_prim + brüt_ikramiye + uretim_destek_primi + yillik_izin_kazanci + yol_yardimi_toplam)

        # Toplam Kazançlar
        toplam_kazanc = kazanclar_toplam + yardimlar

        # SGK Matrahı:
        if es_calisiyor == "Evet":
            sgk_matrah = toplam_kazanc - (cocuk_yardimi + yol_yardimi + (calisan_gun * 158))
        else:
            sgk_matrah = toplam_kazanc - (aile_yardimi + cocuk_yardimi + yol_yardimi + (calisan_gun * 158))

        # Gelir Vergisi Matrahı ve Hesaplaması:
        sgk_primi = sgk_matrah * 0.14
        isssizlik_primi = sgk_matrah * 0.01
        gelir_vergisi_matrahi = toplam_kazanc - (sgk_primi + isssizlik_primi) - yol_yardimi - cocuk_yardimi - son_yevmiyesi - isveren_bes_sigorta - (calisan_gun * 264)
        gelir_vergisi_matrahi = max(0, gelir_vergisi_matrahi)  # Eğer negatifse sıfırlanır

        # Vergi dilimi
        if ay_secimi in ["Ocak", "Şubat"]:
            vergi_orani = 0.15
        elif ay_secimi in ["Mart", "Nisan"]:
            vergi_orani = 0.20
        elif ay_secimi in ["Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım"]:
            vergi_orani = 0.27
        else:
            vergi_orani = 0.35  # Aralık

        # Vergi İstisnası
        if ay_secimi in ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran"]:
            istisna = 3315.60
        elif ay_secimi == "Temmuz":
            istisna = 4257.57
        else:
            istisna = 4420.80

        # Gelir Vergisi hesaplaması
        toplam_vergi = (gelir_vergisi_matrahi * vergi_orani) - istisna - ( engelli_indirimi * vergi_orani )

        # Damga Vergisi hesaplama
        damga_vergisi_matrahi = (toplam_kazanc -(calisan_gun * 264))
        damga_vergisi = (damga_vergisi_matrahi * 0.00759) - 197.38
        if damga_vergisi < 0:
            damga_vergisi = 0
                      
        # Net Maaş
        devlete_odenen = sgk_primi + isssizlik_primi + toplam_vergi + damga_vergisi + son_yevmiyesi + yol_yardimi

        net_maas = toplam_kazanc - devlete_odenen - ozel_kesinti

        return net_maas

    except Exception as e:
        st.error(f"Hesaplama hatası: {str(e)}")
        return None

# Sonuçları göster
        if st.button("Hesapla"):
        st.success(f"💰 Bankaya Yatan Net Maaş: **{net_maas:,.2f} TL**")
        st.write("---")
        st.subheader("📊 Detaylar")
        st.write(f"Toplam Brüt Maaş: {toplam_brut:,.2f} TL")
        st.write(f"SGK Matrahı: {sgk_matrah:,.2f} TL")
        st.write(f"Gelir Vergisi Matrahı: {gelir_vergisi_matrahi:,.2f} TL")
        st.write(f"Toplam Vergi: {toplam_vergi:,.2f} TL")
        st.write(f"Damga Vergisi: {damga_vergisi:,.2f} TL")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
