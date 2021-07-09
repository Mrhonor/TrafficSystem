import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog
from GUI import MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from PyQt5.QtMultimedia import *
# from PyQt5.QtMultimediaWidgets import *

import cv2
import time
import asyncio
import threading



class Ui_MainWindow(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, SQL=None):
        QMainWindow.__init__(self)
        MainWindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.open_flag_A=False
        self.open_flag_B=False

        self.video_stream_A=None
        self.video_stream_B=None

        self.video_mutex = threading.Semaphore(0)
        self.video_show_mutex = threading.Semaphore(0)
        self.video1 = None
        self.video2 = None

        self.painter = QPainter(self)
        self.select_file = ""

        self.sql = SQL

    def folder_A(self):
        # 相机A选中文件
        # directory = QFileDialog.getExistingDirectory(self, "Open Folder", "D:\Workspace")
        directory = QFileDialog.getOpenFileName(self, "Open Folder", "C:\\")

        self.select_file = directory
        if not (directory[0].endswith('.avi') or  directory[0].endswith('.flv') or directory[0].endswith('.mp4')):
            QMessageBox.warning(self, "警告", "请选择正确的视频文件（avi、flv、mp4）", QMessageBox.Cancel)
            return
        self.video1 = directory[0]
        # self.video_stream_A=cv2.VideoCapture(directory[0])
        self.Button_C.setEnabled(True)


    def folder_B(self):
        # 相机B选中文件
        # directory = QFileDialog.getExistingDirectory(self, "Open Folder", "D:\Workspace")
        directory = QFileDialog.getOpenFileName(self, "Open Folder", "C:\\")

        self.select_file = directory
        if not (directory[0].endswith('.avi') or  directory[0].endswith('.flv') or directory[0].endswith('.mp4')):
            QMessageBox.warning(self, "警告", "请选择正确的视频文件（avi、flv、mp4）", QMessageBox.Cancel)
            return
        self.video2 = directory[0]
        # self.video_stream_B=cv2.VideoCapture(directory[0])
        self.Button_C.setEnabled(True)

    def start_run(self):
        self.Button_C.setEnabled(False)
        self.Button_A.setEnabled(False)
        self.Button_B.setEnabled(False)
        self.video_mutex.release()
        QMessageBox.information(self, "开始运行", "根据视频长短需要不同的计算时间，请耐心等候",
                                QMessageBox.Yes)

        # self.video_show_mutex.acquire()
        # print (13)
        # self.open_flag_A = True
        # self.open_flag_B = True

    def out_csv(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "C:/")
        # print (directory)
        if self.sql:
            try:
                self.sql.OutputWorldFrameTable(directory)
                QMessageBox.information(self, "导出数据", "导出csv文件在所选文件夹下",
                                    QMessageBox.Yes)
            except:
                QMessageBox.warning(self, "警告", '''操作非法。可能原因：
                1.没有数据；
                2. 权限受限；
                3. 数据库导入导出限制''', QMessageBox.Cancel)
        else:
            QMessageBox.warning(self, "警告", "数据库没有成功运行", QMessageBox.Cancel)
        # return

    # def changeValue(self, value):
    #     print(value)/100

    def showVideo(self):
        if self.open_flag_A:
            asyncio.get_event_loop().run_until_complete(self.read_videostream_A())
        if self.open_flag_B:
            asyncio.get_event_loop().run_until_complete(self.read_videostream_B())

    def compute(self):
        pass
    
        '''
        def on_video(self):
                    if self.open_flag:
                        self.pushButton.setText('open')
                    else:
                        
                        self.pushButton.setText('close')
                    self.open_flag = bool(1-self.open_flag)#
        '''
    
    def paintEvent(self, a0: QPaintEvent):
        if self.open_flag_A:
            asyncio.get_event_loop().run_until_complete(self.read_videostream_A())
        if self.open_flag_B:
            asyncio.get_event_loop().run_until_complete(self.read_videostream_B())

    # def closeEvent(self, event):
    #     # isClose = True
    #     video_mutex.release()
    #     sys.exit(0)

    async def read_videostream_A(self):
        # 按下A按钮
            try:
                # 读入视频流A
                # retA, frame_A = self.video_stream_A.read()

                # if retA:
                frame_A = self.video_stream_A.pop(0)
                time.sleep(0.02)
                # frame_A=cv2.resize(frame_A,(windows.event.size().width()/2,windows.event.size().height()/2),interpolation=cv2.INTER_AREA)
                frame_A=cv2.resize(frame_A,MainWindow.dim,interpolation=cv2.INTER_AREA)
                frame_A=cv2.cvtColor(frame_A,cv2.COLOR_BGR2RGB)
                #cv2.imshow('test',frame_A)
                #cv2.waitKey(10)
                self.Qframe_A=QImage(frame_A.data,frame_A.shape[1],frame_A.shape[0],frame_A.shape[1]*3,QImage.Format_RGB888)
                #print(Qframe_A)
                #pix = QPixmap(Qframe_A).scaled(frame_A.shape[1], frame_A.shape[0])
                #self.setPixmap(pix)
                #QRect qq(20,50,self.img.width,self.img.height)
                self.img_labelA.setPixmap(QPixmap.fromImage(self.Qframe_A))
                #self.painter.drawImage(QPoint(20,50),Qframe_A)
                #print(Qframe_A)
                self.update()
            except:
                self.open_flag_A = False
                self.video1 = None
                if self.open_flag_B is False:
                    self.Button_A.setEnabled(True)
                    self.Button_B.setEnabled(True)

                # self.video_finish_mutex.release()
                # print("未打开相机A")


    
    async def read_videostream_B(self):
        # 按下B按钮
            try:
                # 读入视频B
                # retB, frame_B = self.video_stream_B.read()
                #
                # if retB:
                frame_B = self.video_stream_B.pop(0)
                time.sleep(0.02)
                frame_B=cv2.resize(frame_B,MainWindow.dim,interpolation=cv2.INTER_AREA)
                frame_B=cv2.cvtColor(frame_B,cv2.COLOR_BGR2RGB)
                #cv2.imshow('test',frame_B)
                #cv2.waitKey(10)
                self.Qframe_B=QImage(frame_B.data,frame_B.shape[1],frame_B.shape[0],frame_B.shape[1]*3,QImage.Format_RGB888)
                #print(Qframe_B)
                #pix = QPixmap(Qframe_B).scaled(frame_B.shape[1], frame_B.shape[0])
                #self.setPixmap(pix)
                #QRect qq(20,50,self.img.width,self.img.height)
                self.img_labelB.setPixmap(QPixmap.fromImage(self.Qframe_B))
                #self.painter.drawImage(QPoint(20,50),Qframe_B)
                #print(Qframe_B)
                self.update()
            except:
                self.open_flag_B = False
                self.video2 = None
                if self.open_flag_A is False:
                    self.Button_A.setEnabled(True)
                    self.Button_B.setEnabled(True)
                # self.video_finish_mutex.release()
                # print("未打开相机B")
            


# if __name__ == '__main__':
#     start_gui()
