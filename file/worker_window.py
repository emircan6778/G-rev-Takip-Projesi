from PyQt5.QtWidgets import  QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QMessageBox, QTabWidget, QLineEdit, QPushButton, QFormLayout
from PyQt5.QtCore import Qt
from database import gorev, kullanicilar_col 
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

class Gorevlerim(QWidget):
    def __init__(self, username):
        super().__init__()
        self.resize(500, 500)
        self.setWindowTitle("Çalışan Ekranı")
        self.username = username
        main_layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        self.gorev_tab = QWidget()
        self.gorev_layout = QVBoxLayout(self.gorev_tab)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Görevler")
        self.gorev_layout.addWidget(self.tree)

        self.tamamlanmis = QTreeWidgetItem(self.tree)
        self.tamamlanmis.setText(0, "Tamamlanmış Görevler")

        self.tamamlanmamis = QTreeWidgetItem(self.tree)#parantez içine ne yazılırsa oluşan nesne onun çocuğu olur.Ağaç yapısı bunu sağlar.
        self.tamamlanmamis.setText(0, "Tamamlanmamış Görevler")

        self.tree.itemClicked.connect(self.tiklandi)#Bu sinyal kullanıcı bir item’a tıkladığı anda çalışır.
        self.tree.itemChanged.connect(self.gorev_checkbox_degisti)#Bu sinyal item’ın verisi değiştiğinde çalışır.

        
        self.gorev_yukle(True)
        self.gorev_yukle(False)

        self.tabs.addTab(self.gorev_tab, "Görevler")

       
        self.sifre_tab = QWidget()
        self.sifre_layout = QFormLayout(self.sifre_tab)

        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.sifre_input.setPlaceholderText("Yeni şifrenizi girin")
        self.sifre_input.setMaxLength(6)
        self.sifre_input.setValidator(QRegExpValidator(QRegExp(r"[0-9]+")))

        self.sifre_button = QPushButton("Şifreyi Değiştir")
        self.sifre_button.clicked.connect(self.sifre_degistir)

        self.sifre_layout.addRow("Yeni Şifre:", self.sifre_input)
        self.sifre_layout.addWidget(self.sifre_button)

        self.tabs.addTab(self.sifre_tab, "Şifre Değiştir")

    
    def tiklandi(self, item, column):
        if item == self.tamamlanmis:
            self.gorev_yukle(True)
        if item == self.tamamlanmamis:
            self.gorev_yukle(False)

    def gorev_yukle(self, durum):
        parent = self.tamamlanmis if durum else self.tamamlanmamis#durum true ise tamamlanmışın altına eklicek
        parent.takeChildren()#Bu satır o başlığın altındaki tüm eski görevleri siliyor.
        for g in gorev.find({"username": self.username, "is_done": durum}):
            item = QTreeWidgetItem(parent)
            item.setText(0, g["title"])#Görev başlığı ağacın 0. kolonuna yazılıyor.
            if not durum:#Eğer görev tamamlanmamışsa bu görevi işaretlenebilir hale getiriyor.
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(0, Qt.Unchecked)

    def gorev_checkbox_degisti(self, item, column):
        if item.parent() == self.tamamlanmamis and item.checkState(0) == Qt.Checked:#Burda 2 koşul var Görev tamamlanmamış görevler
            gorev.update_one(
                {"username": self.username, "title": item.text(0)},
                {"$set": {"boss_notify": True}}
            )
            QMessageBox.information(self, "Bildirim", "Görev işverene bildirildi!")

  
    def sifre_degistir(self):
        yeni_sifre = self.sifre_input.text().strip()
        if not yeni_sifre:
            QMessageBox.warning(self, "Hata", "Lütfen yeni şifre giriniz!")
            return
        kullanicilar_col.update_one(
            {"username": self.username},
            {"$set": {"sifre": yeni_sifre}}
        )
        QMessageBox.information(self, "Başarılı", "Şifreniz başarıyla değiştirildi!")
        self.sifre_input.clear()
