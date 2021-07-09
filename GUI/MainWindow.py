from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import *  # 导入浏览器的包
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication ,QWidget, QVBoxLayout , QHBoxLayout  ,QPushButton
# from PyQt5.QtMultimediaWidgets import QVideoWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        # todo 这一段是浏览器控件代码
        self.webView = QWebEngineView(self.centralwidget)
    
        # 设置浏览器的默认地址
        self.webView.setUrl(QtCore.QUrl("http://8.135.22.92/digitaltwin/"))  

        self.widgetA = QtWidgets.QWidget(self.centralwidget)
        self.widgetA.setObjectName("widgetA")
        self.img_labelA = QtWidgets.QLabel(self.widgetA)
        self.img_labelA.setObjectName("img_labelA")
        self.widgetB = QtWidgets.QWidget(self.centralwidget)
        self.widgetB.setObjectName("widgetB")
        self.img_labelB = QtWidgets.QLabel(self.widgetB)
        self.img_labelB.setObjectName("img_labelB")

        self.img_labelC = QtWidgets.QLabel(self)
        self.img_labelC.setObjectName("img_labelC")
        
        # 选择文件的按钮
        self.Button_A = QPushButton(self)
        self.Button_A.setObjectName("Button A")
        self.Button_A.setText("相机A")
        self.Button_A.clicked.connect(self.folder_A)
        self.Button_B = QPushButton(self)
        self.Button_B.setObjectName("Button B")
        self.Button_B.setText("相机B")
        self.Button_B.clicked.connect(self.folder_B)

        # 开始运行的按钮
        self.Button_C = QPushButton(self)
        self.Button_C.setObjectName("Button C")
        self.Button_C.setText("开始运行")
        self.Button_C.clicked.connect(self.start_run)
        self.Button_C.setEnabled(False)

        # 输出csv文件的按钮
        self.Button_D = QPushButton(self)
        self.Button_D.setObjectName("Button D")
        self.Button_D.setText("导出数据")
        self.Button_D.clicked.connect(self.out_csv)
        # self.Button_D.setEnabled(False)

        # 设置滑动条
        # 获取数据方法 self.splider.value()
        self.splider = QSlider(QtCore.Qt.Horizontal, self)
        self.splider.setMinimum(0)  # 最小值
        self.splider.setMaximum(100)  # 最大值
        self.splider.setSingleStep(5)  # 步长
        self.splider.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.splider.setTickInterval(10)  # 设置刻度间隔
        # self.splider.valueChanged.connect(self.changeValue)
        self.splider.setValue(25)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.img_labelA.setText(_translate("MainWindow", "    视频播放区域"))
        self.img_labelB.setText(_translate("MainWindow", "    视频播放区域"))
        self.img_labelC.setText(_translate("MainWindow", "置信度阈值"))

    def resizeEvent(self,event):
        # print(event.size().width(),event.size().height())
        # (以左上角为原点的x轴坐标, y轴坐标, 控件的宽度, 控件的高度)
        self.widgetB.setGeometry(QtCore.QRect(0, 0, event.size().width()/2, event.size().height()/2))
        self.widgetA.setGeometry(QtCore.QRect(0, event.size().height()/2, event.size().width()/2, event.size().height()/2 ))
        self.img_labelA.setGeometry(QtCore.QRect(0, 0, event.size().width()/2, event.size().height()/2 ))
        self.webView.setGeometry(QtCore.QRect(event.size().width()/2, 0, event.size().width()/2, event.size().height()/2 ))
        self.img_labelB.setGeometry(QtCore.QRect(0, 0, event.size().width()/2, event.size().height()/2 ))
        self.Button_A.setGeometry(event.size().width()*2/3, event.size().height()*2/3, event.size().width()/12, event.size().width()/24)
        self.Button_B.setGeometry(event.size().width()*3/4, event.size().height()*2/3, event.size().width()/12, event.size().width()/24)
        self.Button_C.setGeometry(event.size().width()*0.85, event.size().height()*2/3, event.size().width()/12, event.size().width()/24)
        self.Button_D.setGeometry(event.size().width()*0.85, event.size().height()*0.8, event.size().width()/12, event.size().width()/24)
        self.splider.setGeometry(event.size().width()*2/3, event.size().height()*0.8, event.size().width()*0.15, event.size().width()/24)
        self.img_labelC.setGeometry(event.size().width()*0.55, event.size().height()*0.8, event.size().width()*0.1, event.size().width()/24)
        width = int(event.size().width()/2)
        height = int(event.size().height()/2)
        global dim
        dim = (width,height)