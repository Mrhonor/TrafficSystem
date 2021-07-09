#-*- coding:utf-8 –*- #
from math import cos, pi, atan, exp, log, tan, sqrt
import numpy as np

class WorldtoEarth:
    def __init__(self, CameraIDs=None, Origins=None):
        '''
        初始化世界转经纬度，该类实现给定标定框图像坐标转换为世界坐标的方法
        :param CameraIDs: 相机编号。需要是n维向量。会组成一个以相机编号为Key值的字典。
        :param Origins: 对应每个相机的世界原点的经纬度值。需要是nx2的矩阵。每行由[longitude, latitude]组成
        '''

        self.CameraOrigins = {"115":[12683819.13326001, 2607806.923181742],
                            "112":[12683888.78211379, 2607778.802634159]}
        
        self.Params = {"115":{"A" : 0.76427031, 
                            "B" : 0.52141964,
                            "C" : -0.57575661,
                            "D" : 0.92409132,
                            "dx" : 12683819.13326001,
                            "dy" : 2607806.923181742},
                        "112":{"A" : -0.81925613,
                            "B" : -0.51895576,
                            "C" : 0.57722773,
                            "D" : -0.84405935,
                            "dx" : 12683888.78211379,
                            "dy" : 2607778.802634159}
                        }

        self.__EarthRadius = 6371393 # 单位m

        len_Origin = 0
        if Origins is not None:
            Origin_shape = (np.array(Origins)).shape
            if len(Origin_shape) == 1:
                Origins = np.array(Origins).reshape(1,-1)
                Origin_shape = (np.array(Origins)).shape
            len_Origin = Origin_shape[0]

        # 构建字典
        if CameraIDs is not None:
            camera_index = 0
            for CameraID in CameraIDs:
                # 填充参数矩阵
                if len_Origin  > camera_index:
                    self.UpdateCameraOrigin(CameraID, Origins[camera_index])

                camera_index +=1


    def UpdateCameraOrigin(self, CameraID, newOrigin):
        '''
        初始化世界转经纬度，该类实现给定标定框图像坐标转换为世界坐标的方法
        :param CameraID: 相机编号。
        :param newOrigin: 对应相机的世界原点的经纬度值。由[longitude, latitude]组成
        '''

        if len(newOrigin) < 2:
            print ("Error! The length of Origin must be 2.")

        diff_long, diff_lat = self.CalcMetertoLongAndLat(newOrigin)
        self.CameraOrigins[CameraID] = [newOrigin, diff_long, diff_lat]

    def CalDisByGPS(self, GPSpoint1, GPSpoint2):
        '''
        计算给定经纬度的两个点之间的欧式距离
        :param GPSpoint: 一点的经纬度
        ：return: 两点间距离
        '''
        mkd1 = self.GPS_to_MKD(GPSpoint1)
        mkd2 = self.GPS_to_MKD(GPSpoint2)

        x_distance = mkd1.x - mkd2.x
        y_distance = mkd1.y - mkd2.y

        distance = sqrt(x_distance**2 + y_distance**2)

        return distance


    def GetOriginByCamereID(self, CameraID):
        '''
        返回对应相机ID的经纬度坐标
        :param CameraID: 需返回的相机ID
        :return: [经纬度坐标, 每米经度偏移， 每米纬度偏移]
        '''
        if CameraID in self.CameraOrigins:
            return self.CameraOrigins[CameraID]
        else:
            print ("Warning! Can't return Origin by an nonexistent ID!")
            return None

    def GPS_to_MKD(self, GPSpoint):
        '''
        地球坐标系转换为墨卡托坐标系
        :param GPSpoint: 地球坐标
        :return: 墨卡托坐标
        '''
        x = GPSpoint[0] * 20037508.34 / 180
        y = log(tan((90 + GPSpoint[1]) * pi / 360)) / (pi / 180)
        y = y * 20037508.34 / 180
        MKDpoint = [x, y]

        return MKDpoint

    def MKD_to_GPS(self, MKDpoint):
        '''
        墨卡托坐标系转换为地球坐标系
        :param MKDpoint: 墨卡托坐标
        :return: 经纬度坐标
        '''
        x = MKDpoint[0] / 20037508.34 * 180
        y = MKDpoint[1] / 20037508.34 * 180
        y = 180 / pi * (2 * atan(exp(y * pi / 180)) - pi / 2)
        GPSpoint = [x, y]

        return GPSpoint

    def IMG_to_MKD(self, IMGpoint, A, B, C, D, dx, dy):
        '''
        图像坐标系转换为墨卡托坐标系
        :param IMGpoint: 图像坐标
        :return: 墨卡托坐标
        '''
        x = A*IMGpoint[0] + B*IMGpoint[1] + dx
        y = C*IMGpoint[0] + D*IMGpoint[1] + dy
        MKDpoint = [x, y]

        return MKDpoint

    def toEarthFrame(self, CameraID, World):
        '''
        世界坐标系转换为地球坐标系
        :param CameraID: 对应的相机ID
        :param World: 对应的世界坐标
        :return : 经纬度坐标
        '''

        '''
        ret_val = self.GetOriginByCameraID(CameraID)
        if ret_val is None:
            return None

        Origin = ret_val[0]
        diff_long = ret_val[1]
        diff_lat = ret_val[2]

        longitude = Origin[0] + diff_long*World[0]/100.0
        latitude = Origin[1] + diff_lat*World[1]/100.0
        '''
        
        ret_val = self.Params[CameraID]
        if ret_val is None:
            return None

        IMGpoint = [World[0]/100, World[1]/100]
        MKDpoint = self.IMG_to_MKD(IMGpoint, ret_val["A"], ret_val["B"], ret_val["C"], ret_val["D"], ret_val["dx"], ret_val["dy"])
        GPSpoint = self.MKD_to_GPS(MKDpoint)
        longitude, latitude = GPSpoint[0], GPSpoint[1]
        
        return longitude, latitude

if __name__ == '__main__':
    a = WorldtoEarth()
    print (a.CalcMetertoLongAndLat([113.94131187635446, 22.79941303417509]))
    pass
