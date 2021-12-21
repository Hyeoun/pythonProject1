import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic # ui를 클래스로 바꿔준다.
import pymysql

form_window = uic.loadUiType('./user_insert.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self): # 버튼 누르는 함수 처리해 주는 곳
        super().__init__()
        self.setupUi(self)
        self.btn_insert.clicked.connect(self.btn_insert_slot)
        self.le_userid.setMaxLength(8)  # 글자수 제한
        self.le_username.setMaxLength(10)

    def btn_insert_slot(self):
        userID, username, birthYear, addr, mobile, height = None, None, None, None, None, None
        userID = self.le_userid.text()
        # if len(userID) > 8:
        #     self.le_userid.setText('')
        #     userID = None
        username = self.le_username.text()
        # if len(username) > 10:
        #     self.le_username.setText('')
        #     username = None
        birthYear = self.le_birthyear.text()
        try:
            birthYear = int(birthYear)
        except:
            self.le_username.setText('')
            birthYear = None
        addr = self.le_addr.text()
        if len(addr) > 2:
            self.le_addr.setText('')
            addr = None
        mobile = '"{}"'.format(self.le_mobile.text())
        if mobile == '""': mobile = 'null'
        if len(mobile) > 10:
            self.le_mobile.setText('')
            mobile = None
        height = self.le_height.text()
        if height == '': height = 'null'
        try:
            if height != 'null':
                height = int(height)
        except:
            self.le_height.setText('')
            height = None
        if userID != None and username != None and birthYear != None and addr != None and mobile != None and height != None:
            sql = 'insert into membertbl value("{}", "{}", {}, "{}", {}, {});'.format(userID, username, birthYear, addr, mobile, height)
            print(sql)
            if not self.insert(sql):
                print('conn success')


    def insert(self, sql):
        conn = pymysql.connect(
            user='root',
            passwd='1q2w3e4r',
            host='127.0.0.1',
            port=3306,
            db='shopdb',
            charset='utf8'
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
            conn.commit()
        except:
            print('conn error')
        finally:
            conn.close()
        return 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())