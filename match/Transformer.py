#-*- coding:utf-8 –*- #
import csv
import os
import numpy as np

class Transformer:
    def __init__(self, CameraIDs=None, Intrinsics=None, Extrinsics=None):
        '''
        初始化坐标转换类，该类提供从世界坐标和图像坐标的转换方法
        :param CameraIDs: 相机编号。需要是n维向量。会组成一个以相机编号为Key值的字典。
        :param Intrinsics: 相机内参。需要是nx3x4的矩阵。
        :param Extrinsics: 相机外参。需要是nx4x4的矩阵
        '''

        self.IntrinsicDict = {}
        self.ExtrinsicDict = {}

        # 记录内外参矩阵的长度
        len_intrin = 0
        len_extrin = 0
        if Intrinsics is not None:
            intrin_shape = (np.array(Intrinsics)).shape
            len_intrin = intrin_shape[0]
            if len(intrin_shape) == 2:
                Intrinsics = [Intrinsics]
                intrin_shape = np.array(Intrinsics).shape
                len_intrin = intrin_shape[0]
            if len(intrin_shape) != 3:
                print ("Error! Intrinsics must be nx3x4.")

        if Extrinsics is not None:
            extrin_shape = (np.array(Extrinsics)).shape
            len_extrin = extrin_shape[0]
            if len(extrin_shape) == 2:
                Extrinsics = [Extrinsics]
                extrin_shape = np.array(Extrinsics).shape
                len_extrin = extrin_shape[0]
            if len(extrin_shape) != 3:
                print ("Error! Extrinsics must be nx4x4.")

        if len_intrin != len_extrin:
            print ('Warning! Input dimension of Intrinsics and Extrinsics mismatch. Init will be continue, but some data will be discarded.')

        # 构建字典
        if CameraIDs is not None:
            camera_index = 0
            for CameraID in CameraIDs:
                # 填充参数矩阵
                if len_intrin  > camera_index:
                    self.UpdateIntrinsic(CameraID, Intrinsics[camera_index])

                if len_extrin > camera_index:
                    self.UpdateExtrinsic(CameraID, Extrinsics[camera_index])

                camera_index +=1
        elif len_intrin != 0 or len_extrin !=0:
            print ("Error! CameraID shouldn't be None, dict wouldn't be created!")


    def UpdateIntrinsic(self, CameraID, Intrinsic):
        '''
        更新内参矩阵
        :param CameraID: 需要更新的对应相机ID
        :param Intrinsic: 内参矩阵
        :return 是否更新成功
        '''
        if Intrinsic is None:
            print ("Error! Intrinsic is None. Update will be fail.")
            return False

        rows, cols = np.array(Intrinsic).shape
        if rows != 3 or (cols != 3 and cols != 4):
            print ('Error! Intrinsic should be 3x3 or 3x4 matrix, but got a {}x{} matrix. Update will be fail.'.format(rows, cols))
            return False

        # 如果得到一个3x3的矩阵则补充为3x4
        if cols == 3:
            Intrinsic = np.hstack(Intrinsic, np.zeros((3,1)))

        # 最后一列必须全为0
        if cols == 4:
            for i in range(0, 3):
                if Intrinsic[i][3] != 0:
                    Intrinsic[i][3] = 0
                    print('Warning! The last col of Intrinsic must all be zero.')

        self.IntrinsicDict[CameraID] = Intrinsic
        return True


    def UpdateExtrinsic(self, CameraID, Extrinsic):
        '''
        更新外参矩阵
        :param CameraID: 需要更新的对应相机ID
        :param Extrinsic: 外参矩阵
        :return 是否更新成功
        '''
        if Extrinsic is None:
            print ("Error! Extrinsic is None. Update will be fail.")
            return False

        rows, cols = np.array(Extrinsic).shape
        if cols != 4 or (rows != 3 and rows != 4):
            print ('Error! Extrinsic should be 3x4 or 4x4 matrix, but got a {}x{} matrix. Update will be fail.'.format(rows, cols))
            return False

        # 如果得到一个3x4的矩阵则补充为4x4
        if rows == 3:
            Extrinsic = np.vstack(Extrinsic, np.zeros((1,4)))
            Extrinsic[3][3] = 1

        # 最后一列必须全为0
        if rows == 4:
            if Extrinsic[3] != [0,0,0,1]:
                Extrinsic[3] = [0,0,0,1]
                print('Warning! The last row of Extrinsic must be [0,0,0,1].')

        self.ExtrinsicDict[CameraID] = Extrinsic
        return True

    def ReadFromCSV(self, file_path):
        '''
        从CSV文件中读取矩阵
        :param file_path: CSV文件路径
        :return: 返回矩阵
        '''
        if os.path.isfile(file_path) is False:
            print ("Error! File name or path doesn't exist.")
            return None

        with open(file_path, 'r') as csv_file_read:
            csv_list = list(csv.reader(csv_file_read))
            raw_data = csv_list[0:]  # extract data
            floatMatrix = []
            for row in raw_data:
                row = list(map(float, row))
                floatMatrix.append(row)

        return floatMatrix

    def UpdateIntrinsicFromFile(self, CameraID, file_path):
        '''
        从CSV文件中读取矩阵并更新内参矩阵
        :param CameraID: 对应的相机ID
        :param file_path: CSV文件路径
        :return 是否更新成功
        '''
        return self.UpdateIntrinsic(CameraID, self.ReadFromCSV(file_path))

    def UpdateExtrinsicFromFile(self, CameraID, file_path):
        '''
        从CSV文件中读取矩阵并更新外参矩阵
        :param CameraID: 对应的相机ID
        :param file_path: CSV文件路径
        :return 是否更新成功
        '''
        return self.UpdateExtrinsic(CameraID, self.ReadFromCSV(file_path))

    def UpdateIntrinsicAndExtrinsic(self, CameraID, intrinsic, extrinsic):
        '''
        更新相机内外参矩阵，保持字典一致性，推荐使用。
        :param CameraID: 相机ID
        :param intrinsic: 内参矩阵
        :param extrinsic: 外参矩阵
        :return: 是否更新成功
        '''
        if self.UpdateIntrinsic(CameraID, intrinsic) is False:
            return False

        if self.UpdateExtrinsic(CameraID, extrinsic) is False:
            self.RemoveIntrinsicFromCameraID(CameraID)
            return False

        return True

    def UpdateIntrinsicAndExtrinsicFromFile(self, CameraID, intrinsic_file, extrinsic_file):
        '''
        更新相机内外参矩阵，保持字典一致性，推荐使用
        :param CameraID: 相机ID
        :param intrinsic_file: 内参矩阵文件路径
        :param extrinsic_file: 外参矩阵文件路径
        :return: 是否更新成功
        '''
        intrinsic = self.ReadFromCSV(intrinsic_file)
        extrinsic = self.ReadFromCSV(extrinsic_file)
        return self.UpdateIntrinsicAndExtrinsic(CameraID, intrinsic, extrinsic)

    def UpdateCameraID(self, preCameraID, newCameraID):
        '''
        修改相机ID
        :param preCameraID: 原相机ID
        :param newCameraID:  新相机ID
        :return: 是否更新成功
        '''

        if newCameraID in self.ExtrinsicDict or \
                newCameraID in self.IntrinsicDict:
            print ("Error! Can't update old CameraID to an existent ID. Update will be fail.")
            return False

        if preCameraID in self.ExtrinsicDict or \
                preCameraID in self.IntrinsicDict:
            self.ExtrinsicDict[newCameraID] = self.ExtrinsicDict.pop(preCameraID)
            self.IntrinsicDict[newCameraID] = self.IntrinsicDict.pop(preCameraID)
            return True

        print ("Error! Can't update CameraID from an nonexistent ID. Update will be fail.")
        return False


    def RemoveExtrinsicFromCameraID(self, CameraID):
        '''
        删除对应相机ID的外参矩阵
        :param CameraID: 相机ID
        :return: 被删除的外参矩阵
        '''
        return self.ExtrinsicDict.pop(CameraID)

    def RemoveIntrinsicFromCameraID(self, CameraID):
        '''
        删除对应相机ID的内参矩阵
        :param CameraID: 相机ID
        :return: 被删除的内参矩阵
        '''
        return self.IntrinsicDict.pop(CameraID)

    def GetExtrinsicDict(self):
        '''
        :return: 返回外参字典的浅拷贝
        '''
        return self.ExtrinsicDict.copy()

    def GetIntrinsicDict(self):
        '''
        :return: 返回内参字典的浅拷贝
        '''
        return self.IntrinsicDict.copy()

    def GetExtrinsicFromCameraID(self, CameraID):
        '''
        返回对应相机ID的外参矩阵
        :param CameraID: 需返回的相机ID
        :return: 外参矩阵
        '''
        if CameraID in self.ExtrinsicDict:
            return self.ExtrinsicDict[CameraID]
        else:
            print ("Warning! Can't return extrinsic by an nonexistent ID!")
            return None

    def GetIntrinsicFromCameraID(self, CameraID):
        '''
        返回对应相机ID的内参矩阵
        :param CameraID: 需返回的相机ID
        :return: 内参矩阵
        '''
        if CameraID in self.IntrinsicDict:
            return self.IntrinsicDict[CameraID]
        else:
            print ("Warning! Can't return intrinsic by an nonexistent ID!")
            return None

    def GetAllCameraID(self):
        '''
        :return: 内参字典key， 外参字典key
        '''
        return self.IntrinsicDict.keys(), self.ExtrinsicDict.keys()

    def GetExtrinsicDictSize(self):
        '''
        :return: 返回外参字典长度
        '''
        return self.ExtrinsicDict.keys()

    def GetIntrinsicDictSize(self):
        '''
        :return: 返回内参字典长度
        '''
        return self.IntrinsicDict.keys()

    def toPicureFrame(self, CameraID, WorldCoordinate):
        '''
        将世界坐标转为图像坐标系坐标
        :param CameraID: 相机ID
        :param WorldCoordinate: 世界坐标(cm)
        :return: 图像坐标系坐标
        '''
        extrinsic = self.GetExtrinsicFromCameraID(CameraID)
        intrinsic = self.GetIntrinsicFromCameraID(CameraID)

        if extrinsic is None or intrinsic is None:
           print ("Error! Doesn't exist such CameraID:{}".format(CameraID))
           return None

        WorldCoordinate = np.array(WorldCoordinate)

        WorldCoordinate = WorldCoordinate.reshape(-1, 1)

        rows, cols, = np.array(WorldCoordinate).shape

        if rows != 3 and rows != 4:
           print ("Error! Coordinate should be 3 dimension or 4 dimension, but got {} dimension".format(rows))
           return None

        # 3维向量转4维向量
        if rows == 3:
           WorldCoordinate = np.vstack((WorldCoordinate, [1]))

        PicureFrameCoordinate = np.dot(intrinsic, np.dot(extrinsic, WorldCoordinate))

        PicureFrameCoordinate /= PicureFrameCoordinate[2]

        return PicureFrameCoordinate[0:2].reshape(1, -1)[0]

    def toWorldFrame(self, CameraID, PicureCoordinate, zaxis=0):
        '''
        将图像坐标系转为世界坐标系坐标，默认Z轴为0
        :param CameraID: 相机ID
        :param PicureCoordinate: 图像坐标,[u,v],以图像中点为[0,0]
        :param zaxis: 投影的z轴高度(cm)
        :return: 世界坐标系坐标(cm)
        '''
        extrinsic = self.GetExtrinsicFromCameraID(CameraID)
        intrinsic = self.GetIntrinsicFromCameraID(CameraID)

        if extrinsic is None or intrinsic is None:
           print ("Error! Doesn't exist such CameraID:{}".format(CameraID))
           return None

        PicureCoordinate = np.array(PicureCoordinate)

        PicureCoordinate = PicureCoordinate.reshape(-1, 1)

        rows, cols, = np.array(PicureCoordinate).shape

        if rows != 2 and rows != 3:
           print ("Error! Coordinate should be 2 dimension or 3 dimension, but got {} dimension".format(rows))
           return None

        # 2维向量转3维向量
        if rows == 2:
            PicureCoordinate = np.vstack((PicureCoordinate, [1]))

        inDotex = np.dot(intrinsic, extrinsic)

        ParamMatrix = np.concatenate((inDotex[..., 0:2], -PicureCoordinate), axis=1)
        BMatrix = -(inDotex[..., 2] * zaxis + inDotex[..., 3])

        WorldCoordinate = np.dot(np.linalg.inv(ParamMatrix), BMatrix)

        return WorldCoordinate[0:2]




if __name__ == '__main__':
    # 空参数初始化测试
    transformer = Transformer()
    print ("空参数初始化测试:")
    print (transformer.IntrinsicDict)
    print (transformer.ExtrinsicDict)
    print ('-'*10)

    # 正确参数初始化测试
    print ("正确参数初始化测试:")
    with open('intrinsic_params_112.csv', 'r') as csv_file_read:
        csv_list = list(csv.reader(csv_file_read))
        data = csv_list[0:]  # extract data
        intrinsic = []
        for row in data:
            row = list(map(float, row))
            intrinsic.append(row)

    with open('extrinsic_params_112.csv', 'r') as csv_file_read:
        csv_list = list(csv.reader(csv_file_read))
        data = csv_list[0:]  # extract data
        extrinsic = []
        for row in data:
            row = list(map(float, row))
            extrinsic.append(row)

    transformer = Transformer([1,2], [intrinsic, intrinsic], [extrinsic, extrinsic])
    print (transformer.IntrinsicDict)
    print (transformer.ExtrinsicDict)
    print ('-' * 10)

    # 输入参数维度不匹配初始化测试
    print ("输入参数维度不匹配参数初始化测试:")
    transformer = Transformer([1,2], [intrinsic], [extrinsic, extrinsic])
    print (transformer.IntrinsicDict)
    print (transformer.ExtrinsicDict)
    print ('-' * 10)

    # CameraID为空
    print ("输入参数维度不匹配参数初始化测试:")
    transformer = Transformer(None, [intrinsic, intrinsic], [extrinsic, extrinsic])
    print (transformer.IntrinsicDict)
    print (transformer.ExtrinsicDict)
    print ('-' * 10)

    # 参数矩阵出错
    print ("输入参数矩阵出错初始化测试:")
    transformer = Transformer([1], [intrinsic[1:2]], [extrinsic[1:2]])
    print (transformer.IntrinsicDict)
    print (transformer.ExtrinsicDict)
    print ('-' * 10)

    # 从文件中更新参数矩阵
    print ("从文件中更新参数矩阵测试:")
    transformer = Transformer()
    transformer.UpdateIntrinsicAndExtrinsicFromFile(1, 'intrinsic_params_112.csv', 'extrinsic_params_112.csv')
    transformer.UpdateIntrinsicAndExtrinsicFromFile(2, 'intrinsic_params_115.csv', 'extrinsic_params_115.csv')
    print (transformer.IntrinsicDict)
    print (transformer.ExtrinsicDict)
    print ('-' * 10)

    # 从不存在的文件中更新参数矩阵
    print ("从不存在的文件中更新参数矩阵测试:")
    transformer = Transformer()
    transformer.UpdateIntrinsicAndExtrinsicFromFile(1, 'intrinsic_params_110.csv', 'extrinsic_params_110.csv')
    print (transformer.IntrinsicDict)
    print (transformer.ExtrinsicDict)
    print ('-' * 10)

    # 部分文件不存在时更新参数矩阵
    print ("部分文件不存在时更新参数矩阵测试:")
    transformer = Transformer()
    transformer.UpdateIntrinsicAndExtrinsicFromFile(1, 'intrinsic_params_112.csv', 'extrinsic_params_110.csv')
    print (transformer.IntrinsicDict)
    print (transformer.ExtrinsicDict)
    print ('-' * 10)

    # 修改已经存在的参数矩阵
    print ("修改已经存在的参数矩阵测试:")
    transformer = Transformer()
    transformer.UpdateIntrinsicAndExtrinsicFromFile(1, 'intrinsic_params_112.csv', 'extrinsic_params_112.csv')
    print ("更新前：")
    print (transformer.IntrinsicDict)
    print (transformer.ExtrinsicDict)
    print ("更新后：")
    transformer.UpdateIntrinsicAndExtrinsicFromFile(1, 'intrinsic_params_115.csv', 'extrinsic_params_115.csv')
    print (transformer.IntrinsicDict)
    print (transformer.ExtrinsicDict)
    print ('-' * 10)

    # 世界坐标转图像坐标测试
    print ("世界坐标转图像坐标测试:")
    transformer = Transformer()
    transformer.UpdateIntrinsicAndExtrinsicFromFile(112, 'intrinsic_params_112.csv', 'extrinsic_params_112.csv')
    transformer.UpdateIntrinsicAndExtrinsicFromFile(115, 'intrinsic_params_115.csv', 'extrinsic_params_115.csv')
    world_frame = [[0,0,0],
                   [355,13,0],
                   [355,673,0],
                   [850,673,0],
                   [5355,673,0]]
    true_picture_frame = [[0, 0],
                     [-12, -70],
                     [-609, -79],
                     [-525, -156],
                     [-253, -417]]
    calc_picture_frame = [list(transformer.toPicureFrame(112, world)) for world in world_frame]
    error_picture_frame = [np.abs(np.array(true_picture_frame) - np.array(calc_picture_frame)).tolist()]
    print ("对112号相机：")
    print ("世界坐标："+ str(world_frame))
    print ("真值图像坐标："+ str(true_picture_frame))
    print ("计算所得图像坐标："+str(calc_picture_frame))
    print ("误差值："+str(error_picture_frame))
    print ('-' * 10)
    print ("对115号相机：")
    world_frame = [[0,0,0],
                   [600,0,0],
                   [600,40,0],
                   [600,600,0],
                   [5000,-40,0],
                   [5000,600,0]]
    true_picture_frame = [[0, 0],
                          [-4, -115],
                          [-35, -116],
                          [-472, -125],
                          [-5, -388],
                          [-261, -391]]
    calc_picture_frame = [list(transformer.toPicureFrame(115, world)) for world in world_frame]
    error_picture_frame = [np.abs(np.array(true_picture_frame) - np.array(calc_picture_frame)).tolist()]
    print ("世界坐标："+ str(world_frame))
    print ("真值图像坐标："+ str(true_picture_frame))
    print ("计算所得图像坐标："+str(calc_picture_frame))
    print ("误差值："+str(error_picture_frame))
    print ('-' * 10)

    print ("图像坐标转世界坐标测试:")
    transformer = Transformer()
    transformer.UpdateIntrinsicAndExtrinsicFromFile(112, 'intrinsic_params_112.csv', 'extrinsic_params_112.csv')
    transformer.UpdateIntrinsicAndExtrinsicFromFile(115, 'intrinsic_params_115.csv', 'extrinsic_params_115.csv')
    true_world_frame = [[0,0,0],
                   [355,13,0],
                   [355,673,0],
                   [850,673,0],
                   [5355,673,0],
                        [0,0,0]]
    picture_frame = [[0, 0],
                     [-12, -70],
                     [-609, -79],
                     [-525, -156],
                     [-253, -417],
                     [146, -145]]
    calc_world_frame = [list(transformer.toWorldFrame(112, picture)) for picture in picture_frame]
    error_world_frame = [np.abs(np.array(true_world_frame)[:, 0:2] - np.array(calc_world_frame)).tolist()]
    print ("对112号相机：")
    print ("图像坐标："+ str(picture_frame))
    print ("真值世界坐标："+ str(true_world_frame))
    print ("计算所得世界坐标："+str(calc_world_frame))
    print ("误差值：" + str(error_world_frame))
    print ('-' * 10)
    print ("对115号相机：")
    true_world_frame = [[0,0,0],
                   [600,0,0],
                   [600,40,0],
                   [600,600,0],
                   [5000,-40,0],
                   [5000,600,0],
                        [0,0,0],
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]]
    picture_frame = [[0, 0],
                     [-4, -115],
                     [-35, -116],
                     [-472, -125],
                     [-5, -388],
                     [-261, -391],
                     [728,-17],
                     [611,-100],
                     [-589,-41],
                     [-504,-131],
                     [1186-1280,405-720]]
    calc_world_frame = [list(transformer.toWorldFrame(115, picture)) for picture in picture_frame]

    # error_world_frame = [np.abs(np.array(true_world_frame)[:, 0:2] - np.array(calc_world_frame)).tolist()]
    print ("图像坐标："+ str(picture_frame))
    print ("真值世界坐标："+ str(true_world_frame))
    print ("计算所得世界坐标："+str(calc_world_frame))
    # print ("误差值：" + str(error_world_frame))
    print ('-' * 10)


    # print(transformer.toWorldFrame(1, [569, -144]))
