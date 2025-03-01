import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from g_menu import Ui_MainWindow

class menu (QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)     
        self.pushButton.clicked.connect(self.abrir_crm)
       
 
if __name__ == "__menu__":
    app=QApplication(sys.argv)
    window = menu()
    window.show()
    sys.exit(app.exec())
