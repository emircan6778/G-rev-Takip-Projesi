from PyQt5.QtWidgets import (QWidget, QApplication,QLineEdit, QPushButton, QFormLayout, QMessageBox)
from database import kullanicilar_col
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QRegExpValidator,QIntValidator
from PyQt5.QtCore import QRegExp
from boss_window import BossWindow
from worker_window import Gorevlerim

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Ekranı")
        self.resize(400, 400)

        form = QFormLayout()
        form.setContentsMargins(20, 20, 20, 10)
        form.setSpacing(20)

        
      
        self.username = QLineEdit()
        #QRegExpValidator() fonksiyonu içine yazılan kurala uymayan hiçbirşey yazılmayacak demek
        no_space_validator = QRegExpValidator(QRegExp("[^ ]+"))#Boşluk girilmesini engeller
        self.username.setValidator(no_space_validator)#username ye boşluk girilmesini engeller

        self.username.setPlaceholderText("Lütfen Kullanıcı adınızı giriniz")
        self.username.setFixedHeight(36)
        self.username.setMaxLength(12)
        self.username.setStyleSheet("""
            QLineEdit {
                border: 1px solid #aaa;
                border-radius: 12px;
                padding: 6px;
            }
        """)

        # Password
        self.password = QLineEdit()
        self.password.setPlaceholderText("Lütfen 6 Haneli Şifrenizi giriniz")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMaxLength(6)

        self.password.setValidator( QRegExpValidator(QRegExp(r"[0-9]+")))


        self.password.setFixedHeight(36)
        self.password.setStyleSheet("""
            QLineEdit {
                border: 1px solid #aaa;
                border-radius: 12px;
                padding: 6px;
            }
        """)

        # Login Button
        self.login_btn = QPushButton("Login")
        self.login_btn.setFixedHeight(35)
        
        
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #aaa;
                border-radius: 8px;
                padding: 6px;
                background-color: #ffffff;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
            QPushButton:pressed {
                background-color: #cccccc;
            }
        """)

        form.addRow("Kullanıcı Adı:", self.username)
        form.addRow("Şifre:", self.password)
        form.addRow("", self.login_btn)

        self.login_btn.clicked.connect(self.Kontrol)
        # kullanıcı adı ve şifre kutularına ekle
        self.username.returnPressed.connect(self.login_btn.click)
        self.password.returnPressed.connect(self.login_btn.click)


        self.setLayout(form)
    
    def Kontrol(self):
     username = self.username.text()
     pasword = self.password.text()

     kullanici = kullanicilar_col.find_one({"username": username})

     if kullanici:
         if kullanici["username"] == "admin" and kullanici["sifre"] == pasword:
             self.MyWindow = BossWindow()
             self.MyWindow.show()
             self.close() 
         elif kullanici["sifre"] == pasword:
              self.MyWindow = Gorevlerim(username)
              self.MyWindow.show()
              self.close()
         else:
             QMessageBox.warning(self, "Hata", "Şifre yanlış")
     else:
         QMessageBox.warning(self, "Hata", "Kullanıcı bulunamadı!")

