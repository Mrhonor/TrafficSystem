#-*- coding:utf-8 –*- #
'''
import部分强烈建议使用from xx import xx类
'''
from match.Matching import Matching
from match.YoloTransformer import YoloTransformer
from TimeStampRead import result, save_img
from Yolo import Yolo_detect
from GUI.gui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QDialog
from DataSQL import DataSQL
from GUI.dialog import LogDialog
from web.SendMsg import send_car_msg
import threading
import sys
import asyncio

window = None
# sql = DataSQL('root', 'P8rI6nc9e0.SQL', 'Mrhonor')
sql = None

def main_thread(event_loop):
    # global window, sql

    asyncio.set_event_loop(event_loop)
    sql.CreateWorldFrameTable()
    publisher = send_car_msg()
    transformer = YoloTransformer()
    transformer.UpdateIntrinsicAndExtrinsicFromFile('112', 'data/intrinsic_params_112.csv', 'data/extrinsic_params_112.csv')
    transformer.UpdateIntrinsicAndExtrinsicFromFile('115', 'data/intrinsic_params_115.csv', 'data/extrinsic_params_115.csv')
    Match = Matching(transformer, publisher, sql)

    trainingDigits = r'.\digits\trainingDigits'
    testDigits = r'.\digits\testDigits'

    # video_name1 = 'data/Camera112.mp4'
    # video_name2 = 'data/Camera115.mp4'

    '''
    模块一：从图像化界面获取输入
    '''
    while True:
        window.video_mutex.acquire()

        video_name1 = window.video1
        video_name2 = window.video2
        print (video_name1)
        print (video_name2)
        '''
        模块二：时间戳提取模块
        '''
        # video_pictures1 = None
        Tresult1 = None
        Tresult2 = None
        if video_name1:
            video_pictures1 = save_img(video_name1)
            Tresult1 = result(video_pictures1, trainingDigits, testDigits)  ##返回最终结果列表
        if video_name2:
            video_pictures2 = save_img(video_name2)
            Tresult2 = result(video_pictures2, trainingDigits, testDigits)  ##返回最终结果列表


        '''
        模块三：Yolo识别类
        识别结果视频, CameraID，标注数据信息 = xx.xx(cv_video类, CameraID，起始时间戳，末尾时间戳，总帧数)
        '''
        yolo_finsh_flag = False
        thresh_hold = window.splider.value()/100.0
        if Tresult1:
            out_imgs1 = Yolo_detect(video_name1, Tresult1, Match, thresh_hold)
            window.video_stream_A = out_imgs1
            yolo_finsh_flag = True
        if Tresult2:
            out_imgs2 = Yolo_detect(video_name2, Tresult2, Match, thresh_hold)
            window.video_stream_B = out_imgs2
            yolo_finsh_flag = True


        '''
        模块四: 可视化视频输出
        xx.xx(识别结果视频)
        '''
        # print (3)
        # window.video_show_mutex.release()
        # print (4)

        '''
        模块五：车辆匹配和坐标转换类。包含了经纬度转换模块
        '''
        if yolo_finsh_flag:
            window.open_flag_A = True
            window.open_flag_B = True
            window.showVideo()
            Match.DataProcess()
            # window.Button_D.setEnabled(True)




if __name__ == '__main__':
    '''
    程序运行主线程，顺序运行
    '''
    '''
    第一步：各个模块在此初始化   
    '''

    app = QApplication(sys.argv)
    dialog = LogDialog()
    if dialog.exec_() == QDialog.Accepted:
        loop = asyncio.new_event_loop()
        sql = DataSQL(str(dialog.lineEdit_host.text()), str(dialog.lineEdit_account.text()), str(dialog.lineEdit_password.text()), str(dialog.lineEdit_name.text()))
        window = Ui_MainWindow(sql)
        main_th = threading.Thread(target=main_thread, args=(loop,))
        main_th.setDaemon(True)
        main_th.start()
        window.show()
        sys.exit(app.exec_())





