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
kumulatif_matrah = st.number_input("Kümüle Vergi Matrahı (TL):", min_value=0.0, value=0.0) 
kumule_gelir_vergisi = st.number_input("Kümüle Gelir Vergisi (TL):", min_value=0.0, value=0.0)

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

        # Yardımların Özeti
        yardimlar_ozeti = {
            "Sorumluluk Zammı": sorumluluk_zammi,
            "Yakacak Yardımı": yakacak_yardimi,
            "İş Gücü Primi": is_guclugu_primi,
            "Aile Yardımı": aile_yardimi,
            "Çocuk Yardımı": cocuk_yardimi,
            "Yemek Yardımı": yemek_yardimi,
            "Sosyal Yardım": sosyal_yardim,
            "İşe Devam Teşvik Primi": ise_devam_tesvik_primi,
            "Ekstra Prim": ekstra_prim,
            "İkramiye": brüt_ikramiye,
            "Üretim Destek Primi": uretim_destek_primi,
            "Yıllık İzin Kazancı": yillik_izin_kazanci,
            "Yol Yardımı": yol_yardimi_toplam
        }
        
        # Toplam Kazançlar
        toplam_kazanc = kazanclar_toplam + yardimlar
try:
        # Kodun geri kalanı
    if evlilik_var == "Evet":
        if es_calisiyor == "Evet":
            sgk_matrah = toplam_kazanc - (cocuk_yardimi + yol_yardimi + (calisan_gun * 158))
        else:
            sgk_matrah = toplam_kazanc - (aile_yardimi + cocuk_yardimi + yol_yardimi) + (calisan_gun * 158)
    else:
        sgk_matrah = toplam_kazanc - (cocuk_yardimi + yol_yardimi + (calisan_gun * 158))

except Exception as e:
    st.error(f"Hata: {str(e)}")




        # SGK Primi ve işsizlik primi Hesaplama:
        sgk_primi = sgk_matrah * 0.14
        isssizlik_primi = sgk_matrah * 0.01

        # Gelir Vergisi Hesaplama:
        gelir_vergisi_matrahi = toplam_kazanc - (sgk_primi + isssizlik_primi) - yol_yardimi - cocuk_yardimi - son_yevmiyesi - isveren_bes_sigorta - (calisan_gun * 264) - engelli_indirimi 
        gelir_vergisi_matrahi = max(0, gelir_vergisi_matrahi)

        def gelir_vergisi_hesapla(kumulatif_matrah):
            if kumulatif_matrah <= 158000:
                vergi = kumulatif_matrah * 0.15
            elif kumulatif_matrah <= 330000:
                vergi = 23700 + (kumulatif_matrah - 158000) * 0.20
            elif kumulatif_matrah <= 1200000:
                vergi = 58100 + (kumulatif_matrah - 330000) * 0.27
            elif kumulatif_matrah <= 4300000:
                vergi = 293000 + (kumulatif_matrah - 1200000) * 0.35
            else:
                vergi = 1378000 + (kumulatif_matrah - 4300000) * 0.40
            return vergi

        # Vergi İstisnası
            if ay_secimi in ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran"]:
                istisna = 3315.60
            elif ay_secimi == "Temmuz":
                istisna = 4257.57
            else:
                istisna = 4420.80
        
        kumulatif_vergi = gelir_vergisi_hesapla(kumulatif_matrah )
        toplam_vergi = kumulatif_vergi - kumule_gelir_vergisi - istisna
        toplam_vergi = max(0, toplam_vergi)


       
        # Damga Vergisi hesaplama
        damga_vergisi_matrahi = (toplam_kazanc -(calisan_gun * 264))
        damga_vergisi = (damga_vergisi_matrahi * 0.00759) - 197.38
            if damga_vergisi < 0:
                damga_vergisi = 0
                      
        # Net Maaş
        devlete_odenen = sgk_primi + isssizlik_primi + toplam_vergi + damga_vergisi + son_yevmiyesi + yol_yardimi

        net_maas = toplam_kazanc - devlete_odenen - ozel_kesinti

        return {
            "Net Maaş": net_maas,
            "Kazançlar Toplamı": kazanclar_toplam,
            "Yardımlar Toplamı": yardimlar,
            "Yardımlar Özeti": yardimlar_ozeti,
            "Matrahlar": {
                "Toplam Kazanç": toplam_kazanc,
                "SGK Matrahı": sgk_matrah,
                "Gelir Vergisi Matrahı": gelir_vergisi_matrahi,
                "Damga Vergisi Matrahı": damga_vergisi_matrahi
            },
            "Devlete Ödenenler": {
                "SGK Primi": sgk_primi,
                "İşsizlik Primi": isssizlik_primi,
                "Gelir Vergisi": toplam_vergi,
                "Damga Vergisi": damga_vergisi,
                "Sendika Aidatı (Son Yevmiye)": son_yevmiyesi
            }
        }

    except Exception as e:
        st.error(f"Hesaplama hatası: {str(e)}")
        return None

# Hesaplama butonuna basıldığında sonucu göster
if st.button("Hesapla"):
    sonuclar = hesapla()
    if sonuclar:
        st.subheader("Yardımlar Özeti")
        for yardim, tutar in sonuclar["Yardımlar Özeti"].items():
            st.write(f"{yardim}: {tutar:.2f} TL")
        
        st.subheader("Matrahlar")
        for matrah, tutar in sonuclar["Matrahlar"].items():
            st.write(f"{matrah}: {tutar:.2f} TL")
            
        st.subheader("Devlete Ödenenler")
        for odeme, tutar in sonuclar["Devlete Ödenenler"].items():
            st.write(f"{odeme}: {tutar:.2f} TL")

        st.subheader("Net Maaş")
        st.write(f"Net Maaş: {sonuclar['Net Maaş']:.2f} TL")
