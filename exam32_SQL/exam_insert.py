import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic # ui를 클래스로 바꿔준다.

form_window = uic.loadUiType('./user_insert.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self): # 버튼 누르는 함수 처리해 주는 곳
        super().__init__()
        self.setupUi(self)
        self.btn_insert.clicked.connect(self.btn_insert_slot)

    def btn_insert_slot(self):
        userID = self.le_userid.text()
        username = self.le_username.text()
        birthYear = self.le_birthyear.text()
        addr = self.le_addr.text()
        mobile = self.le_mobile.text()
        height = self.le_height.text()
        print(userID, username, birthYear, addr, mobile, height)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())