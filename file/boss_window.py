from PyQt5.QtWidgets import QWidget, QApplication,QLineEdit, QPushButton, QFormLayout, QMessageBox,QTabWidget,QVBoxLayout,QLabel,QListWidget,QHBoxLayout
from PyQt5.QtCore import Qt,QRegularExpression
from PyQt5.QtGui import QRegExpValidator,QIntValidator,QRegularExpressionValidator
from PyQt5.QtCore import QRegExp
from database import kullanicilar_col,gorev

class Ekle(QWidget):
    def __init__(self,boss_window):
        super().__init__()
     #s
        self.vbox = QFormLayout()
        self.text_edit = QLineEdit()
        self.text_edit2 = QLineEdit()
        self.but1 = QPushButton("Giriş")

        regex = QRegularExpression(r"[0-9]{1,11}")#Burada Sadece 1 ile 11 basamakları arasında sadece rakamlardan oluşan sayı girilmesini sağlayan nesneyi oluşturuyorum
        validator = QRegularExpressionValidator(regex)
        nospace = QRegExpValidator(QRegExp("[^ ]+"))#Burda klavyeden boşluk girilmesini engelliyorum

        self.vbox.setContentsMargins(50, 50, 50, 70)
        self.vbox.setSpacing(20)
        self.but1.setStyleSheet("""
            QPushButton {
                border: 1px solid #aaa;
                border-radius: 8px;
                padding: 6px;
                background-color: #ffffff;
            }
            QPushButton:hover { background-color: #e6e6e6; }
            QPushButton:pressed { background-color: #cccccc; }
        """)
        self.but1.setFixedHeight(35)
        self.but1.setMaximumWidth(100)

        self.text_edit.setValidator(nospace)
        self.text_edit2.setValidator(nospace)
        self.text_edit2.setValidator(validator)

        self.text_edit.setMaxLength(12)
        self.text_edit2.setMaxLength(11)
        self.text_edit.setFixedHeight(34)
        self.text_edit2.setFixedHeight(34)

        self.text_edit.setStyleSheet("border: 1px solid #aaa; border-radius: 12px; padding: 6px;")
        self.text_edit2.setStyleSheet("border: 1px solid #aaa; border-radius: 12px; padding: 6px;")

        self.text_edit.setPlaceholderText("Lütfen eklenmek istenen çalışanın kullanıcı adını giriniz")
        self.text_edit2.setPlaceholderText("Lütfen Eklenmek istenen çalışanın TC kimliğini giriniz")

        self.vbox.addRow("Kullanıcı adı:", self.text_edit)
        self.vbox.addRow("TC kimlik numarası:", self.text_edit2)
        self.vbox.addWidget(self.but1)
        self.but1.clicked.connect(self.kullanici_Ekle)
        self.setLayout(self.vbox)
        self.boss_window = boss_window 

        

    def kullanici_Ekle(self):
        username = self.text_edit.text()
        tc = self.text_edit2.text()

        if not username or not tc:#Kullanıcı kimlik veya kullanıcı adından herhangi birini girmezse hata mesajı alsın
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurunuz")
            return

        var_mi = kullanicilar_col.find_one({"username": username})#Bu username i sağlayan ilk kullanıcıyı veri tabanından getir demek eğer sadece find kullansaydık o username e sahip tüm kullanıcıları listeler.
        if var_mi:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı zaten kayıtlı!")
            return

        kullanici = {"username": username, "tc": tc, "sifre": "123456"}
        kullanicilar_col.insert_one(kullanici)
        QMessageBox.information(self, "Başarılı", f"{username} başarıyla eklendi!")
        self.text_edit.clear()#Burada kullanıcıyı ekledikten sonra Lineedit yapısının içeriğini temizliyorum
        self.text_edit2.clear()
        self.boss_window.gorevler.yenile()
        
        
        

class Gorevler(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Görev Listesi")
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row1.addLayout(self.col1)
        self.row1.addLayout(self.col2)
        self.setLayout(self.row1)

        self.text_List = QListWidget()
        self.col1.addWidget(self.text_List)
        for item in self.get_username():
            self.text_List.addItem(item)

        self.text_List2 = QListWidget()
        self.col2.addWidget(self.text_List2)
       

        self.text_List.itemClicked.connect(self.kullanici_secildi)

    def kullanici_secildi(self, item):
        kisi = item.text()
        self.text_List2.clear()
        dok = gorev.find({"username": kisi})
        for d in dok:
            durum = "Görev tamamlandı" if d["is_done"] else "Görev tamamlanmadı"
            text = f'{d["title"]} - {durum}'
            self.text_List2.addItem(text)

    def get_username(self):
        return [kul["username"] for kul in kullanicilar_col.find({}, {"username": 1, "_id": 0})]
    def yenile(self):
     #Bu fonksiyonumun amacı sekmeler arasında geçiş yaptığımda otomatik güncelleme yapması
     self.text_List.clear()
     for item in self.get_username():
        self.text_List.addItem(item)


class Bildirimler(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bildirimler")
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row1.addLayout(self.col1)
        self.row1.addLayout(self.col2)
        self.setLayout(self.row1)

        self.text_list = QListWidget()
        self.col1.addWidget(self.text_list)

        self.text_button = QPushButton("Onayla")
        self.text_button.setStyleSheet("background-color: green; color: white;")
        self.text_button.setFixedHeight(32)

        self.text_button2 = QPushButton("Reddet")
        self.text_button2.setStyleSheet("background-color: red; color: white;")
        self.text_button2.setFixedHeight(32)

        self.col2.addWidget(self.text_button)
        self.col2.addWidget(self.text_button2)
        self.col2.setAlignment(Qt.AlignVCenter)#Dikeyde ortalıyor.
        self.col2.setSpacing(6)
        self.col2.setContentsMargins(0, 0, 0, 0)

        self.text_button.clicked.connect(self.onayla_buton)
        self.text_button2.clicked.connect(self.reddet_buton)

        self.bildirimleri_goster()

    def bildirimleri_goster(self):
        self.text_list.clear()
        for g in gorev.find({"boss_notify": True}):
            display_text = f'{g["title"]} - {g["username"]}'
            self.text_list.addItem(display_text)

    def onayla_buton(self):
        secilen = self.text_list.currentItem()#Listede şu an seçili olan satırı alıyor
        if secilen:
            try:
                title, username = secilen.text().split(" - ")
                gorev.update_one(
                    {"username": username, "title": title},
                    {"$set": {"is_done": True, "boss_notify": False}}
                )
                self.bildirimleri_goster()
            except Exception:
               QMessageBox.warning(self, "Hata", "Görev işlenemedi")


    def reddet_buton(self):
        secilen = self.text_list.currentItem()
        if secilen:
            try:
                title, username = secilen.text().split(" - ")
                gorev.update_one(
                    {"username": username, "title": title},
                    {"$set": {"boss_notify": False}}
                )
                self.bildirimleri_goster()
            except Exception as e:
                print("Hata:", e)

class Gorevekle(QWidget):
    def __init__(self,boss_window):
        super().__init__()
        self.boss_window=boss_window
        self.lay1 = QVBoxLayout(self)
        self.text_form = QFormLayout()
        self.lay1.addLayout(self.text_form)
        self.setLayout(self.lay1)

        self.text_line = QLineEdit()
        self.text_line2 = QLineEdit()
        self.text_form.addRow("Görev Açıklaması", self.text_line)
        self.text_form.addRow("Gönderilen çalışanın kullanıcı adı", self.text_line2)

        self.text_line.setStyleSheet("""QLineEdit { border: 1px solid #aaa; border-radius: 12px; padding: 6px; }""")
        self.text_line2.setStyleSheet("""QLineEdit { border: 1px solid #aaa; border-radius: 12px; padding: 6px; }""") 

        self.gonder_button = QPushButton("Gönder")
        self.text_form.setContentsMargins(50,50,50,50)
        self.text_form.setSpacing(20)
        self.text_line.setPlaceholderText("Lütfen görev açıklamasını giriniz")
        self.text_line2.setPlaceholderText("Lütfen kullanıcı adını giriniz")
        self.text_form.addWidget(self.gonder_button)
        self.gonder_button.setStyleSheet("""
            QPushButton {
                border: 1px solid #aaa;
                border-radius: 8px;
                padding: 6px;
                background-color: #ffffff;
            }
            QPushButton:hover { background-color: #e6e6e6; }
            QPushButton:pressed { background-color: #cccccc; }
        """)
        self.gonder_button.clicked.connect(self.gorev_gonder)

    def gorev_gonder(self):
        title = self.text_line.text().strip()
        username = self.text_line2.text().strip()

        if not title or not username:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurunuz")
            return


        var_mi = kullanicilar_col.find_one({"username": username})
        if not var_mi:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı bulunamadı!")
            return


        gorev.insert_one({
            "title": title,
            "username": username,
            "is_done": False,
            "boss_notify": False
        })
        QMessageBox.information(self, "Başarılı", f"{username} için görev başarıyla eklendi!")

        self.boss_window.gorevler.yenile()
        self.text_line.clear()
        self.text_line2.clear()
class Kullanicisil(QWidget):
    def __init__(self, boss_window):  # BossWindow referansı parametre olarak alındı
        super().__init__()
        self.boss_window = boss_window  # sakla

        self.text_form = QFormLayout()
        self.text_edit = QLineEdit()
        self.setLayout(self.text_form)

        self.text_form.addRow(
            "Silinmek istenen kullanıcının kullanıcı adını giriniz",
            self.text_edit
        )

        self.button = QPushButton("Sil")
        self.text_form.addWidget(self.button)
        self.button.clicked.connect(self.Kullaniciyisil)

    def Kullaniciyisil(self):
        username = self.text_edit.text()
        if not username:
            QMessageBox.warning(self,"Hata","Lütfen bir kullanıcı adı giriniz")
            return

        # Görevleri ve kullanıcıyı sil
        gorev.delete_many({"username": username})
        kullanicilar_col.delete_one({"username": username})
        QMessageBox.information(self,"Başarıyla tamamlandı",f"{username} silindi")
        self.text_edit.clear()

        # Görevler penceresini güncelle
        self.boss_window.gorevler.yenile()

class BossWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yönetici Ekranı")
        self.resize(600, 500)
        self.Vlayout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Görevler penceresini kaydet
        self.gorevler = Gorevler()
        self.tabs.addTab(Ekle(self), "Kullanıcı Ekle")
        self.tabs.addTab(self.gorevler, "Görevler")
        self.tabs.addTab(Gorevekle(self), "Görev ekle")
        self.tabs.addTab(Bildirimler(), "Bildirimler")

        # Kullanicisil widget’ına BossWindow referansı gönder
        self.tabs.addTab(Kullanicisil(self), "Kullanıcı sil")

        self.Vlayout.addWidget(self.tabs)
        self.setLayout(self.Vlayout)
