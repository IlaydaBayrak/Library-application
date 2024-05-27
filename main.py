#%%
#----------------------KÜTÜPHANE

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QTableWidgetItem
from loginUI import Ui_Form
from kitapListesiUI import Ui_Form2
from personelEkraniUI import Ui_Form3

#%%
#----------------------UYGULAMA

uygulama = QApplication(sys.argv)
pencereLogin = QWidget()
ui = Ui_Form()
ui.setupUi(pencereLogin)
pencereLogin.show()

pencereKitapList = QMainWindow()
ui3 = Ui_Form2()
ui3.setupUi(pencereKitapList)

pencerePerEkrani = QMainWindow()
ui4 = Ui_Form3()
ui4.setupUi(pencerePerEkrani)

#----------------------VERİTABANI_OGRENCI

import sqlite3
global curs
global conn

conn = sqlite3.connect('veritabani_kutuphane.db')
curs = conn.cursor()
ogrenciKayit = ("""
        CREATE TABLE IF NOT EXISTS ogrenciListe (
        Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        OgrenciNo TEXT NOT NULL UNIQUE,
        Isim TEXT NOT NULL,
        Soyisim TEXT NOT NULL,
        Bolum TEXT NOT NULL,
        Sinif TEXT NOT NULL,
        Sifre INTEGER NOT NULL)
""")
curs.execute(ogrenciKayit)
conn.commit()

#%%
#----------------------VERİTABANI_PERSONEL

global curs1
global conn1

conn1 = sqlite3.connect('veritabani_kutuphane.db')
curs1 = conn1.cursor()
personelKayit = ("""
        CREATE TABLE IF NOT EXISTS personelListe (
        Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        PersonelNo TEXT NOT NULL UNIQUE,
        Isim TEXT NOT NULL,
        Soyisim TEXT NOT NULL,
        PSifre TEXT NOT NULL)
        """)
curs1.execute(personelKayit)
conn1.commit()

#%%
#----------------------VERİTABANI_KİTAPLAR

global curs2
global conn2

conn2 = sqlite3.connect('veritabani_kutuphane.db')
curs2 = conn2.cursor()
kitapKayit = ("""
        CREATE TABLE IF NOT EXISTS Kitaplar (
        Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        ISBN TEXT NOT NULL UNIQUE,
        KitapAdi TEXT NOT NULL,
        Yazar TEXT NOT NULL,
        YayinEvi TEXT NOT NULL,
        BasimYili TEXT NOT NULL,
        Durum TEXT NOT NULL,
        KitabiAlanOgrenciNo INTEGER DEFAULT -1,
        FOREIGN KEY (KitabiAlanOgrenciNo) REFERENCES ogrenciListe (Id) ON DELETE SET NULL)
""")
curs2.execute(kitapKayit)
conn2.commit()



#%%
#-----------------------------OGRENCİ_KAYIT

def KAYITOL():
    try:
        _leisim = ui.leisim.text()
        _leSoyisim = ui.leSoyisim.text()
        _leOgrenciNo = ui.leOgrenciNo.text()
        _comboBolum = ui.comboBolum.currentText()
        _comboSinif = ui.comboSinif.currentText()
        _leSifre = ui.leSifre.text()
        _leSifreTekrar = ui.leSifreTekrar.text()

        if _leSifre != "" and _leSifre == _leSifreTekrar:
            curs.execute("INSERT INTO ogrenciListe (Isim, Soyisim, OgrenciNo, Bolum, Sinif, Sifre) VALUES (?, ?, ?, ?, ?, ?)",
                         (_leisim, _leSoyisim, _leOgrenciNo, _comboBolum, _comboSinif, _leSifre))
            
            message_box = QMessageBox()
            message_box.setWindowTitle("KAYIT İŞLEMİ")
            message_box.setText("Kaydınız oluşturulmuştur. Giriş yapabilirsiniz.")
            message_box.exec_()
            
        else:
            message_box = QMessageBox()
            message_box.setWindowTitle("UYARI")
            message_box.setText("Bilgileri kontrol ediniz.")
            message_box.exec_()
    except Exception as Hata:
        message_box = QMessageBox()
        message_box.setWindowTitle("Hata")
        message_box.setText("Şöyle bir hata ile karşılaşıldı: " + str(Hata))
        message_box.exec_()

    conn.commit()

    ui.leisim.clear()
    ui.leSoyisim.clear()
    ui.leOgrenciNo.clear()
    ui.comboBolum.setCurrentIndex(-1)
    ui.comboSinif.setCurrentIndex(-1)
    ui.leSifre.clear()
    ui.leSifreTekrar.clear()
    
#%%
#-----------------------------OGRENCİ_GIRIS

def GIRIS():
    student_no = ui.kullaniciAdi.text()
    password = ui.kullaniciSifre.text()
    
    query = "SELECT * FROM ogrenciListe WHERE OgrenciNo=? AND Sifre=?"
    result = curs.execute(query, (student_no, password))
    
    row = result.fetchone()
    
    if row:
        pencereKitapList.show()
        pencereLogin.hide()
        KitapListesi()
    else:
        message_box = QMessageBox()
        message_box.setWindowTitle("UYARI")
        message_box.setText("Bilgileri kontrol ediniz.")
        message_box.exec_()
        
    ui.kullaniciAdi.clear()
    ui.kullaniciSifre.clear()

#%%
#-----------------------------PERSONEL_GIRIS_EKRANI

def PerEkrani():
    personel_no = ui.lePersonelAd.text()
    personel_password = ui.lePersonelSifre.text()
    
    query = "SELECT * FROM personelListe WHERE PersonelNo=? AND PSifre=?"
    result = curs1.execute(query, (personel_no, personel_password))
    
    row = result.fetchone()
    
    if row:
        pencerePerEkrani.show()
        pencereLogin.hide()
    else:
        message_box = QMessageBox()
        message_box.setWindowTitle("UYARI")
        message_box.setText("Bilgileri kontrol ediniz.")
        message_box.exec_()
    LISTELE()
    ui.lePersonelAd.clear()
    ui.lePersonelSifre.clear()
    
   
#%%
#-----------------------------KİTAP_KAYIT

def KitapKayıt():
    _leISBN = ui4.leISBN.text()
    _leKitapAdi = ui4.leKitapAdi.text()
    _leYazar = ui4.leYazar.text()
    _leYayinevi = ui4.leYayinevi.text()
    _leBasimYili = ui4.leBasimYili.text()
    _comboDurum = ui4.comboDurum.currentText()
    _leodunc = ui4.leodunc.text()
    
    if _leodunc == "yok" or _leodunc == "Yok":
        _leodunc = "yok"

    curs2.execute("SELECT Id FROM ogrenciListe WHERE OgrenciNo = ?", (_leodunc,))
    ogrenci_result = curs2.fetchone()
    if _leodunc != "yok" and ogrenci_result is None:
        message_box = QMessageBox()
        message_box.setWindowTitle("ÖĞRENCİ KONTROLÜ")
        message_box.setText("Böyle bir öğrenci bulunamadı. Lütfen geçerli bir öğrenci numarası girin.")
        message_box.exec_()
        return

    curs2.execute("INSERT INTO Kitaplar (ISBN, KitapAdi, Yazar, YayinEvi, BasimYili, Durum, KitabiAlanOgrenciNo) VALUES (?, ?, ?, ?, ?, ?, ?)",
                 (_leISBN, _leKitapAdi, _leYazar, _leYayinevi, _leBasimYili, _comboDurum, _leodunc))
    conn2.commit()
    
    LISTELE()

    message_box = QMessageBox()
    message_box.setWindowTitle("KİTAP EKLEME")
    message_box.setText("Kitap eklendi...")
    message_box.exec_()


    ui4.leISBN.clear()
    ui4.leKitapAdi.clear()
    ui4.leYazar.clear()
    ui4.leYayinevi.clear()
    ui4.leBasimYili.clear()
    ui4.comboDurum.setCurrentIndex(-1)
    ui4.leodunc.clear()
    
#%%
#--------------------------LİSTELE

def LISTELE():
    
    ui4.tableWidget.clear()
    ui4.tableWidget.setColumnCount(8)
    ui4.tableWidget.setHorizontalHeaderLabels(["ID", "ISBN No", "Kitap Adı", "Yazar", "Yayın Evi", "Basım Yılı", "Durum", "KitabiAlanOgrenciNo"])

    curs2.execute("SELECT * FROM Kitaplar")
    rows = curs2.fetchall()
    row_count = len(rows)
    ui4.tableWidget.setRowCount(row_count)

    for row_idx, row_data in enumerate(rows):
        for col_idx, col_data in enumerate(row_data):
            item = QTableWidgetItem(str(col_data))
            ui4.tableWidget.setItem(row_idx, col_idx, item)

#%%
#----------------------SIL

def SIL():
    cevap = QMessageBox.question(pencerePerEkrani, "KAYIT SİL", "Kaydı silmek istediğinize emin misiniz?", QMessageBox.Yes | QMessageBox.No)
    if cevap == QMessageBox.Yes:
        secili = ui4.tableWidget.selectedItems()
        silinecek = secili[1].text()
        try:
            curs2.execute("DELETE FROM Kitaplar WHERE ISBN = ?", (silinecek,))
            conn2.commit()
            LISTELE()
            message_box = QMessageBox()
            message_box.setWindowTitle("Kayıt Silme")
            message_box.setText("Kayıt silme işlemi başarılı bir şekilde gerçekleşti.")
            message_box.exec_()
        except Exception as Hata:
            message_box = QMessageBox()
            message_box.setWindowTitle("Hata")
            message_box.setText("Şöyle bir hata ile karşılaşıldı: " + str(Hata))
            message_box.exec_()
    else:
        message_box = QMessageBox()
        message_box.setWindowTitle("Bilgi")
        message_box.setText("Silme işlemi iptal edildi.")
        message_box.exec_()
        
    ui4.leISBN.clear()
    ui4.leKitapAdi.clear()
    ui4.leYazar.clear()
    ui4.leYayinevi.clear()
    ui4.leBasimYili.clear()
    ui4.comboDurum.setCurrentIndex(-1)
    ui4.leodunc.clear()

#%%
#--------------------------KİTAP_LİSTELE_OGRENCI
def KitapListesi():
    ui3.tableKitapList.clear()
    ui3.tableKitapList.setColumnCount(7)
    ui3.tableKitapList.setHorizontalHeaderLabels(["ID", "ISBN No", "Kitap Adı", "Yazar", "Yayın Evi", "Basım Yılı", "Durum"])
    curs1.execute("SELECT * FROM Kitaplar")
    rows = curs1.fetchall()
    row_count = len(rows)
    ui3.tableKitapList.setRowCount(row_count)

    for row_idx, row_data in enumerate(rows):
        for col_idx, col_data in enumerate(row_data):
            item = QTableWidgetItem(str(col_data))
            ui3.tableKitapList.setItem(row_idx, col_idx, item)

#%%
#--------------------------KİTAP_LİSTESİ_ARA_ÖĞRENCİ

def AraOgrenci():
    aranacakKelime = ui3.leArama.text()
    query = "SELECT * FROM Kitaplar WHERE KitapAdi LIKE ? OR Yazar LIKE ?"
    param = ('%' + aranacakKelime + '%', '%' + aranacakKelime + '%')
    curs2.execute(query, param)
    conn2.commit()
    ui3.tableKitapList.clear()
    
    ui3.tableKitapList.setHorizontalHeaderLabels(["ID", "ISBN No", "Kitap Adı", "Yazar", "Yayın Evi", "Basım Yılı", "Durum"])
        
    rows = curs2.fetchall()
    row_count = len(rows)
    ui3.tableKitapList.setRowCount(row_count)
    
    for row_idx, row_data in enumerate(rows):
        for col_idx, col_data in enumerate(row_data):
            item = QTableWidgetItem(str(col_data))
            ui3.tableKitapList.setItem(row_idx, col_idx, item)
    
    ui3.leArama.clear()
#%%
#--------------------------KİTAP_LİSTESİ_ARA_PERSONEL
def AraPersonel():
    aranacakKelime = ui4.leAramaKutusu.text()
    query = "SELECT * FROM Kitaplar WHERE KitapAdi LIKE ? OR Yazar LIKE ?"
    param = ('%' + aranacakKelime + '%', '%' + aranacakKelime + '%')
    curs2.execute(query, param)
    conn2.commit()
    ui4.tableWidget.clear()
    
    ui4.tableWidget.setHorizontalHeaderLabels(["ID", "ISBN No", "Kitap Adı", "Yazar", "Yayın Evi", "Basım Yılı", "Durum", "KitabiAlanOgrenciNo"])
        
    rows = curs2.fetchall()
    row_count = len(rows)
    ui4.tableWidget.setRowCount(row_count)

    for row_idx, row_data in enumerate(rows):
        for col_idx, col_data in enumerate(row_data):
            item = QTableWidgetItem(str(col_data))
            ui4.tableWidget.setItem(row_idx, col_idx, item)

    ui4.leAramaKutusu.clear()

#%%
#--------------------------GUNCELLE
def GUNCELLE():
    cevap = QMessageBox.question(pencerePerEkrani, "KAYIT GÜNCELLE", "Kaydı güncellemek istediğinize emin misiniz?",\
                                 QMessageBox.Yes | QMessageBox.No)
    if cevap == QMessageBox.Yes:
        try:
            secili = ui4.tableWidget.selectedItems()
            _leISBN = int(secili[1].text())
            _leKitapAdi = ui4.leKitapAdi.text()
            _leYazar = ui4.leYazar.text()
            _leYayinevi = ui4.leYayinevi.text()
            _leBasimYili = ui4.leBasimYili.text()
            _comboDurum = ui4.comboDurum.currentText()
            _leodunc = ui4.leodunc.text()
            
            curs2.execute("UPDATE Kitaplar SET \
                             KitapAdi = ?, Yazar = ?, YayinEvi = ?, BasimYili = ?, Durum = ?, KitabiAlanOgrenciNo=?\
                             WHERE ISBN = ? ", \
                         (_leKitapAdi, _leYazar, _leYayinevi, _leBasimYili, _comboDurum, _leodunc, _leISBN))
            conn.commit()
            LISTELE()

            message_box = QMessageBox()
            message_box.setWindowTitle("KAYIT GUNCELLEME")
            message_box.setText("Kayıt güncelleme işlemi başarılı bir şekilde gerçekleşti.")
            message_box.exec_()
        except Exception as Hata:
            message_box = QMessageBox()
            message_box.setWindowTitle("HATA")
            message_box.setText("Şöyle bir hata ile karşılaşıldı: " + str(Hata))
            message_box.exec_()
    else:
        message_box = QMessageBox()
        message_box.setWindowTitle("BİLGİ")
        message_box.setText("Güncelleme işlemi iptal edildi.")
        message_box.exec_()
        
    ui4.leISBN.clear()
    ui4.leKitapAdi.clear()
    ui4.leYazar.clear()
    ui4.leYayinevi.clear()
    ui4.leBasimYili.clear()
    ui4.comboDurum.setCurrentIndex(-1)
    ui4.leodunc.clear()
            
#%%
#--------------------------DOLDUR
def Doldur():
    secili = ui4.tableWidget.selectedItems()
    if len(secili) >= 7:
        ui4.leISBN.setText(secili[1].text())
        ui4.leKitapAdi.setText(secili[2].text())
        ui4.leYazar.setText(secili[3].text())
        ui4.leYayinevi.setText(secili[4].text())
        ui4.leBasimYili.setText(secili[5].text())
        ui4.comboDurum.setCurrentText(secili[6].text())
        ui4.leodunc.setText(secili[7].text())
    


#%%
#--------------------------PERSONEL_EKLE

def PersonelEkle():
    try:
        _lePersonelAd = ui4.lePersonelAd.text()
        _lePersonelSoyad = ui4.lePersonelSoyad.text()
        _lePerKullaniciAdi = ui4.lePerKullanciAdi.text()
        _lePersonelSifre = ui4.lePersonelSifre.text()

        curs1.execute("INSERT INTO personelListe (PersonelNo, Isim, Soyisim, PSifre) VALUES (?, ?, ?, ?)",
                  (_lePerKullaniciAdi, _lePersonelAd, _lePersonelSoyad, _lePersonelSifre))
        conn1.commit()
        message_box = QMessageBox()
        message_box.setWindowTitle("KAYIT GUNCELLEME")
        message_box.setText("Kayıt güncelleme işlemi başarılı bir şekilde gerçekleşti.")
        message_box.exec_()
    except Exception as Hata:
        message_box = QMessageBox()
        message_box.setWindowTitle("HATA")
        message_box.setText("Şöyle bir hata ile karşılaşıldı: " + str(Hata))
        message_box.exec_()
        
    ui4.lePersonelAd.clear()
    ui4.lePersonelSoyad.clear()
    ui4.lePerKullanciAdi.clear()
    ui4.lePersonelSifre.clear()



    
#%%
#----------------------SİNYAL-SLOT
ui.btnOgGiris.clicked.connect(GIRIS)
ui.btnOgKayitol.clicked.connect(KAYITOL)
ui.btnPersonelGiris.clicked.connect(PerEkrani)
ui4.btnKitapEkle.clicked.connect(KitapKayıt)
ui4.btnPersonelEkle.clicked.connect(PersonelEkle)
ui4.btnKitapSil.clicked.connect(SIL)
ui3.btnAra.clicked.connect(AraOgrenci)
ui4.btnKitapAra.clicked.connect(AraPersonel)
ui4.tableWidget.itemSelectionChanged.connect(Doldur)
ui4.btnKitapGuncelle.clicked.connect(GUNCELLE)
sys.exit(uygulama.exec_())