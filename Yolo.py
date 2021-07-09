from AIDetector_pytorch import Detector
from os import listdir
from operator import itemgetter
from time import mktime
from datetime import datetime
from numpy import zeros,float32,tile,set_printoptions,sqrt
import imutils
import cv2
import csv
import numpy as np
import time



def Yolo_detect(video_name, Tresult, matching, thresh=0.3):

    name = 'demo'
    det = Detector(thresh)

    cap = cv2.VideoCapture(video_name) ##输入视频路径
    fps = int(cap.get(5))
    print('fps:', fps)
    t = int(1000/fps)

    Start_stamp = Tresult[0]                  ##列表第0项为起始时间戳
    End_stamp = Tresult[1]                    ##列表第1项为结束时间戳
    CameraID = str(Tresult[2])                     ##列表第2项为摄像头编号
    video_framenumber = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print("video_framenumber：", video_framenumber)                           ##视频总帧数
    print("Start_stamp：", Start_stamp)
    print("End_stamp：", End_stamp)
    print("CameraID：", CameraID)

    videoWriter = None
    outimgs = []
 
    # with open("output/infor.csv", "a", newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #
    #     writer.writerow(["X", "Y", "Width", "Height", "Class", "ID", "Color", "Timestamp"])

    i = 1
    while True:

        # try:
        _, im = cap.read()

        if im is None:
            break
        Timestamp = (End_stamp - Start_stamp) / video_framenumber * i + Start_stamp

        # print("i:", i)
        i = i + 1
        # print("Timestamp：", Timestamp)
        # with open("output/infor.csv", "a", newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #
        #     writer.writerow([" ", " ", " ", " ", " ", " ", " ", Timestamp, CameraID])

        output_result = det.feedCap(im, matching, str(CameraID), Timestamp)
        output_result = output_result['frame']
        output_result = imutils.resize(output_result, height=500)
        outimgs.append(output_result)


        # if videoWriter is None:
        #     fourcc = cv2.VideoWriter_fourcc(
        #         'm', 'p', '4', 'v')  # opencv3.0
        #     videoWriter = cv2.VideoWriter(
        #         'result.mp4', fourcc, fps, (output_result.shape[1], output_result.shape[0]))
        #
        # videoWriter.write(output_result)
        # cv2.imshow(name, output_result)
        # cv2.waitKey(t)
        
        # if cv2.getWindowProperty(name, cv2.WND_PROP_AUTOSIZE) < 1:
        #     # 点x退出
        #     break
        # except Exception as e:
        #     print(e)
        #     break
    cap.release()
    # videoWriter.release()
    # cv2.destroyAllWindows()
    return outimgs
    

if __name__ == '__main__':
    pass

    # Yolo_detect()