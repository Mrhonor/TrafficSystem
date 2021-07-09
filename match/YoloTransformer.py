#-*- coding:utf-8 –*- #
from match.Transformer import Transformer
from match.WorldtoEarth import WorldtoEarth

class YoloTransformer:
    def __init__(self, CameraIDs=None, Intrinsics=None, Extrinsics=None, Origins=None):
        '''
        初始化坐标转换类，该类实现给定标定框图像坐标转换为地球坐标的方法
        :param CameraIDs: 相机编号。需要是n维向量。会组成一个以相机编号为Key值的字典。
        :param Intrinsics: 相机内参。需要是nx3x4的矩阵。
        :param Extrinsics: 相机外参。需要是nx4x4的矩阵
        :param Origins: 相机世界原点的经纬度。需要是nx2的矩阵
        '''
        self.transformer = Transformer(CameraIDs, Intrinsics, Extrinsics)
        self.worldtoEarth = WorldtoEarth(CameraIDs)

    def UpdateIntrinsicAndExtrinsicFromFile(self, CameraID, intrinsic_file, extrinsic_file):
        '''
        更新相机内外参矩阵，保持字典一致性，推荐使用
        :param CameraID: 相机ID
        :param intrinsic_file: 内参矩阵文件路径
        :param extrinsic_file: 外参矩阵文件路径
        :return: 是否更新成功
        '''
        return self.transformer.UpdateIntrinsicAndExtrinsicFromFile(CameraID, intrinsic_file, extrinsic_file)

    def GetZbyType(self, Type):
        '''
        根据类型判定车辆高度
        :param Type:
        :return: z轴高度(cm)
        '''
        if Type == 'car':
            return 160
        if Type == 'bus':
            return 250
        if Type == 'truck':
            return 250
        if Type == 'motorcycle' or Type == 'bicycle':
            return 140
        if Type == 'person':
            return 170
        return 0


    def toWorldframe(self, CameraID, X, Y, Width, Height, Type):
        '''
        图像坐标转换为世界坐标
        :param CameraID: 相机ID
        :param X: 标注框左上角x值
        :param Y: 标注框左上角y值
        :param Width: 标注框宽度
        :param Height: 标注框高度
        :param Type: 类型
        :return : ret_x, ret_y, ret_z, ret_width, ret_height, ret_length 右下角点的坐标
        '''
        X = int(X)
        Y = int(Y)
        Width = int(Width)
        Height = int(Height)
        LD = self.transformer.toWorldFrame(CameraID, [X, Y+Height],         zaxis=0) # 左下
        RD = self.transformer.toWorldFrame(CameraID, [X+Width, Y+Height],   zaxis=0) # 右下
        # LU = self.transformer.toWorldFrame(CameraID, [X, Y],                zaxis=self.GetZbyType(Type)) # 左上
        RU = self.transformer.toWorldFrame(CameraID, [X+Width, Y],          zaxis=self.GetZbyType(Type)) # 右上
        # 右上
        ret_x =  RD[0]
        ret_y = RD[1]
        ret_z = 0
        ret_width = LD[1] - RD[1]
        ret_height = self.GetZbyType(Type)
        ret_length = RU[0] - RD[0]
        return ret_x, ret_y, ret_z, ret_width, ret_height, ret_length

    def toEarthframe(self, CameraID, x, y):
        '''
        世界坐标系转换为地球坐标系
        :param CameraID: 对应的相机ID
        :param World: 对应的世界坐标
        :return : 经纬度坐标
        '''
        # print (CameraID, x, y)
        # print (type(CameraID))
        return self.worldtoEarth.toEarthFrame(CameraID, [x, y])
        # return None, None

    def CalDisByGPS(self, GPSpoint1, GPSpoint2):
        '''
        计算给定经纬度的两个点之间的欧式距离
        :param GPSpoint: 一点的经纬度
        ：return: 两点间距离
        '''
        return self.worldtoEarth.CalDisByGPS(GPSpoint1, GPSpoint2)

    # def CalcMetertoLongAndLat(self, Origin):
    #     '''
    #     根据给定经纬度，计算一米的偏移约为多少经纬度
    #     :param Origin: 对应原点的经纬度值。由[longitude, latitude]组成
    #     :return diff_long: 一米对应的经度偏移
    #     :return diff_lat: 一米对应的纬度偏移
    #     '''
    #     # return self.worldtoEarth.CalcMetertoLongAndLat(Origin)
    #     return [8.992661340262631e-06, -1.3018608391654473e-05]


if __name__ == '__main__':
    import csv
    with open('test2.csv', 'r') as csv_file_read:
        csv_list = list(csv.reader(csv_file_read))

    transformer = YoloTransformer()
    transformer.UpdateIntrinsicAndExtrinsicFromFile(115, 'intrinsic_params_115.csv', 'extrinsic_params_115.csv')
    outlist = []
    for data in csv_list:
        res = list(transformer.toWorldframe(115, int(data[0]), int(data[1]), int(data[2]), int(data[3]), data[4]))
        res.append(data[5])
        res.append(data[4])

        outlist.append(res)

    data_type = ["x", "y", "z", "width", "height", "length", "id", "type"]
    with open('out.csv', 'w', newline='') as csv_file:  # csv.writer need to use newline method
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data_type)
        csv_writer.writerows(outlist)
