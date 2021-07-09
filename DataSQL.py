#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

class DataSQL:
         def __init__(self, host, username, password, db_name):
               '''
               初始化数据库类，该类提供图像数据库中表的创建和存储方法
               :param username: 数据库登录用户名
               :param password: 数据库登录，密码
               :param db_name: 数据库名
               '''
               self.db = MySQLdb.connect(host, username, password, db_name, charset='utf8')
               self.cursor = self.db.cursor()

         def CreateImagePathTable(self):
             '''
             在数据库中创建图像路径表
             '''
             try:
                 #self.cursor.execute("DROP TABLE IF EXISTS ImagePathTable")
                 sql = """CREATE TABLE ImagePathTable
                 (ImagePath VARCHAR(50) NOT NULL, PRIMARY KEY(ImagePath))"""
                 self.cursor.execute(sql)
             except:
                 print('ImagePathTable already exists')

         def InsertImagePathTable(self, imagepath):
             '''
             在图像路径表中插入数据
             :param imagepath: 图像路径
             '''
             try:
                 sql = "INSERT INTO ImagePathTable(ImagePath) " \
                       "VALUES('%s')" % (imagepath)
                 self.cursor.execute(sql)
                 self.db.commit()
             except:
                 print('imagepath already exists')
                 self.db.rollback()

         def CreateTimeStampTable(self):
             '''
             在数据库中创建时间帧表
             '''
             try:
                 #self.cursor.execute("DROP TABLE IF EXISTS TimeStampTable")
                 sql = """CREATE TABLE TimeStampTable
                 (TimeStamp VARCHAR(50) NOT NULL, PRIMARY KEY(TimeStamp))"""
                 self.cursor.execute(sql)
             except:
                 print('TimeStampTable already exists')

         def InsertTimeStampTable(self, timestamp):
             '''
             在时间帧表中插入数据
             :param timestamp: 时间帧
             '''
             try:
                 sql = "INSERT INTO TimeStampTable(TimeStamp) " \
                       "VALUES('%s')" % (timestamp)
                 self.cursor.execute(sql)
                 self.db.commit()
             except:
                 # print('timestamp already exists')
                 self.db.rollback()

         def CreateIdTable(self):
             '''
             在数据库中创建车辆/行人ID表
             '''
             try:
                 #self.cursor.execute("DROP TABLE IF EXISTS IdTable")
                 sql = """CREATE TABLE IdTable
                 (ID SMALLINT UNSIGNED NOT NULL, PRIMARY KEY(ID))"""
                 self.cursor.execute(sql)
             except:
                 print('IdTable already exists')

         def InsertIdTable(self, id):
             '''
             在标注框序号表中插入数据
             :param id: 车辆/行人ID
             '''
             try:
                 sql = "INSERT INTO IdTable(ID) " \
                       "VALUES(%d)" % (id)
                 self.cursor.execute(sql)
                 self.db.commit()
             except:
                 # print('id already exists')
                 self.db.rollback()

         def CreateImageDataTable(self):
               '''
               在数据库中创建图像数据对应表
               '''
               try:
                   #self.cursor.execute("DROP TABLE IF EXISTS ImageDataTable")
                   self.CreateImagePathTable()
                   self.CreateTimeStampTable()
                   sql = """CREATE TABLE ImageDataTable
                   (ImagePath VARCHAR(50) NOT NULL, TimeStamp TIMESTAMP NOT NULL, 
                   CameraID TINYINT UNSIGNED,Num_of_Bnb TINYINT UNSIGNED, 
                   primary key(ImagePath, TimeStamp), 
                   FOREIGN KEY(ImagePath) REFERENCES ImagePathTable(ImagePath),
                   FOREIGN KEY(TimeStamp) REFERENCES TimeStampTable(TimeStamp))"""
                   self.cursor.execute(sql)
               except:
                   print('ImageDataTable already exists')

         def InsertImageDataTable(self, imagepath, timestamp, camera_id, num_of_bnb):
               '''
               在图像数据对应表中插入数据
               :param imagepath: 图像路径
               :param timestamp: 时间帧
               :param camera_id: 摄像头编号
               :param num_of_bnb: 标注框数量
               '''
               try:
                  out_0 = self.SearchImageDataTable(imagepath, timestamp)
                  out_1 = self.SearchImageDataTable(imagepath)
                  out_2 = self.SearchImageDataTable(None, timestamp)
                  if out_0 == 0 and out_1 == 0 and out_2 == 0:
                      self.InsertImagePathTable(imagepath)
                      self.InsertTimeStampTable(timestamp)
                      sql = "INSERT INTO ImageDataTable(ImagePath, TimeStamp, CameraID, Num_of_Bnb) " \
                            "VALUES('%s', '%s', %d, %d)" % (imagepath, timestamp, camera_id, num_of_bnb)
                      self.cursor.execute(sql)
                      self.db.commit()
                  else:
                      print('imagedata already exists')
               except:
                  print('Error: fail to insert imagedata')
                  self.db.rollback()

         def SearchImageDataTable(self, imagepath=None, timestamp=None):
               '''
               在图像数据对应表中查询数据
               :param imagepath: 图像路径（主码）
               :param timestamp: 时间帧（主码）
               :return: 表项数据
               '''
               if imagepath == None:
                   if timestamp == None:
                       print("Error: no key input")
                   else:
                       sql = "SELECT * FROM ImageDataTable WHERE TimeStamp = '%s'" % (timestamp)
                       try:
                           self.cursor.execute(sql)
                           results = self.cursor.fetchall()
                           if len(results) == 0:
                               return 0
                           return results
                       except:
                           # print("Error: unable to fecth data")
                           return 0
               else:
                   sql = "SELECT * FROM ImageDataTable WHERE ImagePath = '%s'" % (imagepath)
                   try:
                       self.cursor.execute(sql)
                       results = self.cursor.fetchall()
                       if len(results) == 0:
                           return 0
                       return results
                   except:
                       # print("Error: unable to fecth data")
                       return 0

         def OutputImageDataTable(self):
             '''
             输出图像数据对应表
             '''
             try:
                 sql = "select * from imagedatatable into outfile 'ImageData.csv' " \
                       "fields terminated by ',' " \
                       "lines terminated by '\r\n';"
                 self.cursor.execute(sql)
             except:
                 print("Error: file already exists")

         def CreateImageBoundingTable(self):
               '''
               在数据库中创建图像标注数据表
               '''
               try:
                   #self.cursor.execute("DROP TABLE IF EXISTS ImageBoundingTable")
                   self.CreateIdTable()
                   self.CreateImagePathTable()
                   sql = """CREATE TABLE ImageBoundingTable 
                      (ImagePath CHAR(50) NOT NULL,
                      ID SMALLINT UNSIGNED NOT NULL,
                      X SMALLINT UNSIGNED,Y SMALLINT UNSIGNED,
                      Width SMALLINT UNSIGNED,Height SMALLINT UNSIGNED,
                      Type CHAR(20) NOT NULL, Color CHAR(20) NOT NULL, 
                      primary key(ImagePath, ID), 
                      foreign key(ImagePath) REFERENCES ImagePathTable(ImagePath),
                      foreign key(ID) REFERENCES IdTable(ID))"""
                   self.cursor.execute(sql)
               except:
                   print('ImageBoundingTable already exists')

         def InsertImageBoundingTable(self, imagepath, id, x, y, width, height, type, color):
               '''
               在图像数据标注数据表中插入数据
               :param imagepath: 图像路径
               :param id: 车辆/行人ID
               :param x: 标注框起点x坐标
               :param y: 标注框起点y坐标
               :param width: 标注框宽度
               :param height: 标注框高度
               :param type: 类型
               :param color: 车辆的颜色
               '''
               try:
                  out_0 = self.SearchImageBoundingTable(imagepath, id)
                  out_1 = self.SearchImageBoundingTable(imagepath)
                  out_2 = self.SearchImageBoundingTable(None, id)
                  if out_0 == 0 and out_1 == 0 and out_2 == 0:
                      self.InsertIdTable(id)
                      self.InsertImagePathTable(imagepath)
                      sql = "INSERT INTO ImageBoundingTable(ImagePath, ID, X, Y, Width, Height, Type, Color)" \
                            " VALUE('%s', %d, %d, %d, %d, %d, '%s', '%s')" % (imagepath, id, x, y, width, height, type, color)
                      self.cursor.execute(sql)
                      self.db.commit()
                  else:
                      print('imagebounding already exists')
               except:
                  print('Error: fail to insert imagebounding')
                  self.db.rollback()

         def SearchImageBoundingTable(self, imagepath=None, id=None):
               '''
               在图像标注数据表中查询数据
               :param imagepath: 图像路径（主码）
               :param id: 车辆/行人ID（主码）
               :return: 表项数据
               '''
               if imagepath == None:
                   if id == None:
                       print("Error: no key input")
                   else:
                       sql = "SELECT * FROM ImageBoundingTable WHERE ID = %d" % (id)
                       try:
                           self.cursor.execute(sql)
                           results = self.cursor.fetchall()
                           if len(results) == 0:
                               return 0
                           return results
                       except:
                           # print("Error: unable to fecth data")
                           return 0
               else:
                   sql = "SELECT * FROM ImageBoundingTable WHERE ImagePath = '%s'" % (imagepath)
                   try:
                       self.cursor.execute(sql)
                       results = self.cursor.fetchall()
                       if len(results) == 0:
                           return 0
                       return results
                   except:
                       # print("Error: unable to fecth data")
                       return 0

         def OutputImageBoundingTable(self):
             '''
             输出图像标注数据表
             '''
             try:
                 sql = "select * from imageboundingtable into outfile 'ImageBounding.csv' " \
                       "fields terminated by ',' " \
                       "lines terminated by '\r\n';"
                 self.cursor.execute(sql)
             except:
                 print("Error: file already exists")

         def CreateWorldFrameTable(self):
               '''
               在数据库中创建世界坐标对应表
               '''
               try:
                   #self.cursor.execute("DROP TABLE IF EXISTS WorldFrameTable")
                   self.CreateTimeStampTable()
                   self.CreateIdTable()
                   sql = """CREATE TABLE WorldFrameTable
                      (TimeStamp VARCHAR(50), 
                      ID SMALLINT UNSIGNED NOT NULL,
                      Longitude DOUBLE, Latitude DOUBLE, 
                      Width SMALLINT UNSIGNED, Height SMALLINT UNSIGNED, Length SMALLINT UNSIGNED, 
                      Type CHAR(20) NOT NULL, Speed FLOAT, Color CHAR(20) NOT NULL,
                      primary key(TimeStamp, ID), 
                      FOREIGN KEY(TimeStamp) REFERENCES TimeStampTable(TimeStamp), 
                      FOREIGN KEY(ID) REFERENCES IdTable(ID))"""
                   self.cursor.execute(sql)
               except:
                   print('WorldFrameTable already exists')

         def InsertWorldFrameTable(self, timestamp, id, longitude, latitude, width, height, length, type, speed, color):
             '''
             在世界坐标图像标注数据表中插入数据
             :param timestamp: 时间帧
             :param id: 车辆/行人ID
             :param longitude: 车辆的经度
             :param latitude: 车辆的纬度
             :param width: 标注框宽度
             :param height: 标注框高度
             :param length: 标注框长度
             :param type: 类型
             :param speed: 车辆的速度
             :param color: 车辆的颜色
             '''
             try:
                 flag = 1
                 out = self.SearchWorldFrameTable(timestamp)
                 if out != 0:
                     for index in range(len(out)):
                         if out[index][1] == id:
                             flag = 0
                 if flag == 1:
                     self.InsertIdTable(id)
                     self.InsertTimeStampTable(timestamp)
                     sql = "INSERT INTO WorldFrameTable(TimeStamp, ID, Longitude, Latitude, Width, Height, Length, Type, Speed, Color) " \
                           "VALUE('%s', %d, %f, %f, %d, %d, %d, '%s', %f, '%s')" % \
                           (timestamp, id, longitude, latitude, width, height, length, type, speed, color)
                     self.cursor.execute(sql)
                     self.db.commit()
                 # else:
                 #     print('worldframe already exists')
             except:
                 # print('Error: fail to insert worldframe')
                 self.db.rollback()

         def SearchWorldFrameTable(self, timestamp=None, id=None):
             '''
             在世界坐标对应表中查询数据
             :param timestamp: 时间帧（主码）
             :param id: 车辆/行人ID（主码）
             :return: 表项数据
             '''
             if timestamp == None:
                 if id == None:
                     print("Error: no key input")
                 else:
                     sql = "SELECT * FROM WorldFrameTable WHERE ID = %d" % (id)
                     try:
                         self.cursor.execute(sql)
                         results = self.cursor.fetchall()
                         if len(results) == 0:
                             return 0
                         return results
                     except:
                         # print("Error: unable to fecth data")
                         return 0
             else:
                 sql = "SELECT * FROM WorldFrameTable WHERE TimeStamp = '%s'" % (timestamp)
                 try:
                     self.cursor.execute(sql)
                     results = self.cursor.fetchall()
                     if len(results) == 0:
                         return 0
                     return results
                 except:
                     # print("Error: unable to fecth data")
                     return 0

         def OutputWorldFrameTable(self, directory):
             '''
             输出世界坐标对应表
             '''
             # try:
             # print (str(directory)+ "/WorldFrame.csv' ")
             sql = "select * from worldframetable into outfile '" + str(directory)+ "/WorldFrame.csv' " \
                   "fields terminated by ',' " \
                   "lines terminated by '\r\n';"
             self.cursor.execute(sql)
             # except:
             #     print("Error: file already exists")

         def SearchDirectionTable(self, id):
             '''
             查询车辆的驶入驶出方向
             :param id: 车辆ID
             :return: 车辆第一次出现的经纬度和最后一次出现的经纬度
             '''
             out = self.SearchWorldFrameTable(None, id)
             first_time = (out[-1][2], out[-1][3])
             last_time = (out[0][2], out[0][3])
             return first_time, last_time

         def SearchDirectionTable(self, id):
             '''
             查询车辆的驶入驶出方向
             :param id: 车辆ID
             :return: 车辆第一次出现的经纬度和最后一次出现的经纬度
             '''
             LONG = 2  # 经度数据在表中位置
             LAT = 3  # 纬度数据在表中位置
             out = self.SearchWorldFrameTable(None, id)
             first_time = (out[-1][LONG], out[-1][LAT])  # 更早插入的数据在表的底部
             last_time = (out[0][LONG], out[0][LAT])
             return first_time, last_time

         def CreateDrivingRecordTable(self):
             '''
             在数据库中创建车辆行驶记录表
             '''
             try:
                 # self.cursor.execute("DROP TABLE IF EXISTS DrivingRecordTable")
                 self.CreateIdTable()
                 sql = """CREATE TABLE DrivingRecordTable
                          (ID SMALLINT UNSIGNED NOT NULL,
                          Type CHAR(20) NOT NULL, Color CHAR(20) NOT NULL,
                          primary key(ID),
                          InTime CHAR(50), OutTime CHAR(50),
                          InDirection_Long Double, InDirection_Lat Double,
                          OutDirection_Long Double, OutDirection_Lat Double,
                          FOREIGN KEY(ID) REFERENCES IdTable(ID))"""
                 self.cursor.execute(sql)
             except:
                 print('DrivingRecordTable already exists')

         def InsertDrivingRecordTable(self, id):
             '''
             在车辆行驶记录表中插入数据
             :param id: 车辆ID
             '''
             TYPE = 7  # 车辆类型数据在表中位置
             COLOR = 9  # 车辆颜色数据在表中位置
             try:
                 self.InsertIdTable(id)
                 out = self.SearchDirectionTable(id)
                 indirection_long = out[0][0]
                 indirection_lat = out[0][1]
                 outdirection_long = out[1][0]
                 outdirection_lat = out[1][1]
                 results = self.SearchWorldFrameTable(None, id)
                 type = results[0][TYPE]
                 color = results[0][COLOR]
                 intime = results[-1][0]
                 outtime = results[0][0]
                 sql = "INSERT INTO DrivingRecordTable(ID, Type, Color, InTime, OutTime, " \
                       "InDirection_Long, InDirection_Lat, OutDirection_Long, OutDirection_Lat) " \
                       "VALUE(%d, '%s', '%s', '%s', '%s', %f, %f, %f, %f)" % \
                       (id, type, color, intime, outtime, indirection_long, indirection_lat, outdirection_long,
                        outdirection_lat)
                 self.cursor.execute(sql)
                 self.db.commit()
             except:
                 print('Error: fail to insert drivingrecord')
                 self.db.rollback()

         def SearchDrivingRecordTable(self, id):
             '''
             在车辆行驶记录表中查询数据
             :param id: 车辆ID(主码)
             :return: 表项数据
             '''
             sql = "SELECT * FROM DrivingRecordTable WHERE ID = %d" % (id)
             try:
                 self.cursor.execute(sql)
                 results = self.cursor.fetchall()
                 if len(results) == 0:
                     return 0
                 return results
             except:
                 return 0

         def OutputDrivingRecordTable(self, directory):
             '''
             输出车辆行驶记录表
             '''
             try:
                 sql = "select * from drivingrecordtable into outfile '" + str(directory) + "/DrivingRecord.csv' " \
                                                                                            "fields terminated by ',' " \
                                                                                            "lines terminated by '\r\n';"
                 self.cursor.execute(sql)
             except:
                 print("Error: file already exists")

         def close(self):
               self.db.close()


