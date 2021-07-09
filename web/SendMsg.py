import asyncio
from time import sleep
import websockets
from math import *

# ------------------------------------------------------------------#
# --------------------- 网页通信部分 --------------------------------#
# ------------------------------------------------------------------#

class send_car_msg:

    def __init__(self):
        self.car_message_template = ["{\"id\":", \
                         ",\"type\":\"DCS\",\"action\":\"vehicle\",\"tick\":\"%lld\"," \
                        "\"carInfo\":[{\"id_vehicle\":\"", \
                         "\",\"license\":\"", \
                        "\",\"position\":{\"x\":\"", \
                        "\",\"y\":\"", \
                        "\"},\"cartype\":\"", \
                        "\",\"color\":\"", \
                        "\",\"speed\":", \
                        ",\"rpm\":0,\"rect\":{\"x\":665,\"y\":144,\"w\":", \
                        ",\"h\":", \
                        "}}]}"]

    async def send_msg(self, websocket, car_msg):
        '''
        发送信息，输入websocket套接字，转换为二进制的车辆信息字符串
        :param websocket: 连接使用的套接字
        :param car_msg: 二进制车辆信息字符串
        '''
        await websocket.send(car_msg)

    async def main_logic(self, car_msg):
        '''
        发送信息，输入转换为二进制的车辆信息字符串
        :param car_msg: 二进制车辆信息字符串
        '''
        # 'ws://8.135.22.92/digitaltwin/MapWebSocketServer'为孪生平台ip
        try:
            async with websockets.connect('ws://8.135.22.92/digitaltwin/MapWebSocketServer') as websocket:
                print('connection finished!')
                await self.send_msg(websocket, car_msg)
        except:
            pass
            # print ("服务器error")

    def get_send_buf(self, car_msg2):
        '''
        获取待发送数据的协议头，输入转换为二进制的车辆信息字符串
        :param car_msg2: 车辆信息字符串
        '''

        # send_buf(协议头)：'@ZDX'为头标志位(4字节)
        # 0x00,0x00(2字节)为消息类型
        # 0x00,0x00,0x00,0x00(4字节)为json数据长度
        send_buf = ["@ZDX", 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        length = len(car_msg2)
        send_buf[3] = length & 0xFF
        send_buf[4] = length >> 8 & 0xFF
        send_buf[5] = length >> 16 & 0xFF
        send_buf[6] = length >> 32 & 0xFF

        # 将协议头转换为二进制格式
        car_contain = bytes(send_buf[0], encoding='utf-8')
        
        # 大端模式排列各数位数字
        for i in range(1,7):
            car_contain = car_contain+send_buf[i].to_bytes(length=1,byteorder='big',signed=False)
        
        return car_contain

    def send_to_virtual_platform(self, TimeStamp, ID, Longtitude, Latitude, Width, Height, Length, Type, CarColor, CarLicense, Speed):

        car_message_template = ["{\"id\":", \
                            ",\"type\":\"DCS\",\"action\":\"vehicle\",\"tick\":\"%lld\"," \
                            "\"carInfo\":[{\"id_vehicle\":\"", \
                            "\",\"license\":\"", \
                            "\",\"position\":{\"x\":\"", \
                            "\",\"y\":\"", \
                            "\"},\"cartype\":\"", \
                            "\",\"color\":\"", \
                            "\",\"speed\":", \
                            ",\"rpm\":0,\"rect\":{\"x\":665,\"y\":144,\"w\":", \
                            ",\"h\":", \
                            "}}]}"]
        count = 1000
        count_ = 1000000000000
        car_id = "noname11979-"

        car_msg = car_message_template[0] + str(int(ID)+count) \
                + car_message_template[1] + car_id + str(int(ID)+count_) \
                + car_message_template[2] + CarLicense \
                + car_message_template[3] + str(Longtitude) \
                + car_message_template[4] + str(Latitude) \
                + car_message_template[5] + Type \
                + car_message_template[6] + CarColor \
                + car_message_template[7] + Speed \
                + car_message_template[8] + Width \
                + car_message_template[9] + Height \
                + car_message_template[10]

        # 将车辆信息转换为二进制字符串
        car_msg_ = bytes(car_msg, encoding='utf-8')
        # 发送数据协议头(通过车辆信息得到)
        send_buf = self.get_send_buf(car_msg_)
        # 发送数据
        car_contain = send_buf + car_msg_
        # print (1)
        asyncio.get_event_loop().run_until_complete(self.main_logic(car_contain))