from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from login_window import Login


def main():
    app = QApplication([])
    window = Login()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()