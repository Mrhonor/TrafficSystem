from cv2 import cv2
from os import listdir
from operator import itemgetter
from time import mktime
from datetime import datetime
from numpy import zeros,float32,tile,set_printoptions,sqrt,array


def save_img(video_path): ##视频抽帧并存储

    global video_framenumber
    video_capture = cv2.VideoCapture(video_path)
    video_framenumber = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))  ##计算视频总帧数
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))              ##获取视频宽度
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))            ##获取视频高度
    success, frame = video_capture.read()
    video_pictures = []
    for i in range(video_framenumber):  ##保存前25帧图像
        if(i<25):
            ret, frame = video_capture.retrieve()  ##解码此帧图像
            video_pictures.append(frame)
        if(i>=video_framenumber-25):   ##保存后25帧图像
            ret, frame = video_capture.retrieve()
            video_pictures.append(frame)
        ret = video_capture.grab()  ##读取下一帧图像，但不解码
    video_pictures.append(width)
    return video_pictures

def read_file(doc_name):  ## 定义一个把32x32格式转为1行的函数
    data = zeros((1, 1024))
    f = open(doc_name)
    for i in range(32):
        hang = f.readline()
        for j in range(32):
            data[0, 32 * i + j] = int(hang[j])
    return data

def translate(doc_name):   ##将32*32 numpy数组转换为1024行
    data = zeros((1, 1024))
    for i in range(32):
        for j in range(32):
            data[0, 32 * i + j] = doc_name[i][j]
    return data

def img_predeal_(img):     ##视频分辨率为2560x1440的图像数字像素位置截取及图像预处理

    lower_red = array([218, 218, 222])        ##设置lower_red,图像中低于lower_red，像素值变为0
    upper_red = array([255, 255, 255])        ##设置upper_red,图像中高于upper_red，像素值变为0
    img = cv2.inRange(img, lower_red, upper_red)
    img = img.astype(float32) / 255                                   ##图像归一化
    img_ = [0 for x in range(0, 17)]

    img0 = img[60:130, 1930:1965]                                     ##数字像素位置截取
    img0 = cv2.resize(img0, (32, 32), interpolation=cv2.INTER_NEAREST)##修改截取图像大小为32x32
    img0 = translate(img0)                                            ##将32x32的numpy array转换为1x1024
    img_[0] = img0                                                    ##存储在返回list中

    img1 = img[60:130, 1962:1998]
    img1 = cv2.resize(img1, (32, 32), interpolation=cv2.INTER_NEAREST)
    img1 = translate(img1)
    img_[1] = img1

    img2 = img[60:130, 1995:2030]
    img2 = cv2.resize(img2, (32, 32), interpolation=cv2.INTER_NEAREST)
    img2 = translate(img2)
    img_[2] = img2

    img3 = img[60:130, 2030:2062]
    img3 = cv2.resize(img3, (32, 32), interpolation=cv2.INTER_NEAREST)
    img3 = translate(img3)
    img_[3] = img3

    img4 = img[60:130, 2078:2113]
    img4 = cv2.resize(img4, (32, 32), interpolation=cv2.INTER_NEAREST)
    img4 = translate(img4)
    img_[4] = img4

    img5 = img[60:130, 2109:2145]
    img5 = cv2.resize(img5, (32, 32), interpolation=cv2.INTER_NEAREST)
    img5 = translate(img5)
    img_[5] = img5

    img6 = img[60:130, 2162:2198]
    img6 = cv2.resize(img6, (32, 32), interpolation=cv2.INTER_NEAREST)
    img6 = translate(img6)
    img_[6] = img6

    img7 = img[60:130, 2194:2229]
    img7 = cv2.resize(img7, (32, 32), interpolation=cv2.INTER_NEAREST)

    img7 = translate(img7)
    img_[7] = img7

    img8 = img[60:130, 2243:2278]
    img8 = cv2.resize(img8, (32, 32), interpolation=cv2.INTER_NEAREST)
    img8 = translate(img8)
    img_[8] = img8

    img9 = img[60:130, 2273:2308]
    img9 = cv2.resize(img9, (32, 32), interpolation=cv2.INTER_NEAREST)
    img9 = translate(img9)
    img_[9] = img9

    img10 = img[60:130, 2323:2358]
    img10 = cv2.resize(img10, (32, 32), interpolation=cv2.INTER_NEAREST)
    img10 = translate(img10)
    img_[10] = img10

    img11 = img[60:130, 2352:2387]
    img11 = cv2.resize(img11, (32, 32), interpolation=cv2.INTER_NEAREST)
    img11 = translate(img11)
    img_[11] = img11

    img12 = img[60:130, 2398:2434]
    img12 = cv2.resize(img12, (32, 32), interpolation=cv2.INTER_NEAREST)
    img12 = translate(img12)
    img_[12] = img12

    img13 = img[60:130, 2430:2466]
    img13 = cv2.resize(img13, (32, 32), interpolation=cv2.INTER_NEAREST)
    img13 = translate(img13)
    img_[13] = img13

    img14 = img[1330:1400, 80:115]
    img14 = cv2.resize(img14, (32, 32), interpolation=cv2.INTER_NEAREST)
    img14 = translate(img14)
    img_[14] = img14

    img15 = img[1330:1400, 115:145]
    img15 = cv2.resize(img15, (32, 32), interpolation=cv2.INTER_NEAREST)
    img15 = translate(img15)
    img_[15] = img15

    img16 = img[1330:1400, 140:180]
    img16 = cv2.resize(img16, (32, 32), interpolation=cv2.INTER_NEAREST)
    img16 = translate(img16)
    img_[16] = img16

    set_printoptions(suppress=True)
    set_printoptions(precision=3)
    return img_


def img_predeal(img):    ##视频分辨率为1280x720的图像数字像素位置截取及图像预处理

    lower_red = array([218, 218, 222])        ##设置lower_red,图像中低于lower_red，像素值变为0
    upper_red = array([255, 255, 255])        ##设置upper_red,图像中高于upper_red，像素值变为0
    img = cv2.inRange(img, lower_red, upper_red)


    retval, img = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY)
    img = img.astype(float32) / 255  ##图像归一化
    img_ = [0 for x in range(0, 17)]

    img0 = img[30:60, 956:975]  ##数字像素位置截取
    img0 = cv2.resize(img0, (32, 32), interpolation=cv2.INTER_NEAREST)  ##修改截取图像大小为32x32
    img0 = translate(img0)
    img_[0] = img0  ##存储在返回list中

    img1 = img[30:60, 972:991]
    img1 = cv2.resize(img1, (32, 32), interpolation=cv2.INTER_NEAREST)
    img1 = translate(img1)
    img_[1] = img1

    img2 = img[30:60, 988:1007]
    img2 = cv2.resize(img2, (32, 32), interpolation=cv2.INTER_NEAREST)
    img2 = translate(img2)
    img_[2] = img2

    img3 = img[30:60, 1005:1023]
    img3 = cv2.resize(img3, (32, 32), interpolation=cv2.INTER_NEAREST)
    img3 = translate(img3)
    img_[3] = img3

    img4 = img[30:60, 1030:1048]
    img4 = cv2.resize(img4, (32, 32), interpolation=cv2.INTER_NEAREST)
    img4 = translate(img4)
    img_[4] = img4

    img5 = img[30:60, 1046:1065]
    img5 = cv2.resize(img5, (32, 32), interpolation=cv2.INTER_NEAREST)
    img5 = translate(img5)
    img_[5] = img5

    img6 = img[30:60, 1073:1091]
    img6 = cv2.resize(img6, (32, 32), interpolation=cv2.INTER_NEAREST)
    img6 = translate(img6)
    img_[6] = img6

    img7 = img[30:60, 1088:1107]
    img7 = cv2.resize(img7, (32, 32), interpolation=cv2.INTER_NEAREST)
    img7 = translate(img7)
    img_[7] = img7

    img8 = img[30:60, 1113:1130]
    img8 = cv2.resize(img8, (32, 32), interpolation=cv2.INTER_NEAREST)
    img8 = translate(img8)
    img_[8] = img8

    img9 = img[30:60, 1129:1147]
    img9 = cv2.resize(img9, (32, 32), interpolation=cv2.INTER_NEAREST)
    img9 = translate(img9)
    img_[9] = img9

    img10 = img[30:60, 1151:1169]
    img10 = cv2.resize(img10, (32, 32), interpolation=cv2.INTER_NEAREST)
    img10 = translate(img10)
    img_[10] = img10

    img11 = img[30:60, 1166:1185]
    img11 = cv2.resize(img11, (32, 32), interpolation=cv2.INTER_NEAREST)
    img11 = translate(img11)
    img_[11] = img11

    img12 = img[30:60, 1189:1208]
    img12 = cv2.resize(img12, (32, 32), interpolation=cv2.INTER_NEAREST)
    img12 = translate(img12)
    img_[12] = img12

    img13 = img[30:60, 1205:1224]
    img13 = cv2.resize(img13, (32, 32), interpolation=cv2.INTER_NEAREST)
    img13 = translate(img13)
    img_[13] = img13

    img14 = img[665:698, 40:59]
    img14 = cv2.resize(img14, (32, 32), interpolation=cv2.INTER_NEAREST)
    img14 = translate(img14)
    img_[14] = img14

    img15 = img[665:698, 55:74]
    img15 = cv2.resize(img15, (32, 32), interpolation=cv2.INTER_NEAREST)
    img15 = translate(img15)
    img_[15] = img15

    img16 = img[665:698, 70:89]
    img16 = cv2.resize(img16, (32, 32), interpolation=cv2.INTER_NEAREST)
    img16 = translate(img16)
    img_[16] = img16

    set_printoptions(suppress=True)
    set_printoptions(precision=3)
    return img_


def dict_list(dic: dict):  ##KNN
    keys = dic.keys()
    values = dic.values()
    lst = [(key, val) for key, val in zip(keys, values)]
    return lst

def xiangsidu(tests, xunlians, labels, k):
    data_hang = xunlians.shape[0]
    zu = tile(tests, (data_hang, 1)) - xunlians
    q = sqrt((zu ** 2).sum(axis=1)).argsort()
    my_dict = {}
    for i in range(k):
        votelabel = labels[q[i]]
        my_dict[votelabel] = my_dict.get(votelabel, 0) + 1
    sortclasscount = sorted(dict_list(my_dict), key=itemgetter(1), reverse=True)
    return sortclasscount[0][0]

def shibie(A):
    label_list = []
    Apex = [0 for x in range(0, 17)]
    train_length = len(tarining)
    train_zero = zeros((train_length, 1024))
    for i in range(train_length):
        doc_name = tarining[i]
        file_label = int(doc_name[0])
        label_list.append(file_label)
        train_zero[i, :] = read_file(r'%s\%s' % (trainingDigits, doc_name))
    testnum = len(test)
    for i in range(testnum):
        testdataor = A[i]
        result = xiangsidu(testdataor, train_zero, label_list, 3)
        Apex[i] = result
    return Apex

def result(video_pictures):   ##计算时间戳与摄像头编号并返回

    Bilibili = [0 for x in range(25)]   ##计算起始时间戳
    if(video_pictures[50]==1280):       ##判断视频宽度是否为1280
        for i in range(0,25):               ##循环识别前25帧
            A = img_predeal(video_pictures[i])
            x = shibie(A)
            if i == 0:                      ##将第一帧的时间保存为X，便于之后拼接时间戳
                Start_time = x
            Bilibili[i] = x[13]             ##将每次循环所识别的时间第13位，即秒，保存在同一list
        diffnumber = (Bilibili.count(Bilibili[0]))  ##根据上一步保存的list，判断发生变化的那一秒的具体帧数
        t = 1000 - 40 * diffnumber          ##计算初始的精确时间（毫秒）
    elif(video_pictures[50]==2560):         ##判断视频宽度是否为2560
        for i in range(0,25):               ##循环识别前25帧
            A = img_predeal_(video_pictures[i])
            x = shibie(A)
            if i == 0:                      ##将第一帧的时间保存为X，便于之后拼接时间戳
                Start_time = x
            Bilibili[i] = x[13]             ##将每次循环所识别的时间第13位，即秒，保存在同一list
        diffnumber = (Bilibili.count(Bilibili[0]))  ##根据上一步保存的list，判断发生变化的那一秒的具体帧数
        t = 1000 - 40 * diffnumber          ##计算初始的精确时间（毫秒）

    if(t<100):
        t = str(t)
        t ='0'+t
    Start_time.insert(14, t)            ##将毫秒插入时间list
    Start_time = [str(x) for x in Start_time]    ##转换为字符串
    CameraID = Start_time[15]+Start_time[16]+Start_time[17]  ##拼接摄像头编号
    CameraID = int(CameraID)                                 ##转换为int
    timestr = Start_time[0]+Start_time[1]+Start_time[2]+Start_time[3]+'-'+Start_time[4]+Start_time[5]+'-'+\
              Start_time[6]+Start_time[7]+' '+Start_time[8]+Start_time[9]+':'+Start_time[10]+Start_time[11]+\
              ':'+Start_time[12]+Start_time[13]+'.'+Start_time[14]    ##拼接具体时间（例：2021-0423-18：11：39.040）
    datetime_obj = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
    Start_time = int(mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)  ##将起始时间由str类（2021-0423-18：11：39.04）转换为int类时间戳


    Bilibili = [0 for x in range(25)]    ##计算结束时间戳
    if(video_pictures[50]==1280):       ##判断视频宽度是否为1280
        for i in range(25, 50):
            A = img_predeal(video_pictures[i])
            x = shibie(A)
            if i == 49:
                End_time = x
            Bilibili[i -25] = x[13]
        diffnumber = (Bilibili.count(Bilibili[24]))
        t = 40 * (diffnumber - 1)
    elif (video_pictures[50] == 2560):  ##判断视频宽度是否为2560
        for i in range(25, 50):
            A = img_predeal_(video_pictures[i])
            x = shibie(A)
            if i == 49:
                End_time = x
            Bilibili[i -25] = x[13]
        diffnumber = (Bilibili.count(Bilibili[24]))
        t = 40 * (diffnumber - 1)
    if(t<100):
        t = str(t)
        t ='0'+t
    End_time.insert(14, t)
    End_time = [str(x) for x in End_time]
    timestr = End_time[0]+End_time[1]+End_time[2]+End_time[3]+'-'+End_time[4]+End_time[5]+'-'+\
              End_time[6]+End_time[7]+' '+End_time[8]+End_time[9]+':'+End_time[10]+End_time[11]+':'+End_time[12]+End_time[13]+'.'+End_time[14]
    datetime_obj = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
    End_time = int(mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)    ##将结束时间由str类（2021-0423-18：11：39.04）转换为int类时间戳

    result = []
    float(Start_time)
    float(End_time)
    result.append(Start_time/1000)  ##最终结果增添到返回list
    result.append(End_time/1000)
    result.append(CameraID)
    return result

if __name__ == '__main__':
    trainingDigits = r'.\digits\trainingDigits'
    testDigits = r'.\digits\testDigits'
    tarining = (listdir(trainingDigits))
    test = (listdir(testDigits))

    video_path = r'.\Camvideo\video2.mp4'   ##输入视频路径
    video_pictures = save_img(video_path)    ##运行视频帧数抽取
    result = result(video_pictures)          ##返回最终结果列表
    Start_stamp = result[0]                  ##列表第0项为起始时间戳
    End_stamp = result[1]                    ##列表第1项为结束时间戳
    CameraID = result[2]                     ##列表第2项为摄像头编号
    print(video_framenumber)                           ##视频总帧数
    print(Start_stamp)
    print(End_stamp)
    print(CameraID)

