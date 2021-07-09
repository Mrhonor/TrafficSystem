#-*- coding:utf-8 –*- #
import numpy as np
from match.MatchingImpl import MatchingImpl
from match.YoloTransformer import YoloTransformer


class TimeStampData:
    def __init__(self, TimeStamp):
        '''
        数据类，用以存储每帧图片的标注信息
        :param TimeStamp: 时间戳
        '''
        self.TimeStamp = TimeStamp
        self.InfoList = {}

    def append(self, ID, X=None, Y=None, Width=None, Height=None, Type=None, CarLicense=None, CarColor=None):
        '''
        写入数据类
        :param ID: 目标跟踪用ID
        :param X: 标注框左上角x值
        :param Y: 标注框左上角y值
        :param Width: 标注框宽度
        :param Height: 标注框高度
        :param Type: 类型
        :param CarLicense: 车牌
        :param CarColor: 颜色
        :return:
        '''
        self.InfoList[ID] = [X,Y,Width,Height,Type,CarLicense,CarColor]

    def appendInfoList(self, ID, InfoList):
        while len(InfoList) < 7:
            InfoList.append(None)
        self.InfoList[ID] = InfoList

class Matching:
    def __init__(self, transformer=None, sendCarMSG=None, dataSQL=None):
        self.SQL = dataSQL
        self.SendCarMSG = sendCarMSG
        self.__MatchingImpl = MatchingImpl()
        self.CameraDicts = {}
        self.CarIDMapping = {} # 跟踪目标的映射
        self.Transformer = transformer
        self.CarIDSpeed = {}
        self.MatchingList = {} # 待匹配的车辆列表
        self.RestrictY = {'112': [200, 350, 1300], '115': [200, 570, 1500]}
        self.SIMILAR_THRESH = 200
        self.ColorList = ['red','orange','yellow','green','cyan','blue','purple']
        self.outData = []

    def AppendData(self, CameraID, TimeStamp, Data):
        '''
        传入数据
        :param CameraID: 相机编号
        :param TimeStamp: 时间戳
        :param Data: 列表数据，应是一个列表对象[[ID, x, y. width, height, type, CarLicense, CarColor], ...]
        '''
        if CameraID not in self.CameraDicts:
            self.CameraDicts[CameraID] = []

        data_class = TimeStampData(TimeStamp)
        for data in Data:
            data_class.appendInfoList(data[0], data[1:])
        self.CameraDicts[CameraID].append(data_class)

    def WriteTable(self, TimeStamp, ID, Longtitude, Latitude, Width, Height, Length, Type, CarColor, CarLicense, Speed):
        '''
        :param TimeStamp: 时间戳
        :param ID: 跟踪ID
        :param Longtitude: 经度
        :param Latitude: 纬度
        :param Width: 车辆宽度
        :param Height: 车辆高度
        :param Length: 车辆长度
        :param Type: 车辆类型
        :param CarColor: 车辆颜色
        :param CarLicense: 车牌（未实现）
        :param Speed: 车辆速度
        :return:
        '''
        # return
        if self.SendCarMSG and Type != 'person':
            self.SendCarMSG.send_to_virtual_platform(TimeStamp, int(ID), Longtitude, Latitude, str(Width), str(Height), str(Length), str(Type), str(CarColor), 'None', str(Speed))
        if self.SQL:
            # print(str(TimeStamp), int(ID), Longtitude, Latitude, int(Width), int(Height), int(Length), str(Type), float(Speed), str(CarColor))
            self.SQL.InsertWorldFrameTable(str(TimeStamp), int(ID), Longtitude, Latitude, int(Width), int(Height), int(abs(Length)), str(Type), float(Speed), str(CarColor))

        # print (TimeStamp, ID, Longtitude, Latitude, Width, Height, Length, Type, CarColor, CarLicense, Speed)

    def CalcSpeed(self, LastSpeed, newX, newY, lastX, lastY, deltaT, avg=0.3):
        '''
        计算速度，输入单位cm， 输出单位km/h
        :param LastSpeed: 上帧的时间
        :param deltaT: 两帧时间差
        :param avg: 滑动平均参数
        :return:
        '''
        deltaT += 1e-9
        return (((newX - lastX)**2 + (newY - lastY)**2)**0.5) / deltaT / 100 * 3.6 * avg + LastSpeed * (1 - avg)

    def Similarity(self, info1, info2):
        '''
        计算相似性用于匹配，
        具体计算公式见于文档
        :param info1: 处于管辖区摄像机内的车辆信息
        :param info2: 重叠区另一台摄像机的车辆信息
        :return:
        '''
        # [time_stamp_data.TimeStamp, long, lat, ret_width, ret_height,
        #    ret_length, Type, CarColor, CarLicense, self.CarIDSpeed[CameraID][id]] = info
        # 计算距离相似性

        # 需要修改为用经纬度的相似度
        # 数值范围0-20
        long1 = info1[1]
        lat1 = info1[2]
        long2 = info2[1]
        lat2 = info2[2]
        s_dist = self.Transformer.CalDisByGPS([long1, lat1], [long2, lat2])
        s_dist = 20 - s_dist # 单位m
        if s_dist < 0: s_dist = 0
        # 计算颜色相似度
        # 数值范围0-200

        color1 = info1[7]
        color2 = info2[7]
        s_color = 0
        if color1 not in self.ColorList or color2 not in self.ColorList:
            if color1:
                s_color = int(color1 == color2)
        else:
            index1 = self.ColorList.index(color1)
            index2 = self.ColorList.index(color2)
            dist = abs(index1-index2)
            if dist > len(self.ColorList)/2:
                dist = len(self.ColorList) - dist
            s_color = dist*2 / len(self.ColorList)
        # print (s_color)
        # s_color = 200 - np.linalg.norm(color1-color2)
        # if s_color < 0: s_color = 0

        # 计算车牌相似度
        license1 = info1[8]
        license2 = info2[8]
        s_license = 0
        # if license1 and license1 == license2:
        #     s_license = 1

        # 计算种类相似度
        type1 = info1[6]
        type2 = info2[6]
        s_type = 0
        if type1 == type2:
            s_type = 1

        # 距离和类型各占200分，颜色占50分，车牌占1000分
        return s_dist * 10 + s_color * 50 + s_license * 1000 + s_type * 200

    def ReMapID(self, CameraID, ID):
        '''
        找出该CameraID是否存在配对，如果存在则返回true、是否是映射方（需要修改ID的一方）和对应的ID，
        如果不匹配则返回false
        :param CameraID:
        :param ID:
        :return: flag, flag, newID
        '''

        IsMatched = False
        IsMapping = False
        newID = ID
        # print (self.CarIDMapping)
        if CameraID in self.CarIDMapping:
            if ID in self.CarIDMapping[CameraID]:
                # 找到了匹配的对象
                IsMatched = True
                IsMapping = True
                newID = self.CarIDMapping[CameraID][ID]
            else:
                if len(self.CameraDicts) == 1:
                    # 只有一个视频流无需配对
                    return True, True, ID
                # 没有找到匹配的对象，查看是否是映射方
                for otherCameraID in self.CarIDMapping:
                    if otherCameraID == CameraID: continue
                    for otherID in self.CarIDMapping[otherCameraID].values():
                        # print (otherID)
                        if otherID == newID:
                            # print (1)
                            IsMatched = True

        return IsMatched, IsMapping, newID


    def DataProcess(self):
        cur_time = {}
        cur_index = {}
        len_CameraDicts = {}
        for CameraID in self.CameraDicts:
            self.CameraDicts[CameraID].sort(key=lambda x:x.TimeStamp)
            cur_index[CameraID] = 0
            cur_time[CameraID] = self.CameraDicts[CameraID][cur_index[CameraID]].TimeStamp
            len_CameraDicts[CameraID] = len(self.CameraDicts[CameraID])
            self.CarIDMapping[CameraID] = {}
            self.CarIDSpeed[CameraID] = {}
            self.MatchingList[CameraID] = { }

        while self.CameraDicts:
            CameraID = min(cur_time, key=cur_time.get)
            time_stamp_data = self.CameraDicts[CameraID][cur_index[CameraID]]
            # 清空该摄像头ID的待匹配列表
            self.MatchingList[CameraID] = {}
            for id in time_stamp_data.InfoList:
                X = time_stamp_data.InfoList[id][0]
                Y = time_stamp_data.InfoList[id][1]
                Width = time_stamp_data.InfoList[id][2]
                Height = time_stamp_data.InfoList[id][3]
                Type = time_stamp_data.InfoList[id][4]
                CarLicense = time_stamp_data.InfoList[id][5]
                CarColor = time_stamp_data.InfoList[id][6]
                ret_x, ret_y, ret_z, ret_width, ret_height, ret_length = \
                    self.Transformer.toWorldframe(CameraID, X, Y, Width, Height, Type)

                # 离开该摄像头负责区域，不做进一步处理
                if ret_y > self.RestrictY[CameraID][2]: continue

                IsMatched, IsMapping, id = self.ReMapID(CameraID, id)
                long, lat = self.Transformer.toEarthframe(CameraID, ret_x, ret_y)
                # 记录车辆速度

                if id not in self.CarIDSpeed[CameraID]:
                    self.CarIDSpeed[CameraID][id] = [np.nan, time_stamp_data.TimeStamp, ret_x, ret_y]
                else:
                    last_speed, last_time, last_x, last_y = self.CarIDSpeed[CameraID][id]
                    # 没有上次的速度数据
                    if last_speed is np.nan:
                        new_speed = self.CalcSpeed(0, ret_x, ret_y, last_x, last_y, abs(time_stamp_data.TimeStamp - last_time), 1)
                        self.CarIDSpeed[CameraID][id] = [new_speed, time_stamp_data.TimeStamp, ret_x, ret_y]
                    else:
                        new_speed = self.CalcSpeed(last_speed, ret_x, ret_y, last_x, last_y, abs(time_stamp_data.TimeStamp - last_time))
                        self.CarIDSpeed[CameraID][id] = [new_speed, time_stamp_data.TimeStamp, ret_x, ret_y]

                # 处于摄像头的重叠区域
                if Type != 'person' and Type != 'motorcycle' and Type != 'bicycle':
                    if IsMatched == True and IsMapping == False:
                        # 非映射方无需负责输出
                        continue
                    if ret_y > self.RestrictY[CameraID][1]:
                        # 处于重叠区
                        if IsMatched == False:
                            # 加入匹配队列
                            self.MatchingList[CameraID][id] = [time_stamp_data.TimeStamp, long, lat, ret_width,
                                                               ret_height, ret_length, Type, CarColor, CarLicense,
                                                               self.CarIDSpeed[CameraID][id][0]]
                            continue
                    elif ret_y > self.RestrictY[CameraID][0] and ret_y < self.RestrictY[CameraID][1]:
                        # 处于边缘区域
                        if IsMatched == False:
                            self.MatchingList[CameraID][id] = [time_stamp_data.TimeStamp, long, lat, ret_width,
                                                               ret_height, ret_length, Type, CarColor, CarLicense,
                                                               self.CarIDSpeed[CameraID][id][0]]


                self.WriteTable(time_stamp_data.TimeStamp, id, long, lat, ret_width,
                           ret_height, ret_length, Type, CarColor, CarLicense, self.CarIDSpeed[CameraID][id][0])


            # 结束一帧处理，尝试匹配
            if self.MatchingList[CameraID]:
                for otherCameraID in cur_time:
                    if otherCameraID == CameraID: continue
                    if not self.MatchingList[otherCameraID]: continue
                    if abs(self.CameraDicts[otherCameraID][cur_index[otherCameraID]].TimeStamp - time_stamp_data.TimeStamp) < 0.1:
                        # 进行匹配
                        len_self = len(self.MatchingList[CameraID])
                        len_other = len(self.MatchingList[otherCameraID])
                        n = max([len_self, len_other])
                        adj_matrix = np.zeros((n,n))
                        row_ids = []
                        col_ids = []
                        for i, id1 in enumerate(self.MatchingList[CameraID]):
                            row_ids.append(id1)
                            for j, id2 in enumerate(self.MatchingList[otherCameraID]):
                                if i == 0:
                                    # 填充id列表
                                    col_ids.append(id2)

                                adj_matrix[i][j] = int(self.Similarity(self.MatchingList[CameraID][id1], self.MatchingList[otherCameraID][id2]))
                        match_res = self.__MatchingImpl.Matching(adj_matrix)
                        for i, res in enumerate(match_res):
                            # 找到需要配对的编号
                            # print (1)
                            # print (adj_matrix[int(res)][i])
                            if i >= len(col_ids) or int(res) >= len(row_ids) or adj_matrix[int(res)][i] < self.SIMILAR_THRESH:
                                continue

                            self.CarIDMapping[otherCameraID][col_ids[i]] = row_ids[int(res)]
                            del self.MatchingList[CameraID][row_ids[int(res)]]
                            del self.MatchingList[otherCameraID][col_ids[i]]




            cur_index[CameraID] += 1
            if cur_index[CameraID] >= len_CameraDicts[CameraID]:
                del self.CameraDicts[CameraID]
                del self.MatchingList[CameraID]
                del cur_time[CameraID]
            else:
                cur_time[CameraID] = self.CameraDicts[CameraID][cur_index[CameraID]].TimeStamp










if __name__ == '__main__':
    transformer = YoloTransformer()
    transformer.UpdateIntrinsicAndExtrinsicFromFile('112', 'intrinsic_params_112.csv', 'extrinsic_params_112.csv')
    transformer.UpdateIntrinsicAndExtrinsicFromFile('115', 'intrinsic_params_115.csv', 'extrinsic_params_115.csv')
    Match = Matching(transformer)

    import csv

    def ReadCSV(csv_file_name):
        with open(csv_file_name, "r") as file112:
            csv_list = list(csv.reader(file112))
            datas = csv_list[3:]
            # print (datas[0])
            # print (datas[1])
            CameraID = 0
            TimeStamp = 0
            info_list = []
            for data in datas:
                if data[0] == ' ':
                    if info_list:
                        Match.AppendData(CameraID, TimeStamp, info_list)
                        info_list = []
                    TimeStamp = float(data[7])
                    CameraID = data[8]
                else:
                    x = int(float(data[0])) * 2 + 1280
                    y = int(float(data[1])) * 2 + 720
                    Width = int(float(data[2])) * 2
                    Height = int(float(data[3])) * 2
                    type = data[4]
                    ID = str(CameraID)+"-" + data[5]
                    Color = None
                    if len(data) >= 7:
                        Color = data[6]
                    info_list.append([ID, x,y,Width,Height,type,None,Color])

    ReadCSV("infor112.csv")
    ReadCSV("infor115.csv")



    # Match.AppendData(112, 1.0, [[1,0,0, 100, 200, 'car','粤B46328', 100], [2, -525, -306, 100, 200, 'car', '粤A42357', 200]])
    # Match.AppendData(112, 1.5, [[1, 0, -10, 100, 200, 'car', '粤B46328', 100], [2, -530, -366, 100, 200, 'car', '粤A42357', 200]])
    #
    # Match.AppendData(115, 1.0, [[11,0,0, 100, 200, 'car','粤B46328', 100], [12, -525, -306, 100, 200, 'car', '粤A42357', 200]])
    # Match.AppendData(115, 1.5, [[11, 0, -10, 100, 200, 'car', '粤B46328', 100], [12, -530, -366, 100, 200, 'car', '粤A42357', 200]])

    # Match.AppendData(115, 0, [[1, 2, 3], [2, 1, 3]])
    Match.DataProcess()
    print (Match.CarIDMapping)
    # print (Match.CameraDicts[112][0].InfoList, Match.CameraDicts[112][1].InfoList)

