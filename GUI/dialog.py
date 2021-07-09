import sys
from PyQt5 import QtWidgets, QtCore, QtGui

class LogDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('数据库登录')
        self.resize(400, 400)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.frame = QtWidgets.QFrame(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)

        self.lineEdit_host = QtWidgets.QLineEdit()
        self.lineEdit_host.setPlaceholderText("请输入数据库host:")
        self.verticalLayout.addWidget(self.lineEdit_host)

        self.lineEdit_account = QtWidgets.QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入数据库账号:")
        self.verticalLayout.addWidget(self.lineEdit_account)

        self.lineEdit_password = QtWidgets.QLineEdit()
        self.lineEdit_password.setPlaceholderText("请输入数据库密码:")
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.lineEdit_name = QtWidgets.QLineEdit()
        self.lineEdit_name.setPlaceholderText("请输入数据库名字:")
        self.verticalLayout.addWidget(self.lineEdit_name)

        self.pushButton_enter = QtWidgets.QPushButton()
        self.pushButton_enter.setText("确定")
        self.verticalLayout.addWidget(self.pushButton_enter)
        self.pushButton_enter.clicked.connect(self.Check)

        self.pushButton_quit = QtWidgets.QPushButton()
        self.pushButton_quit.setText("取消")
        self.verticalLayout.addWidget(self.pushButton_quit)
        self.pushButton_quit.clicked.connect(QtCore.QCoreApplication.instance().quit)

    def Check(self):
        self.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = LogDialog()
    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        print(dialog.lineEdit_account.text())
        print(dialog.lineEdit_password.text())

